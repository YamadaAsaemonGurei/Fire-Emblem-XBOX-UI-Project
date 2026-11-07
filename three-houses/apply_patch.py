"""Build the Xbox prompt mod using the user's own extracted RomFS."""
from pathlib import Path
import argparse, hashlib, json, struct, zlib

def inflate(data):
    _, count, total = struct.unpack_from('<III', data)
    lengths = struct.unpack_from('<%dI' % count, data, 12)
    pos = (12 + 4 * count + 127) & ~127
    chunks = []
    for length in lengths:
        stored = struct.unpack_from('<I', data, pos)[0]
        chunks.append(zlib.decompress(data[pos+4:pos+4+stored]) if stored == length-4 else data[pos:pos+length])
        pos = (pos + length + 127) & ~127
    result = b''.join(chunks)
    if len(result) != total:
        raise ValueError('Archive decompression failed.')
    return result

def build(root, output):
    patches = json.loads((Path(__file__).parent / 'patches.json').read_text())
    metadata = (root / 'DATA0.bin').read_bytes()
    overrides = {}
    for patch in sorted(root.glob('patch*')):
        info = patch / 'INFO0.bin'
        if not info.exists():
            continue
        data = info.read_bytes()
        if len(data) % 288:
            raise ValueError('Unexpected patch index format.')
        for pos in range(0, len(data), 288):
            idx, size, stored, compressed = struct.unpack_from('<QQQQ', data, pos)
            name = data[pos+32:pos+288].split(b'\0')[0].decode()
            if not name.startswith('rom:/') or '..' in Path(name[5:]).parts:
                raise ValueError('Unsupported archive path.')
            overrides[idx] = (root / name[5:], compressed)
    prepared = {}
    with (root / 'DATA1.bin').open('rb') as archive:
        for row in patches['archives']:
            idx = row['entry']
            if idx in overrides:
                path, compressed = overrides[idx]
                original = path.read_bytes()
            else:
                offset, size, stored, compressed = struct.unpack_from('<QQQQ', metadata, idx * 32)
                archive.seek(offset)
                original = archive.read(stored)
            original = inflate(original) if compressed else original
            if hashlib.sha256(original).hexdigest() != row['original_sha256']:
                raise ValueError('Archive %d differs from the supported dump. No mod was written. Use an unmodified RomFS dump with the matching update.' % idx)
            modified = bytearray(original)
            for offset, encoded in row['edits']:
                chunk = bytes.fromhex(encoded)
                if offset < 0 or offset+len(chunk) > len(modified):
                    raise ValueError('Invalid patch range.')
                modified[offset:offset+len(chunk)] = chunk
            if hashlib.sha256(modified).hexdigest() != row['modified_sha256']:
                raise ValueError('Patch verification failed.')
            prepared[idx] = modified
    base = (root / 'patch4/INFO0.bin').read_bytes()
    if hashlib.sha256(base).hexdigest() != patches['info0_sha256']:
        raise ValueError('This patch index is from a different update or has been modified. No mod was written.')
    if output.exists():
        raise ValueError('The output folder already exists. Choose another output location or rename that folder.')
    merged = {struct.unpack_from('<Q',base,p)[0]:base[p:p+288] for p in range(0,len(base),288)}
    for idx,data in prepared.items():
        name = ('rom:/mods/xbox_ui/%d.g1t' % idx).encode()
        merged[idx] = struct.pack('<QQQQ',idx,len(data),len(data),0) + name.ljust(256,b'\0')
    romfs = output / 'romfs'
    files = romfs / 'mods/xbox_ui'
    files.mkdir(parents=True)
    for idx,data in prepared.items():
        (files / ('%d.g1t' % idx)).write_bytes(data)
    (romfs / 'patch4').mkdir()
    (romfs / 'patch4/INFO0.bin').write_bytes(b''.join(merged[i] for i in sorted(merged)))
    count1 = struct.unpack_from('<Q',(root/'patch4/INFO2.bin').read_bytes(),8)[0]
    (romfs / 'patch4/INFO2.bin').write_bytes(struct.pack('<QQ',len(merged),count1))
    print('Built and verified the mod:',output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('romfs',nargs='?',help='RomFS folder containing DATA0.bin, DATA1.bin and patch4')
    parser.add_argument('--output',type=Path,default=Path(__file__).parent/'Xbox Button Prompts')
    args = parser.parse_args()
    try:
        if not args.romfs:
            import tkinter as tk
            from tkinter import filedialog
            window = tk.Tk();window.withdraw()
            args.romfs = filedialog.askdirectory(title='Select your Three Houses RomFS dump')
            window.destroy()
            if not args.romfs:
                raise SystemExit('Cancelled.')
        build(Path(args.romfs),args.output)
    except (OSError,ValueError,KeyError,struct.error,zlib.error) as error:
        raise SystemExit('Could not build the mod: '+str(error))
