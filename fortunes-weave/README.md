# Fortune's Weave — Xbox Button Prompts

Replaces the main controller-symbol glyphs with Xbox-style prompts while keeping your current controls unchanged.

**Tested in-game:** Xbox prompts were confirmed working in Lichii with the supplied game build. Other emulator versions and game builds have not been verified.

## Controls

| Switch prompt | Xbox prompt |
| --- | --- |
| A / B | B / A |
| X / Y | Y / X |
| L / R | LB / RB |
| ZL / ZR | LT / RT |
| + / − | Menu / View |

Designed for position-based controller mapping: **B confirms and A cancels**. The mod changes graphics, not input settings. Different controller mappings may not match these prompts.

The changes cover the small, normal and large controller-symbol fonts. Stick glyphs, Switch controller diagrams and separate tutorial images are not replaced.

## What is included

This download contains a patcher and replacement byte ranges. It does **not** contain full game font archives, a game dump, encryption keys or an emulator. You build the finished mod from your own compatible extracted game files.

## Requirements

- A compatible, unmodified extracted RomFS. This patch was built against the supplied `FEFW ROM/131072/romfs` files; the patcher verifies the exact required fonts by hash. The folder number alone does not guarantee compatibility.
- Python 3.9 or newer, with Tkinter if you want the folder picker.
- The `zstandard` Python package.
- An emulator supporting LayeredFS. The target game ID shown in the author's setup is `04007EF01F8AE000`; open your game's actual mod location rather than assuming this ID applies to another build.

## Build and install on Windows

1. Extract this ZIP to its own folder.
2. Install Python if needed. Make sure the `python` command works.
3. Double-click **Install Dependencies.cmd**. This downloads `zstandard` into a local `dependencies` folder beside the patcher.
4. Double-click **Build Mod.cmd** and select your game's **romfs** folder. It should contain the **Font** folder.
5. Wait for the message saying the mod was built and verified.
6. Close the game. In your emulator, right-click it and choose **Open Mod Data Location**.
7. Copy the generated **Xbox Button Prompts** folder into that location.
8. Enable the mod in the game's configuration and restart the game.

Double-click the `.cmd` files in File Explorer; do not paste their contents into PowerShell.

For other platforms or terminal use:

```sh
python -m pip install -r requirements.txt
python apply_patch.py "/path/to/romfs"
```

The patcher leaves your source dump unchanged. It refuses to overwrite an existing output folder. To rebuild, rename that folder or choose a different destination:

```sh
python apply_patch.py "/path/to/romfs" --output "/path/to/Xbox Button Prompts"
```

## Compatibility

Mods replacing `Font/__nintendo_ext_003.bffnt.zst`, `Font/__nintendo_ext_003_Large.bffnt.zst` or `Font/__nintendo_ext_003_Small.bffnt.zst` need merging with this one. Do not enable two conflicting font replacements together.

No saves or controller settings are changed.

## Verification and known limitations

The patcher checks the original and modified decompressed font hashes and verifies the recompressed output. The public patch package was tested by reconstructing all three modified fonts and comparing them with the original mod build.

The author confirmed that the Xbox prompts work in-game on their setup. Separate screens may use other graphics that this version does not cover.

If the patcher reports an incompatible source, do not bypass the hash check. The source fonts differ from the build this patch targets.

## Uninstall

Disable the mod in game configuration, or close the game and remove its **Xbox Button Prompts** folder from the mod location.

## Reporting issues

Include the game build, emulator version, controller mapping, other UI mods and a screenshot of the affected prompt. Do not attach game archives or keys.

## AI disclosure

OpenAI's Codex assistant wrote the inspection, font-editing, packaging and patching scripts, and drafted this documentation. Existing A/B and X/Y artwork was rearranged from the supplied game files. New shoulder/trigger labels and Menu/View symbols were drawn with code; the labels use Arial Bold from the author's Windows installation. No AI image-generation model was used.

The author supplied the goal and game files, then tested the finished mod in-game. Codex performed file checks and inspected the font previews.

## Format references

- [BNTX-Extractor by aboood40091](https://github.com/aboood40091/BNTX-Extractor) — BNTX metadata and texture-layout reference.
- [Lichii](https://github.com/zortos293/Lichii) — native texture-tiling reference.

Those tools are not bundled in this patch-only download. This is an unofficial fan modification, not affiliated with Nintendo, Intelligent Systems or Microsoft.
