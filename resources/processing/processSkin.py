# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Resources for this program
import resources
# To be able to manipulate paths
import os.path
# To be able to copy files
from shutil import copy


# ######### #
# FUNCTIONS #
# ######### #
# Define the function for getting the file names
def getFileNamesAndNumbers(settings, fullFileName):
    # Get the geometry names from the file
    geomNames = resources.GetModelStats(fullFileName)
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
        if not(settings[game + "Num"] == None):
            # This game is used.
            # Determine if the last two digits of the skin number are 01.
            if not(settings[game + "Num"][-2:] == "01"):
                # The last two digits are not 01.
                # Warn the user that this isn't recommended.
                resources.printWarning("The skin number for " + str(game) + " is set to " + settings[game + "Num"] + ". It's recommended for the last two digits of the skin number to be 01 outside of special cases.")
                # Ask the user what they want to do.
                numChoice = resources.select("What do you want to do for the " + game + "number?", ["Update the number to " + settings[game + "Num"][0:-2] + "01 (does not overwrite settings.ini).", "Leave the number as-is. This is a special skin/animated bolton that needs a unique number and file name.", "Leave the number as-is. I want to use a specific skin number."])
                # Determine what the user picked.
                if numChoice == "Update the number to " + settings[game + "Num"][0:-2] + "01 (does not overwrite settings.ini).":
                    # The user wanted to update the skin number to end in 01.
                    # Update the settings for this game.
                    settings[game + "Num"] = settings[game + "Num"][0:-2] + "01"
                elif numChoice == "Leave the number as-is. This is a special skin/animated bolton that needs a unique number and file name.":
                    # The user wants to leave the number as-is, but this is a special model with a new name.
                    # Indicate that a special name is needed
                    description = resources.textInput("Enter a descriptor for the file (i.e., \"Tail Bolton\", \"Wings\", or \"Left Arm\")", None)
            # Determine if cel shading is being used, or if this is an MUA game
            if ((celChoice == True) or ((celChoice == False) and (game[0] == "M"))):
                # Cel shading is in use, or this is an MUA game
                # Set the suffix
                suffix = ""
            else:
                # This is an XML game and cel shading is not in use
                # Set the suffix
                suffix = " - No Cel"
            # Determine what the number is
            if settings[game + "Num"][-2:] == "01":
                # Standard numbering, can end the number in "XX"
                # Set the file name
                nameList.append(resources.setUpFileName(fullFileName, "", settings[game + "Num"][0:-2] + "XX", " (Skin" + suffix + ").igb"))
            else:
                # Non-standard file name
                # Set the file name
                nameList.append(resources.setUpFileName(fullFileName, "", settings[game + "Num"], " (" + description + suffix + ").igb"))
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
    return (XML1Name, XML2Name, MUA1Name, MUA2Name)

# Define the function to process skins
def skinProcessing(fullFileName, settings, XMLPath, MUAPath):
    # Determine the texture format
    textureFormat = resources.get3DTextureFormat("Skin", settings, fullFileName)
    # Confirm that a texture format was chosen
    if not(textureFormat == None):
        # A texture format was chosen
        # Set up file names
        (XML1Name, XML2Name, MUA1Name, MUA2Name) = getFileNamesAndNumbers(settings, fullFileName)
        # Copy the files
        for num, name in zip([settings["XML1Num"], settings["XML2Num"], settings["MUA1Num"], settings["MUA2Num"]], [XML1Name, XML2Name, MUA1Name, MUA2Name]):
            # Determine if the number is used
            if (not(num == None) and not(name == None) and not(os.path.exists(name))):
                # Number isn't empty, need to copy
                # Perform the copying
                copy(fullFileName, name)
        # Perform the hex editing
        resources.hexEdit([settings["XML1Num"], settings["XML2Num"], settings["MUA1Num"], settings["MUA2Num"]], [XML1Name, XML2Name, MUA1Name, MUA2Name], "Skin")
        # Process the file
        complete = resources.process3D("Skin", textureFormat, XML1Name, XML2Name, MUA1Name, MUA2Name, XMLPath, MUAPath, settings)
        # Delete the lingering files
        resources.deleteLingering([XML1Name, XML2Name, MUA1Name, MUA2Name])
    else:
        # A texture format was not chosen
        complete = False
    # Return the collected value
    return complete