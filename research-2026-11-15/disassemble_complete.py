"""Offline ARM disassembly with literal strings and dynamic symbol annotations."""
import sys
import struct
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_MEM, ARM_REG_PC

with open(sys.argv[1], 'rb') as f:
    elf = ELFFile(f)
    sections = list(elf.iter_sections())
    symbols = {}
    for section in sections:
        if section['sh_type'] in ('SHT_DYNSYM', 'SHT_SYMTAB'):
            for symbol in section.iter_symbols():
                if symbol['st_value']:
                    symbols[symbol['st_value']] = symbol.name
    def read(address, length):
        for section in sections:
            if section['sh_type'] == 'SHT_NOBITS':
                continue
            start = section['sh_addr']
            if start <= address < start + section['sh_size']:
                offset = address - start
                return section.data()[offset:offset + length]
        return b''
    def describe(address):
        data = read(address, 200).split(b'\0')[0]
        if len(data) >= 3 and all(32 <= c < 127 or c in (9, 10, 13) for c in data):
            return repr(data.decode())
        return symbols.get(address, '')
    # ARM GNU PLT: 20-byte header followed by 12-byte entries in this binary.
    plt = elf.get_section_by_name('.plt')
    reloc = elf.get_section_by_name('.rel.plt')
    if plt is not None and reloc is not None:
        dynsym = elf.get_section(reloc['sh_link'])
        for i, relocation in enumerate(reloc.iter_relocations()):
            symbols[plt['sh_addr'] + 20 + i * 12] = dynsym.get_symbol(
                relocation['r_info_sym']).name + '@plt'
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    md.skipdata = True
    for request in sys.argv[2:]:
        if ':' in request:
            start, size = (int(v, 0) for v in request.split(':'))
        else:
            symbol = next(s for sec in sections if sec['sh_type'] in
                          ('SHT_DYNSYM', 'SHT_SYMTAB')
                          for s in sec.iter_symbols() if s.name == request)
            start, size = symbol['st_value'], symbol['st_size']
        print('\nFUNCTION', hex(start), symbols.get(start, ''), 'size', size)
        for ins in md.disasm(read(start, size), start):
            if ins.id == 0:
                print(f'{ins.address:08x}  [undecodable bytes] {ins.bytes.hex()}')
                continue
            comment = ''
            if ins.mnemonic.startswith('ldr') and len(ins.operands) == 2:
                op = ins.operands[1]
                if op.type == ARM_OP_MEM and op.mem.base == ARM_REG_PC and not op.mem.index:
                    literal_address = ins.address + 8 + op.mem.disp
                    literal = read(literal_address, 4)
                    if len(literal) == 4:
                        value = struct.unpack('<I', literal)[0]
                        comment = hex(value) + ' ' + describe(value)
            elif ins.mnemonic in ('bl', 'b'):
                try:
                    comment = symbols.get(int(ins.op_str.lstrip('#'), 0), '')
                except ValueError:
                    pass
            print(f'{ins.address:08x}  {ins.mnemonic:8} {ins.op_str:30} {comment}')
