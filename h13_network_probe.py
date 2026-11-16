#!/usr/bin/env python3
"""Single-device H13 network diagnosis; Python standard library only.

Queries only GET deviceinfo commands 2001/2002 and connects to ten fixed TCP
ports without sending application data. No POST, login, debug activation,
ADB connection, configuration change, firmware upload or flashing.
Run locally on a computer connected to the display WLAN, not in the cloud.
"""
import argparse
import datetime
import errno
import ipaddress
import json
from pathlib import Path
import re
import socket
import urllib.error
import urllib.request

PORTS = (22, 23, 80, 443, 554, 5555, 8080, 8081, 8082, 9999)
MAX_BODY = 65536


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def device_address(value):
    address = ipaddress.IPv4Address(value)
    permitted = ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '127.0.0.0/8')
    if not any(address in ipaddress.IPv4Network(n) for n in permitted):
        raise ValueError('Use the local display IPv4 address, usually 192.168.10.1.')
    return str(address)


def probe_port(address, port, timeout=0.8):
    try:
        with socket.create_connection((address, port), timeout=timeout):
            return {'state': 'open'}
    except (TimeoutError, socket.timeout):
        return {'state': 'timeout'}
    except OSError as error:
        refused = error.errno == errno.ECONNREFUSED or getattr(error, 'winerror', None) == 10061
        return {'state': 'refused' if refused else 'error', 'error': str(error)}


def get_info(address, command, http_port=8082, timeout=6):
    if command not in (2001, 2002):
        raise ValueError('Only the two known device-info GET commands are supported.')
    url = f'http://{address}:{http_port}/api/getdeviceinfo?cmd={command}'
    # Do not expose LAN requests to an Internet proxy or follow redirects.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    request = urllib.request.Request(url, method='GET', headers={'User-Agent': 'H13-ReadOnly-Probe/1.0'})
    try:
        try:
            response = opener.open(request, timeout=timeout)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            data = response.read(MAX_BODY + 1)
            body = data[:MAX_BODY].decode('utf-8', errors='replace')
            # Redact standard full MAC-address spellings; other IDs may remain.
            body = re.sub(r'(?i)\b[0-9a-f]{2}(?::[0-9a-f]{2}){5}\b', '[MAC REDACTED]', body)
            body = re.sub(r'(?i)\b[0-9a-f]{2}(?:-[0-9a-f]{2}){5}\b', '[MAC REDACTED]', body)
            return {'status': response.code, 'content_type': response.headers.get('Content-Type'),
                    'body': body, 'truncated': len(data) > MAX_BODY}
    except (OSError, urllib.error.URLError) as error:
        return {'error': str(error)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='192.168.10.1', help='Local display IPv4 address')
    parser.add_argument('--out', type=Path, help='New JSON file to create; existing files are preserved')
    args = parser.parse_args()
    try:
        address = device_address(args.host)
    except ValueError as error:
        parser.error(str(error))
    now = datetime.datetime.now(datetime.timezone.utc)
    output = args.out or Path('h13-network-' + now.strftime('%Y%m%d-%H%M%S') + '.json')
    if output.exists():
        parser.error(f'Output already exists: {output}; choose a different --out.')
    report = {'utc': now.isoformat(), 'target_ipv4': address,
              'mode': 'Two device-info GETs and fixed-port TCP connection checks only',
              'http': {}, 'tcp': {}}
    for command in (2001, 2002):
        result = get_info(address, command)
        report['http'][str(command)] = result
        print(f'GET {command}:', result.get('status', result.get('error')))
    for port in PORTS:
        result = probe_port(address, port)
        report['tcp'][str(port)] = result
        print(f'TCP {port}:', result['state'])
    with output.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print('Saved:', output.resolve())
    print('An open port alone does not prove SSH/Telnet/ADB or usable access.')
    print('Review the local JSON before sharing; do not commit it to the public repository.')


if __name__ == '__main__':
    main()
