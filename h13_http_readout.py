#!/usr/bin/env python3
"""Bounded HTTP GET readout of fixed H13 paths; never upload or execute files.

Run on the local PC in the display WLAN. Requires h13_network_probe.py beside
this script. No POST, setter, login, port-9999 messages or device writes.
"""
import argparse
import datetime
import hashlib
import http.client
import json
from pathlib import Path
import socket
import struct
import urllib.error
import urllib.request

from h13_network_probe import NoRedirect, device_address, get_info

TEXT_LIMIT = 65536
APP_LIMIT = 8 * 1024 * 1024
REQUESTS = (
    ('web_root', '/', None),
    ('update_identity', '/api/getdeviceinfo?cmd=8567', None),
    ('boot_mount_log', '/mountall.log', None),
    ('partition_names', '/proc/mtd', None),
    ('version_file', '/oem/etc/version', None),
    ('app_system_path', '/usr/bin/cvr_app', 'cvr_app.system-path.original'),
    ('app_webroot_path', '/cvr_app', 'cvr_app.webroot-path.original'),
)


def arm_elf(data):
    return (len(data) >= 52 and data[:6] == b'\x7fELF\x01\x01'
            and struct.unpack_from('<H', data, 18)[0] == 40)


def fetch_path(address, path, limit, http_port=8082, timeout=5):
    if path not in {p for _, p, _ in REQUESTS}:
        raise ValueError('This tool only supports the fixed, documented GET paths.')
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    request = urllib.request.Request(f'http://{address}:{http_port}{path}', method='GET',
        headers={'User-Agent': 'H13-Fixed-GET-Readout/1.0', 'Accept-Encoding': 'identity'})
    try:
        try:
            response = opener.open(request, timeout=timeout)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            data = response.read(limit + 1)
            truncated = len(data) > limit
            data = data[:limit]
            length = response.headers.get('Content-Length')
            complete = not truncated and (length is None or (length.isdigit() and int(length) == len(data)))
            result = {'path': path, 'status': response.code, 'received_bytes': len(data),
                'content_type': response.headers.get('Content-Type'),
                'server_header': response.headers.get('Server'),
                'content_length': length, 'truncated': truncated, 'complete': complete,
                'sha256': hashlib.sha256(data).hexdigest()}
            if not arm_elf(data):
                result['text'] = data[:TEXT_LIMIT].decode('utf-8', errors='replace')
                result['text_truncated'] = len(data) > TEXT_LIMIT
            return result, data
    except (OSError, urllib.error.URLError, http.client.HTTPException) as error:
        return {'path': path, 'error': str(error)}, b''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='192.168.10.1')
    parser.add_argument('--out', type=Path, help='New local directory to create')
    args = parser.parse_args()
    try:
        address = device_address(args.host)
    except ValueError as error:
        parser.error(str(error))
    now = datetime.datetime.now(datetime.timezone.utc)
    out = args.out or Path('h13-http-readout-' + now.strftime('%Y%m%d-%H%M%S'))
    out.mkdir(parents=True, exist_ok=False)
    report = {'utc': now.isoformat(), 'target_ipv4': address,
              'mode': 'Fixed HTTP GET paths only; no device writes or execution',
              'api_control': get_info(address, 2001), 'requests': {}}
    try:
        identity = json.loads(report['api_control'].get('body', ''))
    except (ValueError, TypeError):
        identity = {}
    if report['api_control'].get('status') != 200 or identity.get('product') != 'R8-V2.0':
        report['stopped'] = 'Expected R8-V2.0 API control response missing; no other paths requested.'
        print(report['stopped'])
    else:
        for label, path, filename in REQUESTS:
            result, data = fetch_path(address, path, APP_LIMIT if filename else TEXT_LIMIT)
            if filename and result.get('status') == 200 and result.get('complete') and arm_elf(data):
                destination = out / filename
                with destination.open('xb') as stream:
                    stream.write(data)
                result['saved_arm_elf_candidate'] = filename
                print('Saved ARM ELF candidate:', filename)
            report['requests'][label] = result
            print(path, '->', result.get('status', result.get('error')), result.get('received_bytes', ''), flush=True)
    with (out / 'http-report.json').open('x', encoding='utf-8') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print('Saved:', out.resolve())
    print('Keep results local; attach the report in chat. No file was executed or uploaded.')


if __name__ == '__main__':
    main()
