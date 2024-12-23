# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import hex
# External modules
from shutil import copy
from os import makedirs, remove
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