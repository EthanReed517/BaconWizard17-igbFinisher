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
def getHeadFileNamesAndNumbers(settings, fullFileName):
    # Initialize a list of names
    nameList = []
    # Cycle through the list of games
    for game in ["XML1", "XML2"]:
        # Set the default description for the file
        description = "3D Head"
        # Determine if this game is used
        if settings[f"{game}Num"] is not None:
            # This game is used.
            # Determine if the last two digits of the skin number are XX.
            if not(settings[f"{game}Num"][-2:] == "XX"):
                # The last two digits are not XX.
                # Warn the user that this isn't recommended.
                questions.printWarning(f"The skin number for {game} is set to {settings[f'{game}Num']}. Unless this is a special case, it's recommended that the skin number in the settings ends with \"XX\", which will process the 3D Head with the number ending in 01 and no special descriptor.")
                # Ask the user what they want to do.
                numChoice = questions.select(f"What do you want to do for the {game} number?", [f"Update the number to {settings[f'{game}Num'][0:-2]}XX (does not overwrite settings.ini).", "Leave the number as-is. This is a special 3D head that needs a unique number and file name.", "Leave the number as-is. I want to use a specific skin number and not have any descriptor."])
                # Determine what the user picked.
                if numChoice == f"Update the number to {settings[f'{game}Num'][0:-2]}XX (does not overwrite settings.ini).":
                    # The user wanted to update the skin number to end in 01.
                    # Update the settings for this game.
                    settings[f"{game}Num"] = f"{settings[f'{game}Num'][0:-2]}01"
                elif numChoice == "Leave the number as-is. This is a special 3D head that needs a unique number and file name.":
                    # The user wants to leave the number as-is, but this is a special model with a new name.
                    # Indicate that a special name is needed
                    description = questions.textInput("Enter a descriptor for the file (i.e., \"Boss 3D Head\", etc.)", None)
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
            elif description == "3D Head":
                # This is the standard descriptor
                # Set the file name
                nameList.append(common.setUpFileName2("", f"{settings[f'{game}Num'][0:-2]}XX", f" ({description}).igb"))
            else:
                # There is a special descriptor
                # Set the file name
                nameList.append(common.setUpFileName2("", settings[f"{game}Num"], f" ({description}).igb"))
        else:
            # The game is not in use
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
    return (settings, XML1Name, XML2Name, MUA1Name, MUA2Name)

# Define the function to process 3D heads
def headProcessing(fullFileName, settings, XMLPath, MUAPath):
    # Determine the texture format
    textureFormat = textures.get3DTextureFormat("3D Head", settings, fullFileName)
    # Confirm that a texture format was chosen
    if textureFormat is not None:
        # A texture format was chosen
        # Set up file names
        (settings, XML1Name, XML2Name, MUA1Name, MUA2Name) = getHeadFileNamesAndNumbers(settings, fullFileName)
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