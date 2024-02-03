# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Resources for this program
import resources
# To be able to copy and move files
import os
# To be able to search for file names
import glob


# ######### #
# FUNCTIONS #
# ######### #
# Define the validator for the file name of unknown assets
def fileNameValidatorStart(fileName):
    if len(fileName) == 0:
        return "Please enter a file name."
    elif ".igb" in fileName:
        return "Do not include the file extension."
    elif not(os.path.exists(fileName + ".igb")):
        return "The file does not exist."
    else:
        return True

# Define the function to get asset choice options
def getAssetChoices(XML1Num, XML2Num, MUA1Num, MUA2Num):
    # Initialize the file name variable
    fileName = "Known"
    # Skins are present in every game
    assetChoices = ["Skin"]
    # Include mannequins if an MUA1 or MUA2 number is present
    if (not(MUA1Num == "")) or (not(MUA2Num == "")):
        assetChoices.append("Mannequin")
    # Include 3D heads if an XML1 or XML2 number is present
    if (not(XML1Num == "")) or (not(XML2Num == "")):
        assetChoices.append("3D Head")
    # Conversation portraits are present in every game
    assetChoices.append("Conversation Portrait")
    # Include CSPs if an XML1 or XML2 number is present
    if (not(XML1Num == "")) or (not(XML2Num == "")):
        assetChoices.append("Character Select Portrait")
    # Other models are present in every game
    assetChoices.append("Other")
    # Get the asset type
    assetType = resources.select("Which asset type are you finishing?", assetChoices)
    # Determine if the asset is not "Other"
    if not(assetType == "Other"):
        # Asset is not "Other", need to get the file name
        # Ask for the file name
        fileName = resources.path("What is the name of the file that you are processing?", fileNameValidatorStart)
        # add the file extension
        fileName += ".igb"
    return assetType, fileName

# Define the function for getting the asset type from the file name
def assetRecognition(XML1Num, XML2Num, MUA1Num, MUA2Num):
    # Create the list of possible file names
    fileNameList = ["igActor01_Animation01DB.igb", "123XX (Mannequin).igb", "123XX (3D Head).igb", "hud_head_123XX.igb", "123XX (Character Select Portrait).igb"]
    # Create the list of asset types
    assetTypeList = ["Skin", "Mannequin", "3D Head", "Conversation Portrait", "Character Select Portrait"]
    # Get the list of file names
    igbList = glob.glob("*.igb")
    # Get the count of igb files
    igbCount = len(igbList)
    # Start a counter to keep track of valid files
    validCounter = 0
    # Initialize the return variable for the asset type
    assetType = "Unknown"
    # Initialize the return variable for the file name
    fileName = "Known"
    # Loop through the list of igb files
    for file in igbList:
        # Compare the file name and asset type lists
        for fileNameOption, assetTypeOption in zip(fileNameList, assetTypeList):
            # Determine if the file names match
            if file == fileNameOption:
                # File names match
                assetType = assetTypeOption
                # Update the counter
                validCounter += 1
    # Determine the number of igb files
    if igbCount > 1:
        # More than 1 igb file is present
        # Determine how many files are valid
        if validCounter == 0:
            # No file was valid
            # Print a warning
            resources.printWarning("WARNING: Multiple igb files were detected in the folder, but none could be identified. Only 1 igb file can be processed at a time. Please choose the asset type.")
            # Check which assets should be asked about
            (assetType, fileName) = getAssetChoices(XML1Num, XML2Num, MUA1Num, MUA2Num)
        else:
            # At least one file was valid
            # Warn the user
            resources.printWarning("WARNING: More than 1 igb file was found, and at least one was recognized. Only 1 igb file can be processed at a time. The file being processed is a " + assetType + ".\n")
    elif igbCount == 1:
        # 1 igb file is present
        # Determine if the 1 file is valid
        if validCounter == 1:
            # File name is valid
            # Print success
            resources.printSuccess("The asset type was automatically identified as a " + assetType + ".\n")
        else:
            # File name could not be identified
            # Print a warning message
            resources.printWarning("WARNING: Asset type could not be identified from the file name. Please choose the asset type.")
            # Check which assets should be asked about
            (assetType, fileName) = getAssetChoices(XML1Num, XML2Num, MUA1Num, MUA2Num)
    else:
        # No igb file is present
        resources.printError("ERROR: No igb file was found in the folder. Please add an igb file and try again.")
        assetType = None
    # return the collected values
    return assetType, fileName