# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import common
import hex
import processing
import questions
import textures
# External modules
import os.path
from os import remove
from shutil import copy


# ######### #
# FUNCTIONS #
# ######### #
# Define the function for getting the file names
def getFileNamesAndNumbers(settings, fullFileName, textureFormat, fileName):
    # Initialize a list of names
    nameList = []
    # Cycle through the list of games
    for game in ["XML1", "XML2", "MUA1", "MUA2"]:
        # Determine if the game is in use
        if settings[f"{game}Num"] is not None:
            # The game is in use
            # Determine if the texture format reflects this name
            if textureFormat.split(" ")[0] == game:
                # The texture format reflects the game
                # Set the game-specific name
                nameList.append(f"{fileName}.igb")
            else:
                # The texture format doesn't reflect the game
                # Set no name
                nameList.append(None)
        else:
            # The game is not not in use
            # Set no name
            nameList.append(None)
    # Break out the list into the specific variables
    XML1Name = nameList[0]
    XML2Name = nameList[1]
    MUA1Name = nameList[2]
    MUA2Name = nameList[3]
    # Return the collected values
    return (XML1Name, XML2Name, MUA1Name, MUA2Name)

# Define the function to export the portraits
def processIcons(assetType, sourceFileName, textureFormat, numsDict, nameDict, pathDict):
    # Set up the dictionary of necessary operations for each texture type
    processDict = {
        # Plain PNG, all consoles
        "MUA1 PC, Steam, PS3, and 360": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC, Steam, PS3, and 360)", "optList": ["stat1-1.ini"]}}
        ],
        "MUA1 Wii and Xbox": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Wii and Xbox)", "optList": None}}
        ],
        "MUA2 Wii": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA2"], "file": nameDict["MUA2"], "path": pathDict["MUA"], "folder": "for MUA2 (Wii)", "optList": None}}
        ],
        # Plain PNG, PC only
        "MUA1 PC and Steam": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and Steam)", "optList": ["stat1-1.ini"]}}
        ],
        # PNG8 (no transparency), all consoles
        "XML1 All": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC, PS2, and Xbox)", "optList": None}}
        ],
        "XML2 Xbox": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}}
        ],
        "XML2 PC and Xbox": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC and Xbox)", "optList": None}}
        ],
        "XML2 All": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC, PS2, and PSP)", "optList": None}}
        ],
        # PNG8 alpha, all consoles
        "MUA1 PS2 and PSP": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2 and PSP)", "optList": None}}
        ],
        "MUA2 PS2 and PSP": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA2"], "file": nameDict["MUA2"], "path": pathDict["MUA"], "folder": "for MUA2 (PS2 and PSP)", "optList": None}}
        ],
        # PNG8 (no transparency), PC only. Also DXT1 regardless of consoles.
        "XML2 PC": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
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
        questions.PrintError(f"Choice of texture format did not line up with an existing operation. Selected texture format: {textureFormat}")
        # Update the completion variable to indicate that nothing was processed
        complete = False
    # Return the completion variable
    return complete

# Define the function to process conversation portraits
def iconsProcessing(fullFileName, settings, XMLPath, MUAPath):
    # Determine the texture format
    (textureFormat, fileName) = textures.getIconsTextureFormat(settings, fullFileName)
    # Confirm that a texture format was chosen
    if textureFormat is not None:
        # A texture format was chosen
        # Set up the file names
        (XML1Name, XML2Name, MUA1Name, MUA2Name) = getFileNamesAndNumbers(settings, fullFileName, textureFormat, fileName)
        # Set up the dictionaries for processing
        numsDict = {"XML1": settings["XML1Num"], "XML2": settings["XML2Num"], "MUA1": settings["MUA1Num"], "MUA2": settings["MUA2Num"]}
        nameDict = {"XML1": XML1Name, "XML2": XML2Name, "MUA1": MUA1Name, "MUA2": MUA2Name}
        pathDict = {"XML": XMLPath, "MUA": MUAPath}
        # Process the file
        complete = processIcons("Power Icons", fullFileName, textureFormat, numsDict, nameDict, pathDict)
    else:
        # A texture format was not chosen
        complete = False
    # Return the collected value
    return complete