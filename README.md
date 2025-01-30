# igbFinisher
by BaconWizard17

## Description
This is a program to perform finishing operations on igb files to prepare them for release.

### Prerequisites
1. [Alchemy 5](https://marvelmods.com/forum/index.php/topic,11158.0.html) must be installed
2. [BaconWizard17's Marvel Mods GIMP Scripts](https://github.com/EthanReed517/BaconWizard17-MarvelMods-GIMP-Scripts/releases/latest) are needed when creating assets.
3. [3ds Max 5 with Alchemy 2.5](https://marvelmods.com/forum/index.php/topic,10797.0.html) is needed to create assets.
 
### Installation
1. Download/install all prerequisites.
2. Download igbFinisher.
3. Extract it in a location of your choosing.

## Usage
1. Export an igb file to use with the finisher. See the section below titled "Asset Setup" for more information.
2. Set up `settings.ini` to work with the current character. See the section below titled "Settings.ini Setup" for more information.
3. Double click on `igbFinisher.exe`. Two windows will launch: a command window and the drag and drop UI.
4. The program will confirm that all settings are valid before it begins running.
5. Drag and drop the igb file into the drag and drop window.
   + Only one asset can be run through the igbFinisher at a time, but multiple console versions are created on each run.
6. If the igb file is named correctly, it will be automatically recognized by igbFinisher. If not, you'll be asked about the asset type.
7. Depending on your settings, you may be asked additional questions about the asset.
8. The texture format and any asset-specific information will be automatically identified from the igb file.
9. The script will run the required processes on the skin, including hex editing and Alchemy operations, and then send the files to the appropriate destination folders. See the section below titled "Asset Output" for more information.
10. Once the asset is successfully exported, you'll get a completion message.
11. You can repeat the process for any additional igb files by simply dragging and dropping them onto the UI.
12. Once you're done, you can close the windows.

### Settings.ini Setup
`settings.ini` in the `igbFinisher` folder contains important settings that are used to run the finisher properly. Before running it, be sure to set up the values appropriately.

The following settings are used:
+ `xml1num`: Can be `None` to skip exporting for XML1, `Ask` to ask each time the program runs, or a pre-populated skin number.
   + Pre-populated skin numbers: for general processing, enter a 2 or 3 digit character number followed by `XX` (i.e., `01XX` or `172XX`). The skin will be processed with generic names and hex edited to the skin number ending in `01`. If a specific skin number is required for the asset, that can be used instead, and this will allow for special descriptions or no descriptions.
+ `xml2num`: Can be `None` to skip exporting for XML2, `Ask` to ask each time the program runs, or a pre-populated skin number.
   + Pre-populated skin numbers: for general processing, enter a 2 or 3 digit character number followed by `XX` (i.e., `01XX` or `172XX`). The skin will be processed with generic names and hex edited to the skin number ending in `01`. If a specific skin number is required for the asset, that can be used instead, and this will allow for special descriptions or no descriptions.
+ `mua1num`: Can be `None` to skip exporting for MUA1, `Ask` to ask each time the program runs, or a pre-populated skin number.
   + Pre-populated skin numbers: for general processing, enter a 2 or 3 digit character number followed by `XX` (i.e., `01XX` or `172XX`). The skin will be processed with generic names and hex edited to the skin number ending in `01`. If a specific skin number is required for the asset, that can be used instead, and this will allow for special descriptions or no descriptions.
+ `mua2num`: Can be `None` to skip exporting for MUA1, `Ask` to ask each time the program runs, or a pre-populated skin number.
   + Pre-populated skin numbers: for general processing, enter a 2 or 3 digit character number followed by `XX` (i.e., `01XX` or `172XX`). The skin will be processed with generic names and hex edited to the skin number ending in `01`. If a specific skin number is required for the asset, that can be used instead, and this will allow for special descriptions or no descriptions.
+ `xmlpath`: Can be `None` to skip exporting for XML1 and XML2, `Ask` to ask each time the program runs, `Detect` to detect the destination path using the texture folder, or a pre-populated file path for the XML1/XML2 release to automatically process.
   + If both `xml1num` and `xml2num` are set to `None`, exporting will be skipped anyways.
   + For more information on the `Detect` option, see the "Folder Detection" section, below.
+ `muapath`: Can be `None` to skip exporting for MUA1 and MUA2, `Ask` to ask each time the program runs, `Detect` to detect the destination path using the texture folder, or a pre-populated file path for the MUA1/MUA2 release to automatically process.
   + If both `mua1num` and `mua2num` are set to `None`, exporting will be skipped anyways.
   + For more information on the `Detect` option, see the "Folder Detection" section, below.
+ `pcOnly`: Whether or not you want to finish assets for only the PC or for all consoles. Can be `True` or `False`.
   + `True` will export assets for XML2 PC, MUA1 PC, and MUA1 Steam only.
   + `False` will export assets for all consoles.

### Folder Detection
For my own uses, I built in a folder detection option for igbFinisher. This allows me to process multiple files at a time to different folders without having to enter a path each time. You can also use this option, but the texture path must be set up a specific way, and you must also set up a .xml file that the folder can be detected from. Here's how to do this:
+ First, it's necessary to create the detection .xml file. I've already included some examples in the `Folder Detection` folder that comes with igbFinisher. Create a .xml file in this folder named after your character, and include paths for the different folder names based on the example.
+ Next, the texture path should be set up correctly. The path for the .xcf file should be like this: `..\(character name)\(asset type)\(asset name)\12301.xcf` (or `12301_descriptor.xcf` for secondary textures). This will result in the GIMP script exporting to a path like so: `..\(character name)\(asset type)\(asset name)\(console compatibility)\12301.(console-specific file extension)`.
   + Here's what each folder means:
     + `(character name)` is the name of the character, and will be the same as the name of the .xml file in the `Folder Detection` folder.
     + `(asset type)` is not used by igbFinisher, but this is how I organize my files, so it must be in the file path like this.
     + `(asset name)` is whatever you want to name the asset. This value corresponds with a `texPath` attribute within the .xml file.
     + `(console compatibility)` is the folder created by the GIMP script that houses the exported texture and tells you which consoles and games it's compatible with.
     + `(console-specific file extension`) will either be `png` or `dds`, depending on the console and settings.
   + An example texture path would be:
     + `..\Cyclops\Skins\90s\12301.xcf`, which would export to `..\Cyclops\Skins\90s\PC, PS2, Xbox, and MUA1 360\12301.png` (among other textures).
     + The `Cyclops` folder corresponds with a `Cyclops.xml` file in the `Folder Detection` folder, and the `90s` folder corresponds with a `texFolder="90s"` attribute for one of the `skin` elements in the .xml file.

### Asset Setup
Because texture formats repeat across various consoles, one texture type can cover multiple different console versions. You can export a version of each texture format and run it through this program, and finished versions for multiple consoles will be created.

All assets must be exported with Alchemy 2.5 through 3ds Max 5 and should not have any post-processing done on them unless otherwise noted.

#### All 3D Models
For all 3D models (skins, mannequins, 3D heads, and other models), igbFinisher supports regular diffuse textures, transparent diffuse textures, and any environment maps that were set up in 3ds Max. The texture formats must align for igbFinisher to be able to process them correctly. For an easy reference to the different folders that can be used together, check out the tables below:
***PC ONLY***
| Environment Map Folder | Opaque Diffuse Map Folder | Transparent Diffuse Map Folder |
| ---------------------- | ------------------------- | ------------------------------ |
| `PC` | `PC` | `PC and MUA1 Steam` |
| `XML2 PC` | `XML2 PC` | `PC and MUA1 Steam` |
| `MUA1 PC and Steam` | `MUA1 PC and Steam` | `PC and MUA1 Steam` |

***ALL CONSOLES***
| Environment Map Folder | Opaque Diffuse Map Folder | Transparent Diffuse Map Folder |
| ---------------------- | ------------------------- | ------------------------------ |
| `XML2 PC` | `XML2 PC, Xbox, and Wii` | `PC, PS2, Wii, Xbox, MUA1 Steam, PS3, and 360` ***OR*** `PC, Wii, Xbox, MUA1 Steam, PS3, and 360` |
| `PC and MUA1 360` | `PC, PS2, Xbox, and MUA1 360` ***OR*** `PC, Xbox, and MUA1 360` | `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` ***OR*** `PC, Wii, Xbox, MUA1 Steam, PS3, and 360` |
| `MUA1 PC, Steam, 360, and PS3` | `MUA1 PC, Steam, 360, and PS3` | `PC, Wii, Xbox, MUA1 Steam, PS3, and 36`0 |
| `Xbox` | `PC, PS2, Xbox, and MUA1 360` ***OR*** `PC, Xbox, and MUA1 360` | `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` ***OR*** `PC, Wii, Xbox, MUA1 Steam, PS3, and 360` |
| `Wii` | `Wii` | `PC, PS2, Wii, Xbox, MUA1 Steam, PS3, and 360` ***OR*** `PC, Wii, Xbox, MUA1 Steam, PS3, and 36`0 |
| `Xbox and Wii` | `XML2 PC, Xbox, and Wii` ***OR*** `Wii` | `PC, PS2, Wii, Xbox, MUA1 Steam, PS3, and 360` ***OR*** `PC, Wii, Xbox, MUA1 Steam, PS3, and 360` |
| `Xbox, Wii, and XML2 PC` | `XML2 PC, Xbox, and Wii` | `PC, PS2, Wii, Xbox, MUA1 Steam, PS3, and 360` ***OR*** `PC, Wii, Xbox, MUA1 Steam, PS3, and 360` |
| `PS2` | `PC, PS2, Xbox, and MUA1 360` ***OR*** `PS2` | `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` ***OR*** `PS2` |
| `GameCube, PSP, and MUA2 PS2` | `GameCube, PSP, and MUA2 PS2` | `GameCube, PSP, and MUA2 PS2` |

Note that any folder that is only for MUA1 Steam and PS3 is skipped, because that format can be created with Alchemy optimizations from other textures. Additionally, the PSP must use PNG8 textures to be compatible. PNG4, DXT3, and DXT5 textures are not supported.

#### Skins
All skins should be exported with the console-compatible method. The default file name, `igActor01_Animation01DB.igb` should not be changed. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number. If the skin uses cel shading, the cel shading model's name must end in "_outline" for igbFinisher to automatically recognize that the model has cel shading. Otherwise, it will be processed as though it doesn't have cel shading. See the tables above for information on supported texture formats.

#### Mannequins
All mannequins should be exported with the file name `123XX (Mannequin).igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number. If you want to have a custom pose name for your mannequin (for example, "OCP Pose"), you can export it with the name `123XX (Mannequin - OCP Pose).igb`, and the resulting file will have that pose name in its name. See the tables above for information on supported texture formats. For mannequins, any texture formats that are exclusive to XML2 can be skipped, since mannequins aren't used in XML2.

#### 3D Heads
All 3D Heads should be exported with the file name `123XX (3D Head).igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number. See the tables above for information on supported texture formats. For 3D heads, any texture formats that are exclusive to MUA1 can be skipped, since 3D heads aren't used in MUA1.

#### Other 3D Models (BoltOns, power models, map models)
All other models can be exported with any name. You will be asked for a file name during runtime. If the model uses cel shading, the cel shading model's name must end in "_outline" for igbFinisher to automatically recognize that the model has cel shading. Otherwise, it will be processed as though it doesn't have cel shading. If there is a version with cel shading, the version without cel shading should be exported with the name `fileName (No Cel).igb`; this will prevent the no cel model from overwriting the model with cel shading. The skin exporter of the Marvel Mods GIMP scripts can be used to get textures for these types of models. See the tables above for information on supported texture formats.

#### Conversation Portraits (HUDs)
All conversation portraits should be exported with the file name `hud_head_12301.igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

All texture formats from the conversation portrait (HUD) exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher. The next-gen and traditional styles are supported. Characters can use multiple portraits with different outline colors, and each will receive a unique file name.

#### Character Select Portraits (CSPs)
All character select portraits should be exported with the file name `123XX (Character Select Portrait).igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

All texture formats from the character select portrait portrait (CSP) exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher.

#### Power Icons
All power icons should be exported with the file name `power_icons.igb`. The internal name for the model should be the intended name of the resulting model, which should also be the same as the texture name. The name of the texture will be used for the name of the resulting file.

All texture formats from the power icons exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher.

#### Comic Covers
All comic covers should be exported with the file name `comic_cov.igb`. The internal name for the model should be the intended name of the resulting model, which should also be the same as the texture name. The name of the texture will be used for the name of the resulting file.

All texture formats from the comic cover exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher.

#### Loading Screens
All loading screens should be exported with the file name `123XX (Loading Screen).igb`. The internal name for the model should be "12301", regardless of the actual character number.

All texture formats from the loading screen exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher. 

### Asset Output
Assets that are the same for different games will be placed into folders together for convenience. Each folder will be labeled based on the game and console that it supports. The assets will be appropriately named, and will also be hex edited and Alchemy optimized if applicable.

## Development
Want to help develop igbFinisher? igbFinisher is developed with [Python 3](https://www.python.org/downloads/). There are several Python packages that you'll need to install:
1. [Pillow](https://pypi.org/project/pillow/)
2. [PyInstaller](https://pyinstaller.org/en/stable/)
3. [Questionary](https://pypi.org/project/questionary/)
4. [tkinterdnd2](https://pypi.org/project/tkinterdnd2/)