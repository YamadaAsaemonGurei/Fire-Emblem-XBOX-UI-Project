# Three Houses Xbox Button Prompts

Xbox-style button prompts for **Fire Emblem: Three Houses**. Keeps your current controls and changes the icons to match an Xbox controller.

Version 2 includes the separate shoulder and trigger labels used on inventory tabs.

## What changes

| Switch prompt | Xbox prompt |
| --- | --- |
| A | B |
| B | A |
| X | Y |
| Y | X |
| L / R | LB / RB |
| ZL / ZR | LT / RT |
| + / − | Menu / View |

This is for the usual position-based emulator mapping: **B confirms and A cancels**. The mod does not remap your controller. If you use a different mapping, the prompts may not match.

## Requirements

- Fire Emblem: Three Houses, title ID `010055D009F78000`.
- An extracted, unmodified RomFS dump with the **1.2.0 update** applied. The patcher checks the required files and refuses incompatible dumps.
- Python 3.9 or newer. No extra Python packages are needed.
- An emulator with LayeredFS mod support. Tested by a user with Lichii, using its Eden data folder. Other emulators have not been verified.

The download contains a patcher and replacement byte ranges. **Game archives, game dumps and encryption keys are not included.** Build the mod from your own dump.

## Build the mod

1. Download the release ZIP and extract it.
2. On Windows, double-click **Build Mod.cmd**. Do not paste its contents into PowerShell.
3. Select your game's `romfs` folder. It should contain `DATA0.bin`, `DATA1.bin` and `patch4`.
4. Wait for the patcher to report that the mod was built and verified.

The finished **Xbox Button Prompts** folder appears beside the patcher. Your original dump stays unchanged.

You can also run the patcher from a terminal:

```sh
python apply_patch.py "PATH/TO/romfs"
```

## Install

1. Close the game.
2. In your emulator, right-click Three Houses and choose **Open Mod Data Location**.
3. Copy the entire **Xbox Button Prompts** folder into that location.
4. Enable the mod in the game's properties or configuration, then restart the game.

The folder structure should look like this:

```text
010055D009F78000/
└── Xbox Button Prompts/
    └── romfs/
        ├── mods/xbox_ui/
        │   └── ...modified archives...
        └── patch4/
            ├── INFO0.bin
            └── INFO2.bin
```

To upgrade, replace the previous Xbox Button Prompts folder with the newly built one. Keep a backup of your old mod folder if you want to roll back.

## Compatibility and limitations

- The patcher verifies source and output hashes. It will not silently patch a different game version.
- This mod replaces `patch4/INFO0.bin` and `INFO2.bin`. Other mods replacing those files need to be merged; copying one over the other can disable changes.
- Mods editing the same shared UI or font archives can also conflict.
- Stick prompts retain the original L/R artwork. Some tutorial images or separate screens may still contain Switch graphics.
- The initial prompts worked in the user's game. The version 2 inventory-tab fix has passed file and texture checks but still needs in-game confirmation.
- Save files and controller settings are not changed.

## Uninstall

Disable the mod in game properties, or close the game and remove its **Xbox Button Prompts** folder.

## Reporting problems

Include the game update, emulator version, controller mapping and a screenshot of the incorrect prompt. Mention any other UI or gameplay mods you use.

Do not upload game dumps, keys or save files with an issue.

## Credits

- [Three Houses Research Team](https://github.com/three-houses-research-team/Throne-of-Knowledge/wiki) for documenting the game's archive and UI formats.
- [Raytwo's G1Tool](https://github.com/Raytwo/G1Tool) and [FETH Archive Manager](https://github.com/Raytwo/feth-archive-manager) for format references.

Unofficial fan modification. Not affiliated with Nintendo, Intelligent Systems, Koei Tecmo or Microsoft.
