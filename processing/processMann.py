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
def getMannFileNamesAndNumbers(settings, fullFileName):
    # Initialize a list of names with Nones for XML1 and XML2
    nameList = [None, None]
    # Get the suffix for the model
    suffix = os.path.basename(fullFileName).split("XX")[1]
    # Cycle through the list of games
    for game in ["MUA1", "MUA2"]:
        # Set the default description for the file
        description = suffix
        # Determine if the game is in use
        if settings[f"{game}Num"] is not None:
            # The game is in use
            # Determine if the number ends in 01
            if settings[f"{game}Num"][-2:] == "XX":
                # The number ends in XX, which is okay
                # Update the number to end in 01 for proper processing
                settings[f"{game}Num"] = settings[f'{game}Num'][0:-2] + "01"
            else:
                # The number does not end in XX
                # Warn the user that the number should end in XX
                questions.PrintWarning(f"The skin number for {game} is set to {settings[f'{game}Num']}. For mannequins, it is recommended that the skin number end in \"XX\", which will process the mannequin with the number ending in 01 and the standard descriptor.")
                # Ask the user what they want to do.
                numChoice = questions.Select(f"What do you want to do for the {game} number?", [f"Update the number to {settings[f'{game}Num'][0:-2]}XX (does not overwrite settings.ini).", "Leave the number as-is. I want the file name to end in 01 and not have any descriptor."])
                # Determine what the user picked.
                if numChoice == f"Update the number to {settings[f'{game}Num'][0:-2]}XX (does not overwrite settings.ini).":
                    # The user wanted to update the skin number to end in 01.
                    # Update the settings for this game.
                    settings[f"{game}Num"] = f"{settings[f'{game}Num'][0:-2]}01"
                else:
                    # The user wants to leave the number as-is
                    # Set an empty descriptor
                    description = None
            # Determine if there is any description
            if description is None:
                # There is on description
                # Set the file name
                nameList.append(common.setUpFileName2("", f"{settings[f'{game}Num'][0:-2]}01" , ".igb"))
            else:
                # There is a description
                # Add the new name to the list
                nameList.append(common.setUpFileName2("", f"{settings[f'{game}Num'][0:-2]}XX", description))
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
    return (settings, XML1Name, XML2Name, MUA1Name, MUA2Name)

# Define the function to process mannequins
def mannProcessing(fullFileName, settings, XMLPath, MUAPath):
    # Determine the texture format
    textureFormat = textures.get3DTextureFormat("Mannequin", settings, fullFileName)
    # Confirm that a texture format was chosen
    if textureFormat is not None:
        # A texture format was chosen
        # Set up file names
        (settings, XML1Name, XML2Name, MUA1Name, MUA2Name) = getMannFileNamesAndNumbers(settings, fullFileName)
        # Set up the dictionaries for processing
        numsDict = {"XML1": settings["XML1Num"], "XML2": settings["XML2Num"], "MUA1": settings["MUA1Num"], "MUA2": settings["MUA2Num"]}
        nameDict = {"XML1": XML1Name, "XML2": XML2Name, "MUA1": MUA1Name, "MUA2": MUA2Name}
        pathDict = {"XML": XMLPath, "MUA": MUAPath}
        # Process the file
        complete = processing.process3D("Mannequin", fullFileName, textureFormat, numsDict, nameDict, pathDict)
    else:
        # A texture format was not chosen
        complete = False
    # Return the collected value
    return complete