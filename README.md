# igbFinisher
by BaconWizard17

## Description
This is a program to perform finishing operations on igb files to prepare them for release. It is specifically set up to work with the way that I do my releases.

### Prerequisites
1. [Python 3](https://www.python.org/downloads/)
2. [Alchemy 5](https://marvelmods.com/forum/index.php/topic,11158.0.html)
3. [XVI32 Hex Editor](http://www.chmaas.handshake.de/delphi/freeware/xvi32/xvi32.htm#installation)
4. [Questionary for Python](https://pypi.org/project/questionary/)
5. [BaconWizard17's Marvel Mods GIMP Scripts](https://github.com/EthanReed517/BaconWizard17-MarvelMods-Gimp-Scripts/releases/latest) are needed when creating asssets.
6. [3ds Max 5 with Alchemy 2.5](https://marvelmods.com/forum/index.php/topic,10797.0.html) is needed to create assets.
 
### Installation
1. Download/install all prerequisites.
2. Download igbFinisher.
3. Extract it in a location of your choosing.
4. Within the `igbFinisher` folder, create a folder called `XVI32`. Install XVI32 there.
5. Install all other prerequisite programs per their installation instructions.
 
## Usage
1. Export an igb file to use with the finisher. See the section below titled "Asset Setup" for more information.
2. Copy the igb file into the `igbFinisher` folder.
   + Only one asset can be run through the igbFinisher at a time, but multiple console versions are created on each run.
3. Set up `settings.ini` to work with the current character. See the section below titled "Settings.ini Setup" for more information.
4. Double click on `igbFinisher.bat` to run the program.
5. The program will confirm that `settings.ini` exists and is valid.
6. Enter the path to the XML1/XML2 release folder for the current file.
7. Enter the path to the MUA1/MUA2 release folder for the current file.
8. Select the asset that you're finishing.
9. Answer the remaining asset-specific questions, such as which texture format was selected.
10. The script will run the required processes on the skin, including hex editing and Alchemy operations, and then send the files to the appropriate destination folders. See the section below titled "Asset Output" for more information.
11. Press any key to close the window.

### Asset Setup
Because texture formats repeat across various consoles, one texture type can cover multiple different console versions. You can export a version of each texture format and run it through this program, and finished versions for multiple consoles will be created.

#### Skins
All skins should be exported with the console-compatible method. The default file name, `igActor01_Animation01DB.igb` should not be changed. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

The following texture options are possible when exporting with BaconWizard17's Marvel Mods GIMP Scripts (textures with transparency are not currently supported):
+ Original texture size 256x256 or less
  +  Primary Skin
     +  **PC, PS2, Xbox, and MUA1 360**: Used for the PC versions of XML2 and MUA1, PS2 and Xbox versions of XML1, XML2, and MUA1, and Xbox 360 version of MUA1.
     +  **Wii**: Used for the Wii versions of MUA1 and MUA2.
     +  **GameCube, PSP, and MUA2 PS2**: Used for the GameCube versions of XML1 and XML2, PSP versions of MUA1 and MUA2, and PS2 version of MUA2.
  +  Secondary Skin
     +  **PC Xbox, and MUA1 360**: Used for the PC versions of XML2 and MUA1, Xbox versions of XML1, XML2, and MUA1, and Xbox 360 version of MUA1.
     +  **Wii**: Used for the Wii versions of MUA1 and MUA2.
     +  **PS2**: Used for the PS2 versions of XML1, XML2, and MUA1.
     +  **GameCube, PSP, and MUA2 PS2**: Used for the GameCube versions of XML1 and XML2, PSP versions of MUA1 and MUA2, and PS2 version of MUA2.
+  Original texture size over 256x256
   +  **MUA1 PC, Steam, 360, and PS3**: Used for the PC, Steam, Xbox 360, and PS3 versions of MUA1.
   +  **XML2 PC, Xbox, and Wii**: Used for the PC version of XML2, Xbox versions of XML1, XML2, and MUA1, and Wii versions of MUA1 and MUA2.
   +  **PS2**: Used for the PS2 versions of XML1, XML2, and MUA1.
   +  **GameCube, PSP, and MUA2 PS2**: Used for the GameCube versions of XML1 and XML2, PSP versions of MUA1 and MUA2, and PS2 version of MUA2.

#### Mannequins
All mannequins should be exported with the file name `123XX (Mannequin).igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

The following texture options are possible when exporting with BaconWizard17's Marvel Mods GIMP Scripts (textures with transparency are not currently supported):
+ Original texture size 256x256 or less
  +  **PC, PS2, Xbox, and MUA1 360**: Used for the PC, PS2, Xbox, and Xbox 360 versions of MUA1.
  +  **Wii**: Used for the Wii versions of MUA1 and MUA2.
  +  **GameCube, PSP, and MUA2 PS2**: Used for the PSP versions of MUA1 and MUA2, and PS2 version of MUA2.
+  Original texture size over 256x256
   +  **MUA1 PC, Steam, 360, and PS3**: Used for the PC, Steam, Xbox 360, and PS3 versions of MUA1.
   +  **XML2 PC, Xbox, and Wii**: Used for the Xbox version of MUA1 and Wii versions of MUA1 and MUA2.
   +  **PS2**: Used for the PS2 version of MUA1.
   +  **GameCube, PSP, and MUA2 PS2**: Used for the PSP versions of MUA1 and MUA2, and PS2 version of MUA2.

#### 3D Heads
All 3D Heads should be exported with the file name `123XX (3D Head).igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

The following texture options are possible when exporting with BaconWizard17's Marvel Mods GIMP Scripts (textures with transparency are not currently supported):
+ Original texture size 256x256 or less
  +  **PC, PS2, Xbox, and MUA1 360**: Used for the PC version of XML2, and PS2 and Xbox versions of XML1 and XML2.
  +  **GameCube, PSP, and MUA2 PS2**: Used for the GameCube versions of XML1 and XML2.
+  Original texture size over 256x256
   +  **XML2 PC, Xbox, and Wii**: Used for the PC version of XML2 and the Xbox versions of XML1 and XML2.
   +  **PS2**: Used for the PS2 versions of XML1 and XML2.
   +  **GameCube, PSP, and MUA2 PS2**: Used for the GameCube versions of XML1 and XML2.

#### Conversation Portraits (HUDs)
All conversation portraits should be exported with the file name `hud_head_12301.igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

The following texture options are possible when exporting with BaconWizard17's Marvel Mods GIMP Scripts (textures with transparency are not currently supported):
+ TBD

#### Character Select Portraits (CSPs)
All character select portraits should be exported with the file name `123XX (Character Select Portrait).igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

The following texture options are possible when exporting with BaconWizard17's Marvel Mods GIMP Scripts (textures with transparency are not currently supported):
+ TBD

#### Other Models
All other models can be exported with any name. You will be asked for a file name during runtime.

The following texture options are possible when exporting with BaconWizard17's Marvel Mods GIMP Scripts (textures with transparency are not currently supported):
+ Original texture size 256x256 or less
   +  **PC, PS2, Xbox, and MUA1 360**: Used for the PC versions of XML2 and MUA1, PS2 and Xbox versions of XML1, XML2, and MUA1, and Xbox 360 version of MUA1.
   +  **Wii**: Used for the Wii versions of MUA1 and MUA2.
   +  **GameCube, PSP, and MUA2 PS2**: Used for the GameCube versions of XML1 and XML2, PSP versions of MUA1 and MUA2, and PS2 version of MUA2.
+  Original texture size over 256x256
   +  **MUA1 PC, Steam, 360, and PS3**: Used for the PC, Steam, Xbox 360, and PS3 versions of MUA1.
   +  **XML2 PC, Xbox, and Wii**: Used for the PC version of XML2, Xbox versions of XML1, XML2, and MUA1, and Wii versions of MUA1 and MUA2.
   +  **PS2**: Used for the PS2 versions of XML1, XML2, and MUA1.
   +  **GameCube, PSP, and MUA2 PS2**: Used for the GameCube versions of XML1 and XML2, PSP versions of MUA1 and MUA2, and PS2 version of MUA2.

### Settings.ini Setup
`settings.ini` in the `igbFinisher` folder contains important settings that are used to run the finisher properly. Before running it, be sure to set up the values appropriately.

The following settings are used:
+ `xml1num`: The character's 2 or 3 digit character number for XML1. Fill with a number or leave blank to skip exporting for XML1.
+ `xml2num`: The character's 2 or 3 digit character number for XML2. Fill with a number or leave blank to skip exporting for XML2.
+ `mua1num`: The character's 2 or 3 digit character number for MUA1. Fill with a number or leave blank to skip exporting for MUA1.
+ `mua2num`: The character's 2 or 3 digit character number for MUA2. Fill with a number or leave blank to skip exporting for MUA2.
+ `hexeditchoice`: Whether or not you want the assets to be hex edited when running. Can be `True` or `False`. 
  + `True` is recommended for assets that will be released.
  + `False` is recommended for testing.
+ `runalchemychoice`: Whether or not you want the assets to go through Alchemy optimizations when running. Can be `True` or `False`. 
  + `True` is recommended for assets that will be released.
  + `False` is recommended for testing.
+ `multipose`: Whether or not the character will have mannequins with multiple poses in their release.Can be `True` or `False`. 
  + `True` is for characters that will have multiple mannequins with different poses in thier release. When running, you'll be asked about a pose name, and the different mannequins will get unique names. Each mannequin pose for each console will have to be finished individually.
  + `False` is for characters that will only have one mannequin per console in their release and do not use multiple poses.

### Asset Output
Assets that are the same for different games will be placed into folders together for convenience.