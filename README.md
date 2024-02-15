# igbFinisher
by BaconWizard17

## Description
This is a program to perform finishing operations on igb files to prepare them for release. It is specifically set up to work with the way that I do my releases.

### Prerequisites
1. [Alchemy 5](https://marvelmods.com/forum/index.php/topic,11158.0.html) must be installed
2. [XVI32 Hex Editor](http://www.chmaas.handshake.de/delphi/freeware/xvi32/xvi32.htm#installation)
3. [BaconWizard17's Marvel Mods GIMP Scripts](https://github.com/EthanReed517/BaconWizard17-MarvelMods-GIMP-Scripts/releases/latest) are needed when creating asssets.
4. [3ds Max 5 with Alchemy 2.5](https://marvelmods.com/forum/index.php/topic,10797.0.html) is needed to create assets.
 
### Installation
1. Download/install all prerequisites.
2. Download igbFinisher.
3. Extract it in a location of your choosing.
4. Within the `igbFinisher` folder, create a folder called `XVI32`. Install XVI32 there.

## Usage
1. Export an igb file to use with the finisher. See the section below titled "Asset Setup" for more information.
2. Set up `settings.ini` to work with the current character. See the section below titled "Settings.ini Setup" for more information.
3. Double click on `igbFinisher.exe`. Two windows will launch: a command window and the drag and drop UI.
4. The program will confirm that all settings are valid before it begins running.
5. Drag and drop the igb file into the drag and drop window.
   + Only one asset can be run through the igbFinisher at a time, but multiple console versions are created on each run.
6. If the igb file is named correctly, it will be automatically recognized by igbFinisher. If not, you'll be asked about the asset type.
7. Enter the path to the XML1/XML2 release folder for the current file.
8. Enter the path to the MUA1/MUA2 release folder for the current file.
9. You'll be asked several additional asset-specific questions, including the texture format.
10. The script will run the required processes on the skin, including hex editing and Alchemy operations, and then send the files to the appropriate destination folders. See the section below titled "Asset Output" for more information.
11. Once the asset is sucessfully exported, you'll get a completion message.
12. You can repeat the process for any additional igb files by simply dragging and dropping them onto the UI.
13. Once you're done, you can close the windows.

### Settings.ini Setup
`settings.ini` in the `igbFinisher` folder contains important settings that are used to run the finisher properly. Before running it, be sure to set up the values appropriately.

The following settings are used:
+ `xml1num`: The character's 2 or 3 digit character number for XML1. Fill with a number, or leave blank to skip exporting for XML1.
+ `xml2num`: The character's 2 or 3 digit character number for XML2. Fill with a number, or leave blank to skip exporting for XML2.
+ `mua1num`: The character's 2 or 3 digit character number for MUA1. Fill with a number, or leave blank to skip exporting for MUA1.
+ `mua2num`: The character's 2 or 3 digit character number for MUA2. Fill with a number, or leave blank to skip exporting for MUA2.
+ `pcOnly`: Whether or not you want to finish assets for only the PC or for all consoles. Can be `True` or `False`.
   + `True` will export assets for XML2 PC, MUA1 PC, and MUA1 Steam only.
   + `False` will export assets for all consoles.
+ `hexeditchoice`: Whether or not you want the assets to be hex edited when running. Can be `True` or `False`. 
  + `True` is recommended for assets that will be released.
  + `False` is recommended for testing.
+ `runalchemychoice`: Whether or not you want the assets to go through Alchemy optimizations when running. Can be `True` or `False`. 
  + `True` is recommended for assets that will be released.
  + `False` is recommended for testing.
+ `multipose`: Whether or not the character will have mannequins with multiple poses in their release.Can be `True` or `False`. 
  + `True` is for characters that will have multiple mannequins with different poses in thier release. When running, you'll be asked about a pose name, and the different mannequins will get unique names. Each mannequin pose for each console will have to be finished individually.
  + `False` is for characters that will only have one mannequin per console in their release and do not use multiple poses.

### Asset Setup
Because texture formats repeat across various consoles, one texture type can cover multiple different console versions. You can export a version of each texture format and run it through this program, and finished versions for multiple consoles will be created.

All assets must be exported with Alchemy 2.5 through 3ds Max 5 and should not have any post-processing done on them unless otherwise noted.

#### Skins
All skins should be exported with the console-compatible method. The default file name, `igActor01_Animation01DB.igb` should not be changed. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

All texture formats from the skin exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher, and each will yield assets based on the folder names of the exported texture. Select based on the primary texture for the skin. Any texture that's **only** for MUA1 Steam and/or PS3 can be skipped, because those assets can be created from the MUA1 PC/360 texture through Alchemy optimizations. Transparent textures are supported, but any transparency-specific post-processing (like converting igBlend to igAlpha) must be done prior to running the skin through igbFinisher. Environment maps that are set up within 3ds Max are also supported.

#### Mannequins
All mannequins should be exported with the file name `123XX (Mannequin).igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

All texture formats from the skin exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher, and each will yield assets based on the folder names of the exported texture. Select based on the primary texture for the mannequin. Any texture that's **only** for MUA1 Steam and/or PS3 can be skipped, because those assets can be created from the MUA1 PC/360 texture through Alchemy optimizations. Any texture format specific to XML1/XML2 can be skipped as well, since the XML games don't support mannequins. Transparent textures are supported, but any transparency-specific post-processing (like converting igBlend to igAlpha) must be done prior to running the mannequin through igbFinisher. Environment maps that are set up within 3ds Max are also supported.

Mannequins also support unique names for different poses. If you're releasing a skin with multiple mannequins in different poses, you can turn on this option and be able to select the pose name during runtime. When off, no pose name will be added. See the section above titled "Settings.ini Setup" for more information.

#### 3D Heads
All 3D Heads should be exported with the file name `123XX (3D Head).igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

All texture formats from the skin exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher, and each will yield assets based on the folder names of the exported texture. Select based on the primary texture for the mannequin. Any texture format specific to MUA1/MUA2 can be skipped, since the MUA games don't use 3D heads. Transparent textures are supported, but any transparency-specific post-processing (like converting igBlend to igAlpha) must be done prior to running the mannequin through igbFinisher. Environment maps that are set up within 3ds Max are also supported.

#### Conversation Portraits (HUDs)
All conversation portraits should be exported with the file name `hud_head_12301.igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

All texture formats from the conversation portrait (HUD) exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher. The next-gen and traditional styles are supported. Characters can use multiple portraits with different outline colors, and each will receive a unique file name.

#### Character Select Portraits (CSPs)
All character select portraits should be exported with the file name `123XX (Character Select Portrait).igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

All texture formats from the character select portrait portrait (CSP) exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher. 

#### Other Models
All other models can be exported with any name. You will be asked for a file name during runtime. The skin exporter of the Marvel Mods GIMP scripts can be used to get textures for other models.

All texture formats from the skin exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher, and each will yield assets based on the folder names of the exported texture. Select based on the primary texture for the model. Any texture that's **only** for MUA1 Steam and/or PS3 can be skipped, because those assets can be created from the MUA1 PC/360 texture through Alchemy optimizations. Transparent textures are supported, but any transparency-specific post-processing (like converting igBlend to igAlpha) must be done prior to running the model through igbFinisher. Environment maps that are set up within 3ds Max are also supported.

### Asset Output
Assets that are the same for different games will be placed into folders together for convenience. Each folder will be labeled based on the game and console that it supports. The assets will be appropriately named, and will also be hex edited and Alchemy optimized if selected and applicable.

## Development
Want to help develop igbFinisher? igbFinisher is developed with [Python 3](https://www.python.org/downloads/). There are several Python packages that you'll need to install:
1. [Pillow](https://pypi.org/project/pillow/)
2. [PyInstaller](https://pyinstaller.org/en/stable/)
3. [Questionary](https://pypi.org/project/questionary/)
4. [tkinterdnd2](https://pypi.org/project/tkinterdnd2/)