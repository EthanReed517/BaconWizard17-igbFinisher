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
    # Initialize a list of names with Nones for XML1 and XML2
    nameList = [None, None]
    # Get the suffix for the model
    suffix = os.path.basename(fullFileName).split("XX")[1]
    # Cycle through the list of games
    for game in ["MUA1", "MUA2"]:
        # Determine if the game is in use
        if not(settings[game + "Num"] == None):
            # The game is in use
            # Determine if the number ends in 01
            if not(settings[game + "Num"][-2:] == "01"):
                # The number does not end in 01
                # Warn the user that the number should end in 01
                resources.printWarning("The skin number for " + str(game) + " is set to " + settings[game + "Num"] + ". The last two digits of a mannequin number should always be 01. " + settings[game + "Num"][0:-2] + "01 will be used as the number. settings.ini will not be updated.")
                # Update the number to end in 01
                settings[game + "Num"] = settings[game + "Num"][0:-2] + "01"
            # Add the new name to the list
            nameList.append(resources.setUpFileName(fullFileName, "", settings["MUA1Num"][0:-2] + "XX", suffix))
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
    

# Define the function to process skins
def mannProcessing(fullFileName, settings, XMLPath, MUAPath):
    # Determine the texture format
    textureFormat = resources.get3DTextureFormat("Mannequin", settings, fullFileName)
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
        resources.hexEdit([settings["XML1Num"], settings["XML2Num"], settings["MUA1Num"], settings["MUA2Num"]], [XML1Name, XML2Name, MUA1Name, MUA2Name], "Mannequin")
        # Process the file
        complete = resources.process3D("Mannequin", textureFormat, XML1Name, XML2Name, MUA1Name, MUA2Name, XMLPath, MUAPath, settings)
        # Delete the lingering files
        resources.deleteLingering([XML1Name, XML2Name, MUA1Name, MUA2Name])
    else:
        # A texture format was not chosen
        complete = False
    # Return the collected value
    return complete