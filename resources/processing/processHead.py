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
    # Initialize a list of names
    nameList = []
    # Cycle through the list of games
    for game in ["XML1", "XML2"]:
        # Determine if the game is in use
        if not(settings[game + "Num"] == None):
            # The game is in use
            # Determine if the number ends in 01
            if not(settings[game + "Num"][-2:] == "01"):
                # The number does not end in 01
                # Warn the user that this isn't recommended.
                resources.printWarning("The skin number for " + str(game) + " is set to " + settings[game + "Num"] + ". It's recommended for the last two digits of the skin number to be 01 outside of special cases.")
                # Ask the user what they want to do.
                numChoice = resources.select("What do you want to do for the " + game + "number?", ["Update the number to " + settings[game + "Num"][0:-2] + "01 (does not overwrite settings.ini).", "Leave the number as-is. I want to use a specific skin number."])
                if numChoice == "Update the number to " + settings[game + "Num"][0:-2] + "01 (does not overwrite settings.ini).":
                    # The user wants to update the number
                    # Update the number to end in 01
                    settings[game + "Num"] = settings[game + "Num"][0:-2] + "01"
            # Determine what the number is
            if settings[game + "Num"][-2:] == "01":
                # Standard numbering, can end the number in "XX"
                # Set the file name
                nameList.append(resources.setUpFileName(fullFileName, "", settings[game + "Num"][0:-2] + "XX", " (3D Head).igb"))
            else:
                # Non-standard file name
                # Set the file name
                nameList.append(resources.setUpFileName(fullFileName, "", settings[game + "Num"], " (3D Head).igb"))
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
    textureFormat = resources.get3DTextureFormat("3D Head", settings, fullFileName)
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
        resources.hexEdit([settings["XML1Num"], settings["XML2Num"], settings["MUA1Num"], settings["MUA2Num"]], [XML1Name, XML2Name, MUA1Name, MUA2Name], "3D Head")
        # Process the file
        complete = resources.process3D("3D Head", textureFormat, XML1Name, XML2Name, MUA1Name, MUA2Name, XMLPath, MUAPath, settings)
        # Delete the lingering files
        resources.deleteLingering([XML1Name, XML2Name, MUA1Name, MUA2Name])
    else:
        # A texture format was not chosen
        complete = False
    # Return the collected value
    return complete