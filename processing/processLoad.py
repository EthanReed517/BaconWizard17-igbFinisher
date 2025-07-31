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
def getLoadFileNamesAndNumbers(settings, fullFileName, textureFormat):
    # Initialize a list of names
    nameList = []
    # Cycle through the list of games
    for game in ["XML1", "XML2", "MUA1", "MUA2"]:
        # Verify that this is used with the game
        if game[0:-1] in textureFormat:
            # This is used with this game
            # Set the default description for the file
            description = "Loading Screen"
            # Determine if this game is used
            if settings[f"{game}Num"] is not None:
                # This game is used.
                # Determine if the last two digits of the skin number are XX.
                if not(settings[f"{game}Num"][-2:] == "XX"):
                    # The last two digits are not XX.
                    # Warn the user that this isn't recommended.
                    questions.PrintWarning(f"The skin number for {game} is set to {settings[f'{game}Num']}. Unless this is a special case, it's recommended that the skin number in the settings ends with \"XX\", which will process the loading screen with the number ending in 01 and no special descriptor.")
                    # Ask the user what they want to do.
                    numChoice = questions.Select(f"What do you want to do for the {game} number?", [f"Update the number to {settings[f'{game}Num'][0:-2]}XX (does not overwrite settings.ini).", "Leave the number as-is. This is a special loading screen that needs a unique number and file name.", "Leave the number as-is. I want to use a specific skin number and not have any descriptor."])
                    # Determine what the user picked.
                    if numChoice == f"Update the number to {settings[f'{game}Num'][0:-2]}XX (does not overwrite settings.ini).":
                        # The user wanted to update the skin number to end in 01.
                        # Update the settings for this game.
                        settings[f"{game}Num"] = f"{settings[f'{game}Num'][0:-2]}01"
                    elif numChoice == "Leave the number as-is. This is a special HUD that needs a unique number and file name.":
                        # The user wants to leave the number as-is, but this is a special model with a new name.
                        # Indicate that a special name is needed
                        description = questions.TextInput("Enter a descriptor for the file (i.e., \"Boss Loading Screen\", etc.)")
                    else:
                        # The user wants to leave the number as-is
                        # Set an empty descriptor
                        description = None
                else:
                    # The last two digits are XX
                    # Set the proper skin number
                    settings[f"{game}Num"] = settings[f'{game}Num'][0:-2] + "01"
                # Determine if there is a descriptor
                if description is None:
                    # There is no descriptor
                    # Set the file name
                    nameList.append(common.setUpFileName2("", settings[f"{game}Num"], ".igb"))
                elif description == "Loading Screen":
                    # There is no custom descriptor
                    # Set the file name
                    nameList.append(common.setUpFileName2("", f"{settings[f'{game}Num'][0:-2]}XX", f" ({description}).igb"))
                else:
                    # There is a descriptor
                    # Set the file name
                    nameList.append(common.setUpFileName2("", settings[f"{game}Num"], f" ({description}).igb"))
            else:
                # The game is not in use
                # Set no name
                nameList.append(None)
        else:
            # This is not used with the game
            # Set no name
            nameList.append(None)
    # Break out the list into the specific variables
    XML1Name = nameList[0]
    XML2Name = nameList[1]
    MUA1Name = nameList[2]
    MUA2Name = nameList[3]
    # Return the collected values
    return (settings, XML1Name, XML2Name, MUA1Name, MUA2Name)

# Define the function to export the portraits
def processLoad(assetType, sourceFileName, textureFormat, numsDict, nameDict, pathDict):
    # Set up the dictionary of necessary operations for each texture type
    processDict = {
        # PNG8 textures
        "XML1 and XML2 PS2": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2)", "optList": None}}
        ],
        "XML2 PSP": [
            {"function": processing.processPSPFiles, "kwargs": {"nums": numsDict, "files": nameDict, "paths": pathDict, "prefix": "stat"}}
        ],
        "MUA1 and MUA2 PS2 and PSP": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA2"], "file": nameDict["MUA2"], "path": pathDict["MUA"], "folder": "for MUA2 (PS2)", "optList": ["stat3.ini"]}},
            {"function": processing.processPSPFiles, "kwargs": {"nums": numsDict, "files": nameDict, "paths": pathDict, "prefix": "stat"}}
        ],
        # DXT1 textures, 4:3
        "XML2 PC": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        "XML1 and XML2 Xbox": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}}
        ],
        "XML1 Xbox, XML2 PC and Xbox": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC and Xbox)", "optList": None}}
        ],
        "XML1 and XML2 GameCube": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}}
        ],
        # DXT1 textures, 16:9
        "MUA1 PC and Steam": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam)", "optList": ["stat1-1.ini"]}}
        ],
        "MUA1 PS3 and 360": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS3 and 360)", "optList": ["stat1-1.ini"]}}
        ],
        "MUA1 Next-Gen": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Next-Gen)", "optList": ["stat1-1.ini"]}}
        ],
        "MUA1 Wii and Xbox, MUA2 Wii": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}},
            {"function": processing.processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
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
def loadProcessing(fullFileName, settings, XMLPath, MUAPath):
    # Determine the texture format
    textureFormat = textures.getLoadTextureFormat(settings, fullFileName)
    # Confirm that a texture format was chosen
    if textureFormat is not None:
        # A texture format was chosen
        # Set up the file names
        (settings, XML1Name, XML2Name, MUA1Name, MUA2Name) = getLoadFileNamesAndNumbers(settings, fullFileName, textureFormat)
        # Set up the dictionaries for processing
        numsDict = {"XML1": settings["XML1Num"], "XML2": settings["XML2Num"], "MUA1": settings["MUA1Num"], "MUA2": settings["MUA2Num"]}
        nameDict = {"XML1": XML1Name, "XML2": XML2Name, "MUA1": MUA1Name, "MUA2": MUA2Name}
        pathDict = {"XML": XMLPath, "MUA": MUAPath}
        # Process the file
        complete = processLoad("Loading Screen", fullFileName, textureFormat, numsDict, nameDict, pathDict)
    else:
        # A texture format was not chosen
        complete = False
    # Return the collected value
    return complete