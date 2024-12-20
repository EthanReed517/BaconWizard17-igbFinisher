# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import common
import processing
import questions
import textures
# External modules
import os.path
from shutil import copy


# ######### #
# FUNCTIONS #
# ######### #
# Define the function for getting the file names
def getFileNamesAndNumbers(settings, fullFileName):
    # Initialize a list of names
    nameList = []
    # Cycle through the list of games
    for game in ["XML1", "XML2"]:
        # Determine if the game is in use
        if settings[f"{game}Num"] is not None:
            # The game is in use
            # Determine if the number ends in 01
            if not(settings[f"{game}Num"][-2:] == "01"):
                # The number does not end in 01
                # Warn the user that this isn't recommended.
                questions.printWarning(f"The skin number for {game} is set to {settings[f'{game}Num']}. It's recommended for the last two digits of the skin number to be 01 outside of special cases.")
                # Ask the user what they want to do.
                numChoice = questions.select(f"What do you want to do for the {game}number?", [f"Update the number to {settings[f'{game}Num'][0:-2]}01 (does not overwrite settings.ini).", "Leave the number as-is. I want to use a specific skin number."])
                if numChoice == f"Update the number to {settings[f'{game}Num'][0:-2]}01 (does not overwrite settings.ini).":
                    # The user wants to update the number
                    # Update the number to end in 01
                    settings[f"{game}Num"] = f"{settings[f'{game}Num'][0:-2]}01"
            # Determine what the number is
            if settings[f"{game}Num"][-2:] == "01":
                # Standard numbering, can end the number in "XX"
                # Set the file name
                nameList.append(common.setUpFileName2("", f"{settings[f'{game}Num'][0:-2]}XX", " (3D Head).igb"))
            else:
                # Non-standard file name
                # Set the file name
                nameList.append(common.setUpFileName2("", settings[f"{game}Num"], " (3D Head).igb"))
        else:
            # The game is not not in use
            # Set no name
            nameList.append(None)
    # Add two None entries for MUA1 and MUA2.
    nameList.extend([None, None])
    # Break out the list into the specific variables
    XML1Name = nameList[0]
    XML2Name = nameList[1]
    MUA1Name = nameList[2]
    MUA2Name = nameList[3]
    # Return the collected values
    return (XML1Name, XML2Name, MUA1Name, MUA2Name)

# Define the function to process skins
def headProcessing(fullFileName, settings, XMLPath, MUAPath):
    # Determine the texture format
    textureFormat = textures.get3DTextureFormat("3D Head", settings, fullFileName)
    # Confirm that a texture format was chosen
    if textureFormat is not None:
        # A texture format was chosen
        # Set up file names
        (XML1Name, XML2Name, MUA1Name, MUA2Name) = getFileNamesAndNumbers(settings, fullFileName)
        # Set up the dictionaries for processing
        numsDict = {"XML1": settings["XML1Num"], "XML2": settings["XML2Num"], "MUA1": settings["MUA1Num"], "MUA2": settings["MUA2Num"]}
        nameDict = {"XML1": XML1Name, "XML2": XML2Name, "MUA1": MUA1Name, "MUA2": MUA2Name}
        pathDict = {"XML": XMLPath, "MUA": MUAPath}
        # Process the file
        complete = processing.process3D("3D Head", fullFileName, textureFormat, numsDict, nameDict, pathDict)
    else:
        # A texture format was not chosen
        complete = False
    # Return the collected value
    return complete