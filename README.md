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
10. Once the asset is sucessfully exported, you'll get a completion message.
11. You can repeat the process for any additional igb files by simply dragging and dropping them onto the UI.
12. Once you're done, you can close the windows.

### Settings.ini Setup
`settings.ini` in the `igbFinisher` folder contains important settings that are used to run the finisher properly. Before running it, be sure to set up the values appropriately.

The following settings are used:
+ `xml1num`: Can be `None` to skip exporting for XML1, `Ask` to ask each time the program runs, or a pre-populated 2 or 3 digit character number for XML1 to automatically process.
+ `xml2num`: Can be `None` to skip exporting for XML2, `Ask` to ask each time the program runs, or a pre-populated 2 or 3 digit character number for XML2 to automatically process.
+ `mua1num`: Can be `None` to skip exporting for MUA1, `Ask` to ask each time the program runs, or a pre-populated 2 or 3 digit character number for MUA1 to automatically process.
+ `mua2num`: Can be `None` to skip exporting for MUA1, `Ask` to ask each time the program runs, or a pre-populated 2 or 3 digit character number for MUA1 to automatically process.
+ `xmlpath`: Can be `None` to skip exporting for XML1 and XML2, `Ask` to ask each time the program runs, or a pre-populated file path for the XML1/XML2 release to automatically process.
   + If both `xml1num` and `xml2num` are set to `Num`, exporting will be skipped anyways.
+ `muapath`: Can be `None` to skip exporting for MUA1 and MUA2, `Ask` to ask each time the program runs, or a pre-populated file path for the MUA1/MUA2 release to automatically process.
   + If both `mua1num` and `mua2num` are set to `Num`, exporting will be skipped anyways.
+ `pcOnly`: Whether or not you want to finish assets for only the PC or for all consoles. Can be `True` or `False`.
   + `True` will export assets for XML2 PC, MUA1 PC, and MUA1 Steam only.
   + `False` will export assets for all consoles.

### Asset Setup
Because texture formats repeat across various consoles, one texture type can cover multiple different console versions. You can export a version of each texture format and run it through this program, and finished versions for multiple consoles will be created.

All assets must be exported with Alchemy 2.5 through 3ds Max 5 and should not have any post-processing done on them unless otherwise noted.

#### Skins
All skins should be exported with the console-compatible method. The default file name, `igActor01_Animation01DB.igb` should not be changed. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number. If the skin uses cel shading, the cel shading model's name must end in "_outline" for igbFinisher to automatically recognize that the model has cel shading. Otherwise, it will be processed as though it doesn't have cel shading.

All texture formats from the skin exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher, and each will yield assets based on the folder names of the exported texture. However, the PSP textures should use PNG8 compression. PNG4, DXT3, and DXT5 are not supported. Any texture that's **only** for MUA1 Steam and/or PS3 can be skipped, because those assets can be created from the MUA1 PC/360 texture through Alchemy optimizations. Transparent textures are supported, but any transparency-specific post-processing (like converting igBlend to igAlpha) must be done prior to running the skin through igbFinisher. Environment maps that are set up within 3ds Max are also supported. 
   + If mixing regular opaque diffuse textures, transparent diffuse textures, and/or environment maps, only one folder for each texture type must be used, and they must be compatible. The compatibility will be based on the folder with the least compatibility. Some examples:
	 + Opaque diffuse with transparent diffuse example: `PC, PS2, Xbox, and MUA1 360` for the opaque diffuse texture, `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` for the transparent diffuse texture.
     + Opaque diffuse with environment maps example: `PC, PS2, Xbox, and MUA1 360` for the diffuse texture, `PC and MUA1 360` for the environment maps.
	 + Transparent diffuse with environment maps example: `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` for the transparent diffuse texture, `PC and MUA1 360` for the environment maps.
	 + Opaque diffuse, transparent diffuse, and environment maps together: `PC, PS2, Xbox, and MUA1 360` for the opaque diffuse texture, `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` for the transparent diffuse texture, `PC and MUA1 360` for the environment maps.

#### Mannequins
All mannequins should be exported with the file name `123XX (Mannequin).igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number. If you want to have a custom pose name for your mannequin (for example, "OCP Pose"), you can export it with the name `123XX (Mannequin - OCP Pose).igb`, and the resulting file will have that pose name in its name.

All texture formats from the skin exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher, and each will yield assets based on the folder names of the exported texture. However, the PSP textures should use PNG8 compression. PNG4, DXT3, and DXT5 are not supported. Any texture that's **only** for MUA1 Steam and/or PS3 can be skipped, because those assets can be created from the MUA1 PC/360 texture through Alchemy optimizations. Any texture format specific to XML1/XML2 can be skipped as well, since the XML games don't support mannequins. Transparent textures are supported, but any transparency-specific post-processing (like converting igBlend to igAlpha) must be done prior to running the mannequin through igbFinisher. Environment maps that are set up within 3ds Max are also supported.
   + If mixing regular opaque diffuse textures, transparent diffuse textures, and/or environment maps, only one folder for each texture type must be used, and they must be compatible. The compatibility will be based on the folder with the least compatibility. Some examples:
	 + Opaque diffuse with transparent diffuse example: `PC, PS2, Xbox, and MUA1 360` for the opaque diffuse texture, `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` for the transparent diffuse texture.
     + Opaque diffuse with environment maps example: `PC, PS2, Xbox, and MUA1 360` for the diffuse texture, `PC and MUA1 360` for the environment maps.
	 + Transparent diffuse with environment maps example: `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` for the transparent diffuse texture, `PC and MUA1 360` for the environment maps.
	 + Opaque diffuse, transparent diffuse, and environment maps together: `PC, PS2, Xbox, and MUA1 360` for the opaque diffuse texture, `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` for the transparent diffuse texture, `PC and MUA1 360` for the environment maps.

#### 3D Heads
All 3D Heads should be exported with the file name `123XX (3D Head).igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

All texture formats from the skin exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher, and each will yield assets based on the folder names of the exported texture. However, the PSP textures should use PNG8 compression. PNG4, DXT3, and DXT5 are not supported. Any texture format specific to MUA1/MUA2 can be skipped, since the MUA games don't use 3D heads. Transparent textures are supported, but any transparency-specific post-processing (like converting igBlend to igAlpha) must be done prior to running the mannequin through igbFinisher. Environment maps that are set up within 3ds Max are also supported.
   + If mixing regular opaque diffuse textures, transparent diffuse textures, and/or environment maps, only one folder for each texture type must be used, and they must be compatible. The compatibility will be based on the folder with the least compatibility. Some examples:
	 + Opaque diffuse with transparent diffuse example: `PC, PS2, Xbox, and MUA1 360` for the opaque diffuse texture, `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` for the transparent diffuse texture.
     + Opaque diffuse with environment maps example: `PC, PS2, Xbox, and MUA1 360` for the diffuse texture, `PC and MUA1 360` for the environment maps.
	 + Transparent diffuse with environment maps example: `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` for the transparent diffuse texture, `PC and MUA1 360` for the environment maps.
	 + Opaque diffuse, transparent diffuse, and environment maps together: `PC, PS2, Xbox, and MUA1 360` for the opaque diffuse texture, `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` for the transparent diffuse texture, `PC and MUA1 360` for the environment maps.

#### Conversation Portraits (HUDs)
All conversation portraits should be exported with the file name `hud_head_12301.igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

All texture formats from the conversation portrait (HUD) exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher. The next-gen and traditional styles are supported. Characters can use multiple portraits with different outline colors, and each will receive a unique file name.

#### Character Select Portraits (CSPs)
All character select portraits should be exported with the file name `123XX (Character Select Portrait).igb`. The internal numbers for model portions should use the skin number "12301," regardless of the actual skin number.

All texture formats from the character select portrait portrait (CSP) exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher. 

#### Other Models (BoltOns, power models, map models)
All other models can be exported with any name. You will be asked for a file name during runtime. If the skin uses cel shading, the cel shading model's name must end in "_outline" for igbFinisher to automatically recognize that the model has cel shading. Otherwise, it will be processed as though it doesn't have cel shading. If there is a version with cel shading, the version without cel shading should be exported with the name `fileName (No Cel).igb`; this will prevent the no cel model from overwriting the model with cel shading. The skin exporter of the Marvel Mods GIMP scripts can be used to get textures for other models.

All texture formats from the skin exporter of the Marvel Mods GIMP Scripts are compatible with igbFinisher, and each will yield assets based on the folder names of the exported texture. However, the PSP textures should use PNG8 compression. PNG4, DXT3, and DXT5 are not supported. Any texture that's **only** for MUA1 Steam and/or PS3 can be skipped, because those assets can be created from the MUA1 PC/360 texture through Alchemy optimizations. Transparent textures are supported, but any transparency-specific post-processing (like converting igBlend to igAlpha) must be done prior to running the model through igbFinisher. Environment maps that are set up within 3ds Max are also supported.
   + If mixing regular opaque diffuse textures, transparent diffuse textures, and/or environment maps, only one folder for each texture type must be used, and they must be compatible. The compatibility will be based on the folder with the least compatibility. Some examples:
	 + Opaque diffuse with transparent diffuse example: `PC, PS2, Xbox, and MUA1 360` for the opaque diffuse texture, `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` for the transparent diffuse texture.
     + Opaque diffuse with environment maps example: `PC, PS2, Xbox, and MUA1 360` for the diffuse texture, `PC and MUA1 360` for the environment maps.
	 + Transparent diffuse with environment maps example: `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` for the transparent diffuse texture, `PC and MUA1 360` for the environment maps.
	 + Opaque diffuse, transparent diffuse, and environment maps together: `PC, PS2, Xbox, and MUA1 360` for the opaque diffuse texture, `PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360` for the transparent diffuse texture, `PC and MUA1 360` for the environment maps.

### Asset Output
Assets that are the same for different games will be placed into folders together for convenience. Each folder will be labeled based on the game and console that it supports. The assets will be appropriately named, and will also be hex edited and Alchemy optimized if applicable.

## Development
Want to help develop igbFinisher? igbFinisher is developed with [Python 3](https://www.python.org/downloads/). There are several Python packages that you'll need to install:
1. [Pillow](https://pypi.org/project/pillow/)
2. [PyInstaller](https://pyinstaller.org/en/stable/)
3. [Questionary](https://pypi.org/project/questionary/)
4. [tkinterdnd2](https://pypi.org/project/tkinterdnd2/)