#!/usr/bin/env python3
"""Read-only RKFW/RKAF inspection. No USB access, flashing, repacking or execution.

This checks container bounds, NOT signatures, checksums or hardware compatibility.
Tested on the Imagebon H70 R33 reference package, not on an H13 R13 package.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct


def u32(data, offset):
    return struct.unpack_from('<I', data, offset)[0]


def bmp_info(data):
    if len(data) < 54 or data[:2] != b'BM':
        return None
    dib = u32(data, 14)
    if dib < 40:
        return {'format': 'BMP', 'dib_bytes': dib, 'note': 'Unsupported old DIB header'}
    return {
        'format': 'BMP', 'actual_bytes': len(data),
        'declared_bytes': u32(data, 2), 'pixel_offset': u32(data, 10),
        'dib_bytes': dib, 'width': struct.unpack_from('<i', data, 18)[0],
        'height': struct.unpack_from('<i', data, 22)[0],
        'planes': struct.unpack_from('<H', data, 26)[0],
        'bits_per_pixel': struct.unpack_from('<H', data, 28)[0],
        'compression': u32(data, 30),
    }


def inspect(data):
    base = 0
    if data[:4] == b'RKFW':
        if len(data) < 102:
            raise ValueError('Truncated RKFW header')
        base, firmware_size = u32(data, 33), u32(data, 37)
        if base < 102 or base + firmware_size > len(data):
            raise ValueError('RKFW payload outside input file')
    if data[base:base + 4] != b'RKAF':
        raise ValueError('Expected RKFW or RKAF container; format not supported')
    if base + 140 > len(data):
        raise ValueError('Truncated RKAF header')
    af = data[base:]
    count = u32(af, 136)
    if not 1 <= count <= 128 or 140 + 112 * count > len(af):
        raise ValueError('Invalid RKAF item table')
    items = []
    payloads = {}
    for i in range(count):
        p = 140 + 112 * i
        name = af[p:p + 32].split(b'\0')[0].decode('ascii')
        if not re.fullmatch(r'[a-zA-Z0-9_.-]+', name) or name in ('.', '..'):
            raise ValueError('Unsafe item name')
        if name in payloads:
            raise ValueError('Duplicate item name')
        path = af[p + 32:p + 96].split(b'\0')[0].decode('ascii')
        offset, flash, space, size = struct.unpack_from('<4I', af, p + 96)
        if size and (offset < 140 + 112 * count or offset + size > len(af)):
            raise ValueError('Item outside payload or overlapping table: ' + name)
        raw = af[offset:offset + size] if size else b''
        payloads[name] = raw
        entry = dict(name=name, package_path=path, bytes=size,
                     rkaf_offset=offset, file_offset=base + offset,
                     flash_sector=flash, sha256=hashlib.sha256(raw).hexdigest())
        bmp = bmp_info(raw)
        if bmp:
            entry['bmp'] = bmp
        items.append(entry)
    parameter = payloads.get('parameter', b'').decode('ascii', errors='replace')
    partitions = []
    for size, start, name in re.findall(
            r'(0x[0-9A-Fa-f]+)@(0x[0-9A-Fa-f]+)\(([^)]+)\)', parameter):
        partitions.append(dict(name=name, start_sector=int(start, 16),
                               sectors=int(size, 16), bytes=int(size, 16) * 512))
    return dict(container=data[:4].decode('ascii'), rkaf_offset=base,
                items=items, parameter=parameter, partitions=partitions), payloads


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--extract', type=Path, help='New directory for extracted files')
    parser.add_argument('--bmp', action='store_true', help='Inspect a standalone BMP instead')
    args = parser.parse_args()
    data = args.file.read_bytes()
    if args.bmp:
        report = bmp_info(data)
        if report is None:
            parser.error('Not a supported BMP file')
        payloads = {}
    else:
        report, payloads = inspect(data)
    report.update(file=str(args.file), sha256=hashlib.sha256(data).hexdigest(),
                  warning='No authenticity, checksum, signature or device compatibility validation')
    if args.extract:
        args.extract.mkdir(parents=True, exist_ok=False)
        for name, raw in payloads.items():
            if raw:
                (args.extract / name).write_bytes(raw)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
