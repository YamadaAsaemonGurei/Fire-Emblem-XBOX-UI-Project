"""Build Fortune's Weave Xbox prompts from a compatible, user-supplied RomFS."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent / 'dependencies'))

def build(root, output):
    try:
        import zstandard as zstd
    except ImportError:
        raise ValueError('Missing zstandard. Run Install Dependencies.cmd first, or install requirements.txt into your Python environment.')
    payload = json.loads((Path(__file__).parent / 'patches.json').read_text())
    if output.exists():
        raise ValueError('The output folder already exists. Rename it or choose a different --output folder.')
    prepared = {}
    for row in payload['files']:
        relative = Path(row['file'])
        if relative.is_absolute() or '..' in relative.parts or relative.parts[0] != 'Font':
            raise ValueError('Invalid patch path.')
        source = root / relative
        original = zstd.ZstdDecompressor().decompress(source.read_bytes(), max_output_size=16*1024*1024)
        if hashlib.sha256(original).hexdigest() != row['original_sha256']:
            raise ValueError('Incompatible or modified source file: '+str(relative)+'. No mod was written. Use the original fonts from the matching extracted build.')
        modified = bytearray(original)
        for offset, encoded in row['edits']:
            chunk = bytes.fromhex(encoded)
            if offset < 0 or offset+len(chunk) > len(modified):
                raise ValueError('Invalid patch range.')
            modified[offset:offset+len(chunk)] = chunk
        if hashlib.sha256(modified).hexdigest() != row['modified_sha256']:
            raise ValueError('Output verification failed: '+str(relative))
        packed = zstd.ZstdCompressor(level=12).compress(modified)
        if zstd.ZstdDecompressor().decompress(packed) != modified:
            raise ValueError('Compression verification failed.')
        prepared[relative] = packed
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.xbox-ui-', dir=output.parent))
    try:
        for relative, packed in prepared.items():
            target = stage / 'romfs' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(packed)
        stage.rename(output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    print('Built and verified:', output)
    print('Copy this entire folder into the game\'s Mod Data Location, enable it, and restart the game.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('romfs', nargs='?', help='Folder containing Font/__nintendo_ext_003*.bffnt.zst')
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent / 'Xbox Button Prompts')
    args = parser.parse_args()
    try:
        if not args.romfs:
            import tkinter as tk
            from tkinter import filedialog
            window = tk.Tk()
            window.withdraw()
            args.romfs = filedialog.askdirectory(title="Select Fortune's Weave RomFS folder")
            window.destroy()
            if not args.romfs:
                raise SystemExit('Cancelled.')
        build(Path(args.romfs), args.output)
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        raise SystemExit('Could not build the mod: '+str(error))
