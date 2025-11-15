# igbFinisher
by BaconWizard17

## Description
This program takes exported igb files and processes them for release. A single exported file can be made compatible with all console versions of X-Men Legends, X-Men Legends II: Rise of Apocalypse, Marvel: Ultimate Alliance, and Marvel: Ultimate Alliance 2.

### Prerequisites
1. [Alchemy 5](https://marvelmods.com/forum/index.php/topic,11158.0.html): For applying optimizations to files.
2. [Alchemy 3.2 sgOptimizer](https://marvelmods.com/forum/index.php/topic,11586.0.html): For applying optimizations to files for last-gen consoles.
3. [BaconWizard17's Marvel Mods GIMP Scripts](https://github.com/EthanReed517/BaconWizard17-MarvelMods-GIMP-Scripts/releases/latest): For exporting textures for models.
4. [3ds Max 5 with Alchemy 2.5](https://marvelmods.com/forum/index.php/topic,10797.0.html): For creating igb files.
 
### Installation
1. Download igbFinisher and extract it to a location of your choosing.
2. Download and install Alchemy 5 per the instructions in the Alchemy 5 tutorial.
3. Within your Alchemy 5 installation, create a folder called `bin32` and extract Alchemy 3.2 sgOptimizer there.

## Usage
1. Create an igb file in 3ds Max 5 with a texture exported from the Marvel Mods GIMP Scripts.
2. Export the igb file from 3ds Max. See the section below titled "Asset Setup" for more information.
3. Set up `settings.ini` to include the necessary settings. See the section titled "Setting up settings.ini", below, for more information.
4. Drag and drop the igb file (or multiple files) onto `igbFinisher.bat`.
   - igbFinisher can also be called from the command line: `igbFinisher.exe (input file path)`
   - You have the option to call a specific settings file: `igbFinisher.exe (input file name) -s (custom settings ini file path)` or `igbFinisher.exe (input file name) --settings (custom settings ini file path)`
5. After launching, the program will confirm your settings and installation.
   - If you chose to be asked about specific settings, you'll be asked for their values at this time.
6. If the igb file was named correctly, the program will automatically recognize it. Otherwise, you'll be asked for the asset type.
   - Boltons, power models, and map models ("Other models") will never be recognized automatically due to their varied names, so you'll always be asked for their names unless you force a specific asset type in the settings.
7. igbFinisher will read the igb file to identify its texture information.
8. The program will then run through each game and console that you've specified in the settings. It will create a copy of the igb file that's optimized to work for that game and console.
9. Once processing is complete, the program will automatically close.

## Asset Setup
igbFinisher is set up to convert texture formats and apply required optimizations to an igb file for all games and consoles, so a single file can be made to work with every game and console. For igbFinisher to properly recognize the file, it must be named correctly and properly set up in 3ds Max.

All assets must be exported with Alchemy 2.5 through 3ds Max 5 and should not have any post-processing done on them unless otherwise noted.

<details>
<summary>Expand to see more information about asset setup</summary>

### 3D Assets
For all 3D models (skins, mannequins, 3D heads, and "other" models (boltons, power models, and map models)), igbFinisher supports a mix of opaque diffuse maps, transparent diffuse maps, and environment maps that were set up in 3ds Max 5. 
- For diffuse maps, use the "Export 3D Asset Texture" script from the Marvel Mods GIMP Scripts. Choose "Opaque" for opaque textures and "Transparent" for transparent textures.
- For environment maps, use the "Export Environment Maps" script from the Marvel Mods GIMP Scripts. This will export 4 different sizes for the different consoles:
   - `(texture name)_XS_(direction suffix).png`: used with the GameCube, PSP, and MUA2 PS2.
   - `(texture name)_S_(direction suffix).png`: used with XML1/XML2/MUA1 PS2.
   - `(texture name)_M_(direction suffix).png`: used with Wii and Original Xbox
   - `(texture name)_L_(direction suffix).png`: used with XML2 PC.
   igbFinisher will automatically identify the compatible console from the available environment maps. Processing will be skipped for MUA1 PC, Steam, PS3 and Xbox 360 if environment maps are detected. However, environment maps can be set up on these next-gen consoles by add a next-gen texture ini to the settings. See the section titled "Setting Up settings.ini", below, for more information.

| Asset Type | File Name to Export from 3ds Max | Additional Notes |
| ---------- | -------------------------------- | ---------------- |
| Skin (including animated boltons with skeletons) | `igActor01_Animation01DB.igb` (default file name for skins exported with the console-compatible method) | Export with the console-compatible method. |
| Mannequin | `123XX (Mannequin).igb` | If you want a custom pose name, like "OCP Pose", the file can be named `123XX (Mannequin - OCP Pose).igb`. |
| 3D Head | `123XX (3D Head).igb` | |
| Other 3D Model (BoltOn, Power Model, Map Model) | Any name, including the name that the model uses in-game | If there is a version with cel shading, the version without cel shading should be exported with the name `fileName (No Cel).igb`. |

Other notes:
- For skins, mannequins, and 3D heads, The internal numbers for geometry should use the skin number "12301," regardless of the actual skin number.
- For skins and other 3D models, if they use cel shading, the cel shading geometry's name must end in "_outline" for igbFinisher to automatically recognize that the model has cel shading. Otherwise, it will be processed as though it doesn't have cel shading.

### 2D Assets
All 2D assets should only have 1 texture, and they all support opaque textures. For some, transparent textures are also supported.

| Asset Type | GIMP Script to Export Textures | File Name to Export from 3ds Max | Additional Notes |
| ---------- | ------------------------------ | -------------------------------- | ---------------- |
| Conversation Portrait (HUD) | Export Conversation Portrait (HUD) ***or*** Export Multiple Portraits (CSP and HUD) | `hud_head_123XX.igb` | Transparent textures are supported for next-gen style HUDs. |
| Character Select Portrait (CSP) | Export Character Select Portrait (CSP) ***or*** Export Multiple Portraits (CSP and HUD) | `123XX (Character Select Portrait).igb` | |
| Power Icons | Export Power Icons | `power_icons.igb` | Uses opaque textures for XML1 and XML2 and transparent textures for MUA1 and MUA2. |
| Comic Covers | Export Comic Covers | `comic_cov.igb` | |
| Concept Art | Export Concept Art | `concept.igb` | |
| Loading Screen | Export Loading Screen | `123XX (Loading Screen).igb` | |

Other notes:
- HUDs, CSPs, and Loading Screens will be named and hex edited using the character numbers. 
- Power Icons, Comic Covers, and Concept Art use the texture name to get the output file name.
- HUDs use the prefix of the texture name to identify the type and give it a unique output file name. 
- CSPs, Loading Screens, Power Icons, Comic Covers, and Concept Art use the prefix x of the texture name to determine the compatible game.

</details>

## Settings.ini Setup
`settings.ini` in the `igbFinisher` folder contains important settings that are used to run the program properly. Before running it, be sure to set up the values appropriately. Alternatively, you can set up a custom `settings.ini` file with any name and specify that as an input argument to the program.

<details>
<summary>Expand to see information about the settings</summary>

| Section | Setting Value | Explanation | Possible Values | Additional Information |
| ------- | ------------- | ----------- | --------------- | ---------------------- |
| \[CHARACTER\] | XML1_num, XML2_num, MUA1_num, MUA2_num | The skin number for the specified game. | - **None**: Skips processing for this game.<br/>- **Ask**: Asks you for a skin number during runtime.<br/>- Any 4- or 5-digit skin number. | Skin numbers are not used with Power Icons, Comic Covers, Concept Art, or Other models, except to check if assets should be exported for this game. |
| \[CHARACTER\] | XML1_path, XML2_path, MUA1_path, MUA2_path | The path that the asset will export to for the specified game. | - **None**: Skips processing for this game</br>- **Ask**: Asks you for a path during runtime.<br/>- **Detect**: To use the folder detection option.<br/>- A hard-coded path, which must exist. | |
| \[ASSET\] | XML1_num_XX, XML2_num_XX, MUA1_num_XX, MUA2_num_XX | If the skin number should end in `XX` for the exported file name. | - **True**: The last two digits of the skin number in the file name will be replaced with `XX` (my preferred setting).<br/>- **False**: Skin numbers in file names will not end in `XX` (the full skin number will be used instead).<br/>- **Ask**: Asks you about this setting during runtime. | This setting only impacts Skins, Mannequins, 3D Heads, Conversation Portraits, Character Select Portraits, and Loading Screens. |
| \[ASSET\] | XML1_special_name, XML2_special_name, MUA1_special_name, MUA2_special_name | The special name for the selected game. | - **None**: Follows the typical naming convention for this asset type.<sup>1</sup><br/>- **NumberOnly**: Removes any descriptor or suffix and only exports the file with the skin number.<br/>- **Ask**: Asks you about this setting during runtime.<br/>- Any pre-populated special name without a file extension. | For Skins, Mannequins, 3D Heads, Conversation Portraits, Character Select Portraits, and Loading Screens, this value is added as a custom suffix to the file name. For the other asset types, this value will be used for the full file name.<br/>A **NumberOnly** value will be ignored for any asset type that doesn't use a skin number. |
| \[CONSOLES\] | PC, Steam, GameCube, PS2, PS3, PSP, Wii, Xbox, Xbox_360 | If assets should be exported for this console. |  **True**: Assets will be exported for this console.<br/>- **False**: Assets will not be exported for this console.<br/>- **Ask**: Asks you about this setting during runtime. | If all games that use this console are skipped (like if they're disabled by the settings or if the asset isn't compatible with those games), nothing will be exported for the selected console regardless of what is entered. |
| \[SETTINGS\] | big_texture | If oversized textures should preserve their original size on weaker consoles. | **True**: Oversized textures should preserve their original size on weaker consoles (recommended for large characters, like Galactus/Ymir, or for specific assets like maps).<br/>- **False**: Oversized textures will be scaled to the maximum allowed for the weaker console.<br/>- **Ask**: Asks you about this setting during runtime. | The weaker consoles are the GameCube, PS2, and PSP. The maximum allowed texture size depends on the console and asset. For the GameCube, PSP, and MUA2 PS2, a **True** value will still cut the texture sizes in half. |
| \[SETTINGS\] | secondary_skin | If this is a secondary skin (like Human Torch's flame on skin), which should have its texture size cut in half on weaker consoles. | **True**: This is a secondary skin, so the texture size should be reduced in half for weaker consoles.<br/>- **False**: This is not a secondary skin, so texture sizes can be the maximum allowed for the console.<br/>- **Ask**: Asks you about this setting during runtime. | The weaker consoles are the GameCube, PS2, and PSP. The maximum allowed texture size depends on the console and asset. This setting only applies to Skins. For XML1/XML2/MUA1 PS2, this setting also applies to Other models, which are sometimes the same resolution as the more powerful consoles, but sometimes they are the same as the weaker consoles. |
| \[SETTINGS\] | untextured_okay | If it's okay to process an asset without textures. | **True**: It's okay to process an asset without textures.<br/>- **False**: It's not okay to process an asset without textures.<br/>- **Ask**: Asks you about this setting during runtime. | |
| \[SETTINGS\] | generate_collision | If collision should be generated with the Alchemy 3.2 "igCollideHullRaven" optimization. | **True**: Collision should be generated.<br/>- **False**: Collision should not be generated.<br/>- **Ask**: Asks you about this setting during runtime. | This setting only applies to Other models and is only recommended for map models. |
| \[SETTINGS\] | igBlend_to_igAlpha_transparency | If igBlendFunctionAttr should be hex edited to igAlphaFunctionAttr and igBlendStateAttr should be hex edited to igAlphaStateAttr to allow transparent textures to appear correctly. | **True**: These values should be hex edited.<br/>- **False**: These values should not be hex edited.<br/>- **Ask**: Asks you about this setting during runtime. | |
| \[SETTINGS\] | skip_subfolder | If the console-specific sub-folder should be skipped when exporting the assets, and the asset will just be exported directly to the chosen export directory. | **True**: The console-specific sub-folder should be skipped (not recommended unless you are only exporting for one game and console).<br/>- **False**: The console-specific sub-folder should not be skipped when (recommended).<br/>- **Ask**: Asks you about this setting during runtime. | |
| \[SETTINGS\] | force_adv_tex_folders | If the advanced texture folder structure should be forced (separate XML2 PC and Xbox, MUA1 PC and 360, and MUA1 PS3 and Steam into their own folders). | **True**: This folder structure should be forced (recommended for portraits used with skins that have advanced textures).<br/>- **False**: This folder structure should not be forced.<br/>- **Ask**: Asks you about this setting during runtime. | A **False** value is ignored if advanced textures are detected. |
| \[SETTINGS\] | advanced_texture_ini | If an ini file for advanced textures should be used. | **None**: No advanced textures should be used.<br/>- **Ask**: Asks you for a path to an advanced texture ini file during runtime.<br/>- A hard-coded path to an advanced texture ini file. | If an advanced texture ini file is used, the asset will only be exported for MUA1 PC, Steam, PS3, and Xbox 360. This only works with 3D assets. For more information on advanced texture ini files, see the section titled "Advanced Texture Usage", below. |
| \[SETTINGS\] | forced_asset_type | If a specific asset type should be forced. | - **None**: no asset type should be forced, assets will be recognized from the file name (recommended).<br/>**Ask**: Always ask for the asset type regardless of what is detected.<br/>- Any of the following asset types: **Skin**, **Mannequin**, **3D Head**, **Conversation Portrait**, **Character Select Portrait**, **Power Icons**, **Comic Cover**, **Concept Art**, **Loading Screen**, **Other** | If **None** is selected and the asset type is not recognized, you will still be asked for the asset type. |

<sup>1</sup>The typical naming convention is as follows (using example skin number 12301):
- Skins: `12301 (Skin).igb` (or `12301 (Skin - No Cel Shading).igb` for XML1/XML2 skins without cel shading)
- Mannequins: `12301 (Mannequin).igb`
- 3D Heads: `12301 (3D Head).igb`
- Other models: The same name as the input file
- Conversation Portraits (HUDs): `hud_head_12301.igb` (will include a descriptor based on the texture prefix if available)
- Character Select Portraits (CSPs): `12301 (Character Select Portrait).igb` (will include a descriptor based on the texture prefix if available)
- Power Icons: The name of the texture (minus any game-specific prefix)
- Comic Covers: The name of the texture (minus any game-specific prefix)
- Concept Art: The name of the texture (minus any game-specific prefix)
- Loading Screens: `12301 (Loading Screen).igb`

If XML1_num_XX, XML2_num_XX, MUA1_num_XX, or MUA2_num_XX are set to **True**, any `12301` would be replaced with `123XX`.

</details>

## Folder Detection
igbFinisher has the capability to detect the output folder using parts of the texture's path.

<details>
<summary>Expand to see information about the settings</summary>

For this option to work correctly, the texture path must be set up a specific way, and you must also set up a .xml file that the folder can be detected from. Here's how to do this:
+ First, it's necessary to create the detection .xml file. I've already included some examples in the `Folder Detection` folder that comes with igbFinisher. Create a .xml file in this folder named after your character, and include paths for the different folder names based on the example.
+ Next, the texture path should be set up correctly. The path for the .xcf file should be like this: `..\(character name)\(asset type)\(asset name)\12301.xcf` (or `12301_descriptor.xcf` for secondary textures). This will result in the GIMP script exporting to a path like so: `..\(character name)\(asset type)\(asset name)\12301.png` (or `12301_descriptor.png` for secondary textures).
   + Here's what each folder means:
     + `(character name)` is the name of the character, and will be the same as the name of the .xml file in the `Folder Detection` folder.
     + `(asset type)` is not used by igbFinisher, but this is how I organize my files. Realistically, this folder can be anything, but it has to be in the structure like this.
     + `(asset name)` is whatever you want to name the asset. This value corresponds with a `tex_folder` attribute within the .xml file.
   + An example texture path would be:
     + `..\Cyclops\Skins\90s\12301.xcf`, which would export to `..\Cyclops\Skins\90s\12301.png`.
     + The `Cyclops` folder corresponds with a `Cyclops.xml` file in the `Folder Detection` folder, and the `90s` folder corresponds with a `tex_folder="90s"` attribute for one of the `skin` elements in the .xml file.

</details>

## Advanced Texture Usage
igbFinisher has the ability to set up advanced textures for you. More information on this is coming soon!

## Asset Output
Assets that are the same for different games will be placed into folders together for convenience. Each folder will be labeled based on the game and console that it supports. The assets will be appropriately named, and will also be hex edited and Alchemy optimized if applicable.

## Development
Want to help develop igbFinisher? igbFinisher is developed with [Python 3](https://www.python.org/downloads/). There are several Python packages that you'll need to install:
1. [Pillow](https://pypi.org/project/pillow/)
2. [PyInstaller](https://pyinstaller.org/en/stable/)
3. [Questionary](https://pypi.org/project/questionary/)
4. [tkinterdnd2](https://pypi.org/project/tkinterdnd2/)