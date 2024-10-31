# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Modules from this program
import common
import questions
# Other modules
import os.path
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
                questions.printWarning("The skin number for " + str(game) + " is set to " + settings[game + "Num"] + ". The last two digits of a mannequin number should always be 01. " + settings[game + "Num"][0:-2] + "01 will be used as the number. settings.ini will not be updated.")
                # Update the number to end in 01
                settings[game + "Num"] = settings[game + "Num"][0:-2] + "01"
            # Add the new name to the list
            nameList.append(common.setUpFileName2("", settings["MUA1Num"][0:-2] + "XX", suffix))
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