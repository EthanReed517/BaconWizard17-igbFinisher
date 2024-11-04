# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import questions
# External modules
import os.path


# ######### #
# FUNCTIONS #
# ######### #
# Define the validator for the file name of unknown assets
def fileNameValidatorStart(fileName):
    if len(fileName) == 0:
        return "Please enter a file name."
    elif ".igb" in fileName:
        return "Do not include the file extension."
    elif not(os.path.exists(f"{fileName}.igb")):
        return "The file does not exist."
    else:
        return True

# Define the function to get asset choice options
def getAssetChoices(settings):
    # Initialize the file name variable
    fileName = "Known"
    # Skins are present in every game
    assetChoices = ["Skin"]
    # Include mannequins if an MUA1 or MUA2 number is present
    if ((settings["MUA1Num"] is not None) or (settings["MUA2Num"] is not None)):
        assetChoices.append("Mannequin")
    # Include 3D heads if an XML1 or XML2 number is present
    if ((settings["XML1Num"] is not None) or (settings["XML2Num"] is not None)):
        assetChoices.append("3D Head")
    # Conversation portraits are present in every game
    assetChoices.append("Conversation Portrait")
    # Include CSPs if an XML1 or XML2 number is present
    if ((settings["XML1Num"] is not None) or (settings["XML2Num"] is not None)):
        assetChoices.append("Character Select Portrait")
    # Other models are present in every game
    assetChoices.append("Other")
    # Get the asset type
    assetType = questions.selectDefault("Which asset type are you finishing?", assetChoices, "Other")
    # Determine if the asset is not "Other"
    return assetType

# Define the function for getting the asset type from the file name
def assetRecognition(inputFileName, fullFileName, settings):
    # Create the list of possible file names
    fileNameList = ["igActor01_Animation01DB.igb", "123XX (Mannequin", "123XX (3D Head).igb", "hud_head_123XX.igb", "123XX (Character Select Portrait).igb"]
    # Create the list of asset types
    assetTypeList = ["Skin", "Mannequin", "3D Head", "Conversation Portrait", "Character Select Portrait"]
    # Initialize the return variable for the asset type
    assetType = "Unknown"
    # Initialize the return variable for the file name
    fileName = "Known"
    # Compare the file name and asset type lists
    for fileNameOption, assetTypeOption in zip(fileNameList, assetTypeList):
        # Determine if the file names match
        if fileNameOption in inputFileName:
            # File names match
            assetType = assetTypeOption
    # Determine if a valid name was found
    if assetType == "Unknown":
        # The file does not have a known name
        # Print a warning message
        questions.printWarning(f"The asset type for {inputFileName} could not be identified from the file name. Please choose the asset type.")
        # Check which assets should be asked about
        assetType = getAssetChoices(settings)
        # Set the file name
        fileName = fullFileName
    else:
        # The file has a known name
        # Print success
        questions.printSuccess(f"{inputFileName} was automatically identified as a {assetType}.\n")
    # return the collected values
    return assetType, fileName