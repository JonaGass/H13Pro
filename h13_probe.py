#!/usr/bin/env python3
"""Collect H13 information through HTTP GET and existing ADB. Never flash.

Usage: python h13_probe.py --host 192.168.10.1 --adb PATH/adb.exe --pull-app
All output is saved locally. HTTP uses only cmd=2001 and cmd=2002.
No debug activation, POST requests, driver changes, reboot or root command.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import urllib.request


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--host', help='Display IP, usually 192.168.10.1')
    ap.add_argument('--adb', default='adb', help='Path to Android platform-tools adb')
    ap.add_argument('--pull-app', action='store_true', help='Read /usr/bin/cvr_app into local folder')
    ap.add_argument('--out', type=Path)
    a = ap.parse_args()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S')
    out = a.out or Path('h13-diagnose-' + stamp)
    out.mkdir(parents=True, exist_ok=False)
    report = {'utc': stamp, 'host_os': platform.system()}

    def run(args, timeout=10):
        try:
            p = subprocess.run(args, capture_output=True, timeout=timeout, check=False)
            return {'exit': p.returncode,
                    'stdout': p.stdout.decode('utf-8', errors='replace'),
                    'stderr': p.stderr.decode('utf-8', errors='replace')}
        except (OSError, subprocess.TimeoutExpired) as ex:
            return {'error': str(ex)}

    if platform.system() == 'Windows':
        ps = "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -like 'USB\\*' } | Select-Object Status,Class,FriendlyName,InstanceId | ConvertTo-Json -Depth 3"
        report['usb_devices'] = run(['powershell.exe', '-NoProfile', '-Command', ps], 20)

    if a.host:
        # Direct local LAN request; never send it to a configured Internet proxy.
        if any(c not in '0123456789.' for c in a.host):
            ap.error('--host must be an IPv4 address')
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        report['http'] = {}
        for cmd in (2001, 2002):
            url = f'http://{a.host}:8082/api/getdeviceinfo?cmd={cmd}'
            try:
                with opener.open(url, timeout=8) as response:
                    report['http'][str(cmd)] = {'status': response.status,
                        'body': response.read(65536).decode('utf-8', errors='replace')}
            except Exception as ex:
                report['http'][str(cmd)] = {'error': str(ex)}

    adb = shutil.which(a.adb)
    if adb is None and Path(a.adb).is_file():
        adb = str(Path(a.adb).resolve())
    if adb:
        listing = run([adb, 'devices', '-l'])
        report['adb_devices'] = listing
        connected = [line.split()[0] for line in listing.get('stdout', '').splitlines()
                     if len(line.split()) >= 2 and line.split()[1] == 'device']
        if len(connected) == 1:
            prefix = [adb, '-s', connected[0]]
            commands = {
                'identity': 'id', 'kernel': 'uname -a',
                'mtd': 'cat /proc/mtd', 'partitions': 'cat /proc/partitions',
                'mounts': 'cat /proc/mounts', 'cmdline': 'cat /proc/cmdline',
                'partition_names': 'ls -l /dev/block/by-name',
                'model': 'cat /proc/device-tree/model',
                'apps': 'ls -l /usr/bin/cvr_app /usr/bin/adbd',
                'mtd_names': 'for p in /sys/class/mtd/mtd[0-9]*; do echo "$p"; cat "$p/name" "$p/size" "$p/erasesize"; done',
            }
            report['device'] = {key: run(prefix + ['shell', command])
                                for key, command in commands.items()}
            if a.pull_app:
                dst = out / 'cvr_app.original'
                report['pull_app'] = run(prefix + ['pull', '/usr/bin/cvr_app', str(dst)], 90)
                if dst.is_file():
                    report['app_sha256'] = hashlib.sha256(dst.read_bytes()).hexdigest()
        else:
            report['adb_note'] = 'Need exactly one already connected, authorized device; no device selected.'
    else:
        report['adb_note'] = 'ADB not found. USB/HTTP results are still useful.'
    (out / 'diagnose.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Saved:', out.resolve())
    print('No flash or device configuration writes performed. Review diagnose.json before sharing.')


if __name__ == '__main__':
    main()
