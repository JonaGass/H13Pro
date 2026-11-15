"""Offline ARM control-flow checks on the pinned H70 reference, with mocked I/O.

No target connection, shell execution, ARM syscalls or firmware writes occur.
This does not emulate a complete system or prove H13 compatibility.
Requires unicorn==2.1.4 and pyelftools.
"""
import hashlib
import json
from pathlib import Path
import sys

from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R2

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'reference-rootfs/1305731643/rootfs/usr/bin/cvr_app'
EXPECTED = '9a719fc17bc404c3f640c9aa117fbb973bf0edb4adc4c8d899500c1ebc874c79'
if hashlib.sha256(APP.read_bytes()).hexdigest() != EXPECTED:
    raise SystemExit('This harness only supports the pinned H70 reference binary.')

with APP.open('rb') as f:
    elf = ELFFile(f)
    segments = [(s['p_vaddr'], s.data()) for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD']
    dynsym = elf.get_section_by_name('.dynsym')
    symbols = {s['st_value']: s.name for s in dynsym.iter_symbols() if s['st_value']}
    functions = {s.name: (s['st_value'], s['st_size']) for s in dynsym.iter_symbols() if s['st_value'] and s['st_size']}
    rel = elf.get_section_by_name('.rel.plt')
    plt = elf.get_section_by_name('.plt')
    for i, r in enumerate(rel.iter_relocations()):
        symbols[plt['sh_addr'] + 20 + 12*i] = dynsym.get_symbol(r['r_info_sym']).name

SD = '/mnt/sdcard/rk_pcba_test_res'
SENTINEL = 0x600000


def run(phase, present):
    entry_name = {'entry': '_Z9pcba_testv', 'ui': '_Z15CreateBigWindowv', 'thread': '_Z10ddr_ThreadPv'}[phase]
    entry, size = functions[entry_name]
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(0x10000, 0x300000)
    uc.mem_map(0x500000, 0x100000)
    uc.mem_map(SENTINEL, 0x1000)
    uc.mem_map(0x700000, 0x10000)
    for address, data in segments:
        uc.mem_write(address, data)
    uc.reg_write(UC_ARM_REG_SP, 0x70ff00)
    uc.reg_write(UC_ARM_REG_LR, SENTINEL)
    result = {'phase': phase, 'present': sorted(present), 'accesses': [], 'threads': [], 'system_commands': [], 'stop': None}
    heap = 0x500000

    def cstring(address):
        return bytes(uc.mem_read(address, 512)).split(b'\0', 1)[0].decode('utf-8', errors='replace')

    def hook(machine, address, length, ignored):
        nonlocal heap
        if address == SENTINEL:
            result['stop'] = 'function returned'
            machine.emu_stop()
            return
        if entry <= address < entry + size:
            return
        name = symbols.get(address, hex(address))
        return_value = 0
        if name == 'access':
            path = cstring(machine.reg_read(UC_ARM_REG_R0))
            result['accesses'].append(path)
            return_value = 0 if path in present else -1
        elif name == '_Z15CreateBigWindowv' and phase == 'entry':
            result['stop'] = 'selected CreateBigWindow'
            machine.emu_stop()
            return
        elif name == 'system':
            result['system_commands'].append(cstring(machine.reg_read(UC_ARM_REG_R0)))
        elif name == 'pthread_create':
            target = machine.reg_read(UC_ARM_REG_R2)
            result['threads'].append({'address': hex(target), 'symbol': symbols.get(target, '?')})
        elif name == 'pthread_exit':
            result['stop'] = 'pthread_exit'
            machine.emu_stop()
            return
        elif name in ('__stack_chk_fail', '__stack_chk_fail_local'):
            raise RuntimeError('Stack guard failed')
        elif name == '__xpg_basename':
            return_value = machine.reg_read(UC_ARM_REG_R0)
        elif name == 'lv_disp_get_hor_res':
            return_value = 1600
        elif name == 'lv_disp_get_ver_res':
            return_value = 600
        elif name == '_Z13pcba_ddr_testv':
            return_value = 512
        elif name == '_Z18pcba_norflash_testv':
            return_value = 256
        elif name in ('_ZN12SystemConfig19GetScreenResolutionEv', '_ZN12SystemConfig19PureCarplayMotoFlagEv', '_ZN18StartWindowFactory13GetWindowTypeEv'):
            return_value = 0
        elif name in ('_ZN12SystemConfig11GetInstanceEv', '_ZN18StartWindowFactory11GetInstanceEv', '_ZN7Preview11GetInstanceEv', 'lv_disp_get_default', 'lv_obj_create', 'lv_label_create', 'lv_imgbtn_create', '0x220754'):
            return_value = heap
            heap += 0x400
        elif name.startswith('lv_') or name in ('C_LJQ_LOG2', 'puts', 'printf', 'perror', 'sleep', 'pthread_mutex_init', '_ZN7Preview11ShowDisplayEv'):
            return_value = 0
        else:
            raise RuntimeError(f'Unmocked external call in {phase}: {hex(address)} {name}')
        machine.reg_write(UC_ARM_REG_R0, return_value & 0xffffffff)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, hook)
    uc.emu_start(entry, SENTINEL + 4, timeout=5_000_000, count=100_000)
    if result['stop'] is None:
        raise RuntimeError('Emulation budget exhausted before a defined stop')
    return result


present = {SD, SD+'/pcba_factory_flag_file', SD+'/pcba_ddr_special_flag_file', SD+'/memtester_smd'}
results = [run('entry', set()), run('entry', present), run('ui', present), run('thread', present)]
assert results[0]['stop'] == 'function returned'
assert results[1]['stop'] == 'selected CreateBigWindow'
assert [t['symbol'] for t in results[2]['threads']] == ['_Z10ddr_ThreadPv', '_Z9tp_ThreadPv']
assert results[3]['system_commands'] == [
    'mount -o remount,rw /',
    'chmod 777 /mnt/sdcard/rk_pcba_test_res/memtester_smd',
    '/mnt/sdcard/rk_pcba_test_res/memtester_smd 128m 1',
]
print(json.dumps({'reference_sha256': EXPECTED, 'scope': 'Real ARM instructions for three isolated functions; filesystem, LVGL, threads and libc mocked; no actual shell commands executed; not an H13 test.', 'results': results}, indent=2))
