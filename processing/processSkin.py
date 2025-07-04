# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
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
def getSkinFileNamesAndNumbers(settings, fullFileName):
    # Get the geometry names from the file
    geomNames = alchemy.GetModelStats(fullFileName)
    # Set the cel shading option to False initially. It could be updated to True if cel shading is detected.
    celChoice = False
    # Loop through the geometry names.
    for name in geomNames:
        # Determine if the geometry name has "_outline" in it
        if "_outline" in name:
            # "_outline" is in a geometry name, meaning that this skin has cel shading.
            # Since cel shading was detected, set the cel shading choice to True.
            celChoice = True
    # Determine if cel shading is in use
    if celChoice == True:
        # Cel shading is in use.
        # Only XML1 and XML2 use cel shading, so only add them to the list.
        gameList = ["XML1", "XML2"]
    else:
        # Cel shading is not in use.
        # All four games are in use, so add them all to the list.
        gameList = ["XML1", "XML2", "MUA1", "MUA2"]
    # Initialize a list to keep track of which games need a special name
    nameList = []
    # Loop through the 4 games
    for game in gameList:
        # Set the default description for the file
        description = "Skin"
        # Determine if this game is used
        if settings[f"{game}Num"] is not None:
            # This game is used.
            # Determine if the last two digits of the skin number are XX.
            if not(settings[f"{game}Num"][-2:] == "XX"):
                # The last two digits are not XX.
                # Warn the user that this isn't recommended.
                questions.printWarning(f"The skin number for {game} is set to {settings[f'{game}Num']}. Unless this is a special case, it's recommended that the skin number in the settings ends with \"XX\", which will process the skin with the number ending in 01 and no special descriptor.", skip_pause=True)
                # Ask the user what they want to do.
                numChoice = questions.select(f"What do you want to do for the {game} number?", [f"Update the number to {settings[f'{game}Num'][0:-2]}XX (does not overwrite settings.ini).", "Leave the number as-is. This is a special skin/animated bolton that needs a unique number and file name.", "Leave the number as-is. I want to use a specific skin number and not have any descriptor."])
                # Determine what the user picked.
                if numChoice == f"Update the number to {settings[f'{game}Num'][0:-2]}XX (does not overwrite settings.ini).":
                    # The user wanted to update the skin number to end in 01.
                    # Update the settings for this game.
                    settings[f"{game}Num"] = f"{settings[f'{game}Num'][0:-2]}01"
                elif numChoice == "Leave the number as-is. This is a special skin/animated bolton that needs a unique number and file name.":
                    # The user wants to leave the number as-is, but this is a special model with a new name.
                    # Indicate that a special name is needed
                    description = questions.textInput("Enter a descriptor for the file (i.e., \"Boss Skin\", \"Tail Bolton\", \"Wings\", \"Left Arm\", etc.)", None)
                else:
                    # The user wants to leave the number as-is
                    # Set an empty descriptor
                    description = None
            else:
                # The last two digits are XX
                # Set the proper skin number
                settings[f"{game}Num"] = settings[f'{game}Num'][0:-2] + "01"
            # Determine if cel shading is being used, or if this is an MUA game
            if ((celChoice == True) or ((celChoice == False) and (game[0] == "M"))):
                # Cel shading is in use, or this is an MUA game
                # Set the suffix
                suffix = ""
            else:
                # This is an XML game and cel shading is not in use
                # Set the suffix
                suffix = " - No Cel"
            # Determine if there is a descriptor
            if description is None:
                # There is no descriptor
                # Set the file name
                nameList.append(common.setUpFileName2("", settings[f"{game}Num"], ".igb"))
            elif description == "Skin":
                # This is the standard description
                # Set the file name
                nameList.append(common.setUpFileName2("", f"{settings[f'{game}Num'][0:-2]}XX", f" ({description}{suffix}).igb"))
            else:
                # There is a special descriptor
                # Set the file name
                nameList.append(common.setUpFileName2("", settings[f"{game}Num"], f" ({description}{suffix}).igb"))
        else:
            # The game is not used.
            # The name should be None as well
            nameList.append(None)
    # Determine if MUA1/MUA2 were skipped due to cel shading
    if len(nameList) == 2:
        # MUA1 and MUA2 were skipped.
        # Add two None entries for those games.
        nameList.extend([None, None])
    # Break out the list into the specific variables
    XML1Name = nameList[0]
    XML2Name = nameList[1]
    MUA1Name = nameList[2]
    MUA2Name = nameList[3]
    # Return the collected values
    return (settings, XML1Name, XML2Name, MUA1Name, MUA2Name)

# Define the function to process skins
def skinProcessing(fullFileName, settings, XMLPath, MUAPath):
    # Determine the texture format
    textureFormat = textures.get3DTextureFormat("Skin", settings, fullFileName)
    # Confirm that a texture format was chosen
    if textureFormat is not None:
        # A texture format was chosen
        # Set up file names
        (settings, XML1Name, XML2Name, MUA1Name, MUA2Name) = getSkinFileNamesAndNumbers(settings, fullFileName)
        # Set up the dictionaries for processing
        numsDict = {"XML1": settings["XML1Num"], "XML2": settings["XML2Num"], "MUA1": settings["MUA1Num"], "MUA2": settings["MUA2Num"]}
        nameDict = {"XML1": XML1Name, "XML2": XML2Name, "MUA1": MUA1Name, "MUA2": MUA2Name}
        pathDict = {"XML": XMLPath, "MUA": MUAPath}
        # Process the file
        complete = processing.process3D("Skin", fullFileName, textureFormat, numsDict, nameDict, pathDict)
    else:
        # A texture format was not chosen
        complete = False
    # Return the collected value
    return complete