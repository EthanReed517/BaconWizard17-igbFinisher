# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Modules from this program
import alchemy
import globalVars
import hex
import questions
# Other modules
from shutil import copy
from os import makedirs, rename, remove
import os.path
from configparser import ConfigParser


# ######### #
# FUNCTIONS #
# ######### #
# Define the function to get local resources
def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    # Return the collected value
    return os.path.join(base_path, relative_path)

# Define the function for updating the path for XML2 PSP optimizations
def updateXML2PSPOptPath():
    # Get the file path to the secondary alchemy optimization
    skin2_2Path = resource_path("Scripts\\skin2-2.ini")
    # Prepare to parse the optimization
    config = ConfigParser()
    # Make the config parser case sensitive
    config.optionxform=str
    # Read the optimization
    config.read("Scripts/skin2-1.ini")
    # Get the path
    savedPath = config["OPTIMIZATION1"]["fileName"]
    # Determine if the path matches
    if not(savedPath == skin2_2Path):
        # The paths do not match
        # Update the path in the optimization
        config["OPTIMIZATION1"]["fileName"] = skin2_2Path
    # Write the new path to the optimization
    with open("Scripts/skin2-1.ini", "w") as configfile:
        config.write(configfile)

# Define the function for sending a file
def processFile(sourceFileName, assetType, num, file, path, folder, optList):
    # Verify that something needs to be done
    if ((num is not None) and (file is not None) and (path is not None)):
        # Make the destination folder if needed
        makedirs(os.path.join(path, folder), exist_ok=True)
        # Create a temporary copy of the file
        tempFile = os.path.join(os.path.dirname(sourceFileName), "temp.igb")
        copy(sourceFileName, tempFile)
        # Hex edit the file
        hex.hexEdit2(tempFile, num, assetType)
        # Run the Alchemy operations if needed
        if optList is not None:
            for optimization in optList:
                alchemy.callAlchemy(tempFile, optimization)
        # Copy the file and then remove the temp file (can't move by renaming because the destination could exist)
        copy(tempFile, os.path.join(path, folder, file))
        remove(tempFile)

# Define the function for sending Wii files
def processWiiFiles(sourceFileName, assetType, nums, files, path):
    # Determine if the MUA1 and MUA2 files have the same name
    if files["MUA1"] == files["MUA2"]:
        # The files are the same, so copy to one folder
        processFile(sourceFileName, nums["MUA1"], assetType, files["MUA1"], path, "for MUA1 (Wii) and MUA2 (Wii)", None)
    else:
        # The files are not the same, so copy to two folders
        processFile(sourceFileName, nums["MUA1"], assetType, files["MUA1"], path, "for MUA1 (Wii)", None)
        processFile(sourceFileName, nums["MUA1"], assetType, files["MUA2"], path, "for MUA2 (Wii)", None)

# Define the function for sending PSP files
def processPSPFiles(sourceFileName, assetType, nums, files, paths, prefix):
    # Determine if this is a skin. XML2 PSP skins need special consideration
    if prefix == "skin":
        # This is a skin, so check if XML2 PSP skins are allowed
        if globalVars.allowXML2PSPSkin == True:
            # This is allowed, so process it
            # Check if this is the file without cel shading, which is the only one used in XML2 PSP
            if "No Cel" in files["XML2"]:
                # This is without cel shading
                # The name should not mention that this is without cel shading, since XML2 PSP doesn't use cel shading
                outName = files["XML2"].replace(" - No Cel", "")
                # Update the Alchemy optimization to reference the correct file path
                updateXML2PSPOptPath()
                # Process the file
                processFile(sourceFileName, nums["XML2"], assetType, outName, paths["XML"], "for XML2 (PSP)", ["skin2-1.ini"])
    else:
        # This is not a skin, so process the XML2 file
        processFile(sourceFileName, nums["XML2"], assetType, files["XML2"], paths["XML"], "for XML2 (PSP)", None)
    # MUA1 and MUA2 are processed the same way no matter what
    if files["MUA1"] == files["MUA2"]:
        # The files are the same, so copy to one folder
        processFile(sourceFileName, nums["MUA1"], assetType, files["MUA1"], paths["MUA"], "for MUA1 (PSP) and MUA2 (PSP)", [f"{prefix}3.ini"])
    else:
        # The files are not the same, so copy to two folders
        processFile(sourceFileName, nums["MUA1"], assetType, files["MUA1"], paths["MUA"], "for MUA1 (PSP)", [f"{prefix}3.ini"])
        processFile(sourceFileName, nums["MUA2"], assetType, files["MUA2"], paths["MUA"], "for MUA2 (PSP)", [f"{prefix}3.ini"])

# Define the function for processing files with no textures
def processNoTexFile(sourceFileName, assetType, nums, files, paths, prefix):
    # Set up the list of folder options
    folderOptions = ["Like a model with a 256x256 or less texture", "Like a model with a larger than 256x256 texture", "Using as few folders as possible"]
    # Determine how the user wants to process the file
    folderOption = questions.select("What folder structure should be used?", folderOptions)
    # Determine what the user picked
    if folderOption == folderOptions[0]:
        # Send out like a model with a 256x256 or less texture
        processFile(sourceFileName, nums["XML1"], assetType, files["XML1"], paths["XML"], "for XML1 (GC)", None)
        processFile(sourceFileName, nums["XML1"], assetType, files["XML1"], paths["XML"], "for XML1 (PS2 and Xbox)", None)
        processFile(sourceFileName, nums["XML2"], assetType, files["XML2"], paths["XML"], "for XML2 (GC)", None)
        processFile(sourceFileName, nums["XML2"], assetType, files["XML2"], paths["XML"], "for XML2 (PC, PS2, and Xbox)", None)
        processPSPFiles(sourceFileName, nums, assetType, files, paths, prefix)
        processFile(sourceFileName, nums["MUA1"], assetType, files["MUA1"], paths["MUA"], "for MUA1 (PS2 and Xbox)", None)
        processWiiFiles(sourceFileName, nums, assetType, files, paths["MUA"])
        processFile(sourceFileName, nums["MUA1"], assetType, files["MUA1"], paths["MUA"], "for MUA1 (PC and 360)", [f"{prefix}1-1.ini"])
        processFile(sourceFileName, nums["MUA1"], assetType, files["MUA1"], paths["MUA"], "for MUA1 (Steam and PS3)", [f"{iniPrefix}1-1.ini"])
        processFile(sourceFileName, nums["MUA2"], assetType, files["MUA2"], paths["MUA"], "for MUA2 (PS2)", [f"{prefix}3.ini"])
    elif folderOption == folderOptions[1]:
        # Send out like a model with a larger than 256x256 texture
        processFile(sourceFileName, nums["XML1"], assetType, files["XML1"], paths["XML"], "for XML1 (GC)", None)
        processFile(sourceFileName, nums["XML1"], assetType, files["XML1"], paths["XML"], "for XML1 (PS2)", None)
        processFile(sourceFileName, nums["XML1"], assetType, files["XML1"], paths["XML"], "for XML1 (Xbox)", None)
        processFile(sourceFileName, nums["XML2"], assetType, files["XML2"], paths["XML"], "for XML2 (GC)", None)
        processFile(sourceFileName, nums["XML2"], assetType, files["XML2"], paths["XML"], "for XML2 (PS2)", None)
        processFile(sourceFileName, nums["XML2"], assetType, files["XML2"], paths["XML"], "for XML2 (PC and Xbox)", None)
        processPSPFiles(sourceFileName, nums, assetType, files, paths, prefix)
        processFile(sourceFileName, nums["MUA1"], assetType, files["MUA1"], paths["MUA"], "for MUA1 (PS2)", None)
        processFile(sourceFileName, nums["MUA1"], assetType, files["MUA1"], paths["MUA"], "for MUA1 (Xbox)", None)
        processWiiFiles(sourceFileName, nums, assetType, files, paths["MUA"])
        processFile(sourceFileName, nums["MUA1"], assetType, files["MUA1"], paths["MUA"], "for MUA1 (PC, Steam, PS3, and 360)", [f"{prefix}1-1.ini"])
        processFile(sourceFileName, nums["MUA2"], assetType, files["MUA2"], paths["MUA"], "for MUA2 (PS2)", [f"{prefix}3.ini"])
    else:
        # Send to as few folders as possible
        processFile(sourceFileName, nums["XML1"], assetType, files["XML1"], paths["XML"], "for XML1 (GC, PS2, and Xbox)", None)
        processFile(sourceFileName, nums["XML2"], assetType, files["XML2"], paths["XML"], "for XML2 (PC, GC, PS2, and Xbox)", None)
        processPSPFiles(sourceFileName, nums, assetType, files, paths, prefix)
        processFile(sourceFileName, nums["MUA1"], assetType, files["MUA1"], paths["MUA"], "for MUA1 (PS2 and Xbox)", None)
        processWiiFiles(sourceFileName, nums, assetType, files, paths["MUA"])
        processFile(sourceFileName, nums["MUA1"], assetType, files["MUA1"], paths["MUA"], "for MUA1 (PC, Steam, PS3, and 360)", [f"{prefix}1-1.ini"])
        processFile(sourceFileName, nums["MUA2"], assetType, files["MUA2"], paths["MUA"], "for MUA2 (PS2)", [f"{prefix}3.ini"])

# Define the function for processing assets
def process3D(assetType, sourceFileName, textureFormat, numsDict, nameDict, pathDict):
    # Determine the asset type
    if assetType == "Skin":
        # This is a skin
        # Set the ini prefix
        iniPrefix = "skin"
    else:
        # Not a skin
        # Set the ini prefix
        iniPrefix = "stat"
    # Set up the dictionary of necessary operations for each texture type
    processDict = {
        # No texture type
        "No Texture": [
            {"function": processNoTexFile, "kwargs": {"nums": numsDict, "assetType": assetType, "files": nameDict, "paths": pathDict, "prefix": iniPrefix}}
        ],
        # Single texture type, PNG8 format, all consoles
        "PC, PS2, Xbox, and MUA1 360": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2 and Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC, PS2, and Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2 and Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and 360)", "optList": [f"{iniPrefix}1-1.ini"]}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam and PS3)", "optList": [f"{iniPrefix}1-1.ini", f"{iniPrefix}1-2.ini"]}}
        ],
        "PC, Xbox, and MUA1 360": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC and Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and 360)", "optList": [f"{iniPrefix}1-1.ini"]}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam and PS3)", "optList": [f"{iniPrefix}1-1.ini", f"{iniPrefix}1-2.ini"]}}
        ],
        "PS2": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2)", "optList": None}}
        ],
        "GameCube, PSP, and MUA2 PS2": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}},
            {"function": processPSPFiles, "kwargs": {"nums": numsDict, "files": nameDict, "paths": pathDict, "prefix": iniPrefix}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA2"], "file": nameDict["MUA2"], "path": pathDict["MUA"], "folder": "for MUA2 (PS2)", "optList": [f"{iniPrefix}3.ini"]}}
        ],
        # Single texture type, PNG8 format, PC only
        "PC": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC)", "optList": [f"{iniPrefix}1-1.ini"]}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam)", "optList": [f"{iniPrefix}1-1.ini", f"{iniPrefix}1-2.ini"]}}
        ],
        # Single texture type, DXT1 format, all consoles
        "MUA1 PC, Steam, 360, and PS3": [
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC, Steam, PS3 and 360)", "optList": [f"{iniPrefix}1-1.ini"]}}
        ],
        "XML2 PC, Xbox, and Wii": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC and Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox and Wii)", "optList": None}}
        ],
        "Wii": [
            {"function": processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        # Single texture type, DXT1 format, PC only
        "MUA1 PC and Steam": [
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and Steam)", "optList": [f"{iniPrefix}1-1.ini"]}}
        ],
        "XML2 PC": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        # Single texture type, plain PNG format, all consoles ("PS2" and "GameCube, PSP, and MUA2 PSP" already covered earlier)
        "PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2 and Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC, PS2, and Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2 and Xbox)", "optList": None}},
            {"function": processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and 360)", "optList": [f"{iniPrefix}1-1.ini"]}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam and PS3)", "optList": [f"{iniPrefix}1-1.ini"]}}
        ],
        "PC, Xbox, Wii, MUA1 Steam, PS3, and 360": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC and Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}},
            {"function": processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and 360)", "optList": [f"{iniPrefix}1-1.ini"]}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam and PS3)", "optList": [f"{iniPrefix}1-1.ini"]}}
        ],
        # Single texture type, plain PNG format, PC only
        "PC and MUA1 Steam": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and Steam)", "optList": [f"{iniPrefix}1-1.ini"]}}
        ],
        # Single texture type with environment maps, PNG8 format, all consoles
        "Main texture: PC, PS2, Xbox, and MUA1 360 / Environment texture: PC and MUA1 360": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        "Main texture: PC, PS2, Xbox, and MUA1 360 / Environment texture: Xbox": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}}
        ],
        "Main texture: PC, PS2, Xbox, and MUA1 360 / Environment texture: PS2": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2)", "optList": None}}
        ],
        "Main texture: PC, Xbox, and MUA1 360 / Environment texture: PC and MUA1 360": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        "Main texture: PC, Xbox, and MUA1 360 / Environment texture: Xbox": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}}
        ],
        "Main texture: PC and MUA1 360 / Environment texture: PC and MUA1 360": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}}
        ],
        "Main texture: Xbox / Environment texture: Xbox": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}}
        ],
        "Main texture: PS2 / Environment texture: PS2": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2)", "optList": None}}
        ],
        "Main texture: GameCube, PSP, and MUA2 PS2 / Environment texture: GameCube, PSP, and MUA2 PS2": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}},
            {"function": processPSPFiles, "kwargs": {"nums": numsDict, "files": nameDict, "paths": pathDict, "prefix": iniPrefix}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA2"], "file": nameDict["MUA2"], "path": pathDict["MUA"], "folder": "for MUA2 (PS2)", "optList": [f"{iniPrefix}3.ini"]}}
        ],
        # Single texture type with environment maps, PNG8, PC only
        "Main texture: PC / Environment texture: PC": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        # Single texture type with environment maps, DXT1 Format, all consoles
        "Main texture: XML2 PC, Xbox, and Wii / Environment texture: XML2 PC": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        "Main texture: XML2 PC, Xbox, and Wii / Environment texture: Xbox and Wii": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}},
            {"function": processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        "Main texture: Wii / Environment texture: Wii": [
            {"function": processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        "Main texture: Wii / Environment texture: Xbox and Wii": [
            {"function": processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        # Single texture type with environment maps, DXT1, PC only
        "Main texture: XML2 PC / Environment texture: XML2 PC": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        # Transparent texture with PNG8 environment maps, all consoles
        "Main texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment texture: PC and MUA1 360": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        "Main texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment texture: Xbox": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}}
        ],
        "Main texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment texture: PS2": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2)", "optList": None}}
        ],
        "Main texture: PC, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment texture: PC and MUA1 360": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        "Main texture: PC, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment texture: Xbox": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}}
        ],
        # Transparent texture with PNG8 environment maps, PC only
        "Main texture: PC and MUA1 Steam / Environment texture: PC": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        # Transparent texture with DXT1 environment maps, all consoles
        "Main texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment texture: XML2 PC": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        "Main texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment texture: Xbox and Wii": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}},
            {"function": processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        "Main texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment texture: Wii": [
            {"function": processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        "Main texture: PC, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment texture: XML2 PC": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        "Main texture: PC, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment texture: Xbox and Wii": [
            {"function": processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}},
            {"function": processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}},
            {"function": processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        "Main texture: PC, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment texture: Wii": [
            {"function": processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        # Transparent texture with DXT1 environment maps, PC only
        "Main texture: PC and MUA1 Steam / Environment texture: XML2 PC": [
            {"function": processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ]
    }
    # Start a variable that assumes completion
    complete = True
    # Attempt to process
    try:
        # Loop through the possible files for the selected texture format
        for file in processDict[textureFormat]:
            # Process the file using its necessary function and arguments
            file["function"](sourceFileName, assetType, **file["kwargs"])
    except KeyError:
        # The selected texture format doesn't have an entry in the dictionary
        # Print an error
        questions.printError(f"Choice of texture format did not line up with an existing operation. Selected texture format: {textureFormat}", True)
        # Update the completion variable to indicate that nothing was processed
        complete = False
    # Return whether or not the processing was successfully completed
    return complete