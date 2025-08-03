# ########### #
# INFORMATION #
# ########### #
# This module is the main function for igbFinisher that the rest of the program runs on.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import assetRecognition
import basicXMLOps
import questions
import processing
import settings
# External modules
import argparse
import os.path
from os import rename, system
from pathlib import Path
import sys


# ######### #
# FUNCTIONS #
# ######### #
# This function displays the command prompt information.
def DisplayInfo():
    # Display the title.
    questions.PrintPlain('██╗ ██████╗ ██████╗ ███████╗██╗███╗   ██╗██╗███████╗██╗  ██╗███████╗██████╗ ')
    questions.PrintPlain('██║██╔════╝ ██╔══██╗██╔════╝██║████╗  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗')
    questions.PrintPlain('██║██║  ███╗██████╔╝█████╗  ██║██╔██╗ ██║██║███████╗███████║█████╗  ██████╔╝')
    questions.PrintPlain('██║██║   ██║██╔══██╗██╔══╝  ██║██║╚██╗██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗')
    questions.PrintPlain('██║╚██████╔╝██████╔╝██║     ██║██║ ╚████║██║███████║██║  ██║███████╗██║  ██║')
    questions.PrintPlain('╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝')
    # Print the relevant information.
    questions.PrintPlain('\nVersion 3.1.0')
    questions.PrintPlain('https://marvelmods.com/forum/index.php/topic,11440.0.html\n')

# This function gets the application path.
def GetApplicationPath():
    # Get the execution path by first checking if there is a frozen attribute for the system.
    if getattr(sys, 'frozen', False):
        # There is a frozen attribute, so this is running as the compiled exe.
        # Get the path to the exe's folder.
        application_path  = Path(('/').join(Path(sys.executable).parts[0:-1]))
    else:
        # There is no frozen attribute, so this is not compiled.
        # Get the path to the main python file's folder.
        application_path = Path(('/').join(Path(__file__).resolve().parts[0:-1]))
    # Return the collected path
    return application_path

# This function processes the arguments.
def ProcessArguments(args, application_path):
    # Check if the input file path can be converted to a path.
    try:
        input_file_path = Path(args.input_file_path)
    except Exception as e:
        questions.PrintError(f'The input file ({args.input_file_path}) could not be processed as a path. Error text:\n\n{e}\n\nThe system will now exit.', system_exit = True)
    # Check if the input file exists.
    if not(input_file_path.exists()):
        # The input path does not exist.
        # Print the error.
        questions.PrintError(f'The input file ({args.input_file_path}) does not exist. The system will now exit.', system_exit = True)
    # Check if a settings path was entered.
    if args.settings_file_path is None:
        # No settings path was entered.
        # Use the default path.
        settings_file_path = application_path / 'settings.ini'
    else:
        # Something was entered.
        # Check if the file exists.
        if Path(args.settings_file_path).exists():
            # The file exists.
            # Set this value.
            settings_file_path = Path(args.settings_file_path)
        else:
            # The file does not exist.
            # Give a warning.
            questions.PrintError(f'The input settings file ({args.settings_file_path}) does not exist. The system will now exit.', system_exit = True)
    # Return the collected arguments.
    return input_file_path, settings_file_path

# Define the function that will occur when a file is dropped
def fileDrop(fullFileName):
    # Clear the screen from the previous run
    system("cls")
    # Print the welcome information
    displayInfo()
    # Restore the settings from the ini file
    settings = settings.parse_settings()
    # Trim the curly brackets off the file name
    fullFileName = fullFileName.data.replace("{", "").replace("}", "")
    # Get the file name
    inputFileName = os.path.basename(fullFileName)
    # Determine the numbers
    settings = getNumbers(settings)
    # Determine the asset type
    (assetType, fileName) = assetRecognition.assetRecognition(inputFileName, fullFileName, settings)
    # Determine if an XML-compatible asset is being used
    if not(assetType == "Mannequin"):
        # XML-compatible asset is being used
        # Get the XML file path
        XMLPath = getFilePath(fullFileName, settings, assetType, "XML", "XML1", "XML2")
    else:
        # Not XML-compatible (mannequin)
        # Set the path to none
        XMLPath = None
    # Determine if an MUA-compatible asset is being used
    if not((assetType == "Character Select Portrait") or (assetType == "3D Head")):
        # MUA-compatible asset is being used
        # Get the MUA file path
        MUAPath = getFilePath(fullFileName, settings, assetType, "MUA", "MUA1", "MUA2")
    else:
        # Not MUA-compatible (CSP or 3D Head)
        # Set the path to none
        MUAPath = None
    # Determine if the file name is known
    if not(fileName == "Known"):
        # Name unknown, need to update
        fullFileName = fileNameCorrection(fullFileName, assetType)
    # Set up the dictionary for processing
    processingDict = {
        "Skin": processing.skinProcessing,
        "Mannequin": processing.mannProcessing,
        "3D Head": processing.headProcessing,
        "Conversation Portrait": processing.convoProcessing,
        "Character Select Portrait": processing.CSPProcessing,
        "Loading Screen": processing.loadProcessing,
        "Power Icons": processing.iconsProcessing,
        "Comic Cover": processing.comicProcessing,
        "Other": processing.otherProcessing,
    }
    # Begin processing
    complete = processingDict[assetType](fullFileName, settings, XMLPath, MUAPath)
    # Clear the screen from the previous run
    system("cls")
    # Print the welcome information
    displayInfo()
    # Determine if the process was complete
    if complete == True:
        # The process was completed
        # Print the completion message
        questions.PrintSuccess(f"{assetType} {inputFileName} was successfully processed!")
    else:
        # The process was not completed
        # Print the error message
        questions.PrintError(f"{assetType} {inputFileName} was not able to be processed.")

# Define the function to get the character numbers
def getNumbers(settings):
    # Go through the different games.
    for game in ["XML1", "XML2", "MUA1", "MUA2"]:
        # Determine if the character number for that game needs to be asked about.s
        if settings[f"{game}Num"] == "Ask":
            # Need to ask about the character number.
            # Ask the user.
            settings[f"{game}Num"] = questions.TextInput(f"Enter the 4 or 5 digit skin number for {game}:", validator = questions.SkinNumberValidator)
    # Return the updated settings.
    return settings

# Define the function to get the file path
def getFilePath(fullFileName, settings, assetType, series, game1Name, game2Name):
    # Start by assuming that the file path is unknown
    filePath = "Unknown"
    # Set up the numbers
    game1Num = settings[f"{game1Name}Num"]
    game2Num = settings[f"{game2Name}Num"]
    # Determine if both games are not used
    if ((game1Num is None) and (game2Num is None)):
        # Neither game is in use, so no file path is needed
        filePath = None
    else:
        # Determine if a path should be collected
        if settings[f"{series}Path"] == None:
            # No path, so just set it to none
            filePath = None
        elif settings[f"{series}Path"] == "Detect":
            # Get the list of textures for the model
            (texturePaths, textureFormats) = alchemy.GetTexPath(fullFileName)
            # Determine if there are any textures
            if not(texturePaths == []):
                # There are textures
                # Remove any sphereImage textures, since they won't have a path
                for texturePath in texturePaths:
                    if "sphereImage" in texturePath:
                        sphereImageIndex = texturePaths.index(texturePath)
                        texturePaths.remove(texturePaths[sphereImageIndex])
                # Get the folder from the first path
                firstPath = "\\".join(texturePaths[0].split("\\")[0:-2])
                # Assume that all folders for all paths will be the same
                sameFolders = True
                # Loop through the remaining textures to see if they match
                for texture in texturePaths:
                    currentPath = "\\".join(texture.split("\\")[0:-2])
                    if not(currentPath == firstPath):
                        sameFolders = False
                # Check if the textures all come from the same folder
                if sameFolders == True:
                    # The paths are the same
                    # Get the character folder from the path
                    characterFolder = texturePaths[0].split("\\")[-5]
                    xmlPath = os.path.join("Folder Detection", f"{characterFolder}.xml")
                    # Check if an xml file exists
                    if os.path.exists(xmlPath):
                        # An xml file exists
                        # Open the xml file and get its root
                        pathsRoot = basicXMLOps.openGetTreeAndRoot(xmlPath)
                        # Determine the asset type and get the necessary XML information from it
                        if assetType == "Loading Screen":
                            assetsElem = pathsRoot.find("lscreens")
                            assetElemType = "lscreen"
                        elif assetType == "Power Icons":
                            assetsElem = pathsRoot.find("icons")
                            assetElemType = "icon"
                        elif assetType == "Comic Cover":
                            assetsElem = pathsRoot.find("covers")
                            assetElemType = "cover"
                        else:
                            assetsElem = pathsRoot.find("skins")
                            assetElemType = "skin"
                        # Get the start of the path for the current series
                        pathStart = assetsElem.get(series)
                        # Get the skin's sub-folder
                        skinFolder = texturePaths[0].split("\\")[-3]
                        # Initialize a variable for the sub-folder
                        subFolder = None
                        # Loop through all the assets in the asset element
                        for assetElem in assetsElem.findall(assetElemType):
                            # Check if the element's texFolder attribute matches with the skin's subfolder
                            if assetElem.get("texFolder") == skinFolder:
                                subFolder = assetElem.get("outputFolder")
                        # Check if anything was found
                        if subFolder is not None:
                            # Something was found
                            # Create the path
                            filePath = os.path.join(pathStart, subFolder)
                            # Verify that the path exists
                            if not(os.path.exists(filePath)):
                                questions.PrintWarning(f"The value for the path for the {series} games was set to \"Detect\", but the output path for {skinFolder} ({filePath}) does not exist. Please enter a path instead.", skip_pause = True)
                                # Set the file path back to unknown since it's not found
                                filePath = "Unknown"
                            else:
                                # The file path exists
                                # Announce that it was found
                                questions.PrintSuccess(f"The {series} destination folder was automatically identified as {filePath}.\n")
                        else:
                            # Nothing was found
                            questions.PrintWarning(f"The value for the path for the {series} games was set to \"Detect\", but {characterFolder}.xml does not contain a matching output folder for {skinFolder}. Please enter a path instead.", skip_pause = True)
                    else:
                        # No xml file exists
                        questions.PrintWarning(f"The value for the path for the {series} games was set to \"Detect\", but {characterFolder}.xml does not exist in the \"Folder Detection\" folder. Please enter a path instead.", skip_pause = True)
                else:
                    # The paths are not all the same
                    questions.PrintWarning(f"The value for the path for the {series} games was set to \"Detect\", but the model contains textures that are in multiple folders. Detection does not support multiple folders. Please enter a path instead.", skip_pause = True)
            else:
                # There are no textures
                questions.PrintWarning(f"The value for the path for the {series} games was set to \"Detect\", but the model contains no textures. Please enter a path instead.", skip_pause = True)
        # Determine if anything has been found up to this point
        if filePath == "Unknown":
            # Nothing has been found yet
            # Determine if the setting is a path
            if os.path.exists(settings[f"{series}Path"]):
                # The path is already in the settings
                filePath = settings[f"{series}Path"]
            else:
                # The path is either "Ask", or detection failed. Need to ask.
                # Determine which games are in use
                if game1Num is not None:
                    # game 1 is in use
                    if game2Num is not None:
                        # game 1 and game 2 are in use
                        games = f"{game1Name}/{game2Name}"
                    else:
                        # Only game 1 is in use
                        games = game1Name
                else:
                    # Only game 2 is in use
                    games = game2Name
                # Create the message for the prompt
                message = f"Enter the path to the folder for the {games} release:"
                # Ask the question
                filePath = questions.PathInput(message, validator = questions.PathValidator)
                # Replace any incorrect slashes
                filePath = filePath.replace("\\", "/")
    # Return the path
    return filePath

# Define the function to correct the file name
def fileNameCorrection(fullFileName, assetType):
    # Define the asset type list
    assetTypeList = ["Skin", "Mannequin", "3D Head", "Conversation Portrait", "Character Select Portrait", "Power Icons"]
    # Define the name list
    nameList = ["igActor01_Animation01DB.igb", "123XX (Mannequin).igb", "123XX (3D Head).igb", "hud_head_123XX.igb", "123XX (Character Select Portrait).igb", "power_icons.igb"]
    # List the asset types and names
    for asset, fileName in zip(assetTypeList, nameList):
        # Determine if the assets match
        if asset == assetType:
            # Assets match
            # Update the name
            rename(fullFileName, os.path.join(os.path.dirname(fullFileName), fileName))
            # Set the new file name
            fullFileName = os.path.join(os.path.dirname(fullFileName), fileName)
    # Return the corrected file name
    return fullFileName


# ############## #
# MAIN EXECUTION #
# ############## #
# Set the window title.
system("title BaconWizard17's igb Finisher")
# Print the welcome information.
DisplayInfo()
# Print the welcome message.
questions.PrintImportant("Welcome to BaconWizard17's igb Finisher!\n")
# Get the application path.
application_path = GetApplicationPath()
# Create an argument parser.
parser = argparse.ArgumentParser()
# Add an argument for the input file's path.
parser.add_argument('input_file_path')
# Add an argument for the settings file path.
parser.add_argument('-s', '--settings')
# Parse the arguments.
args = parser.parse_args()
# Process the arguments.
(input_file_path, settings_file_path) = ProcessArguments(args, application_path)


# Read the settings
settings = settings.parse_settings()
# Reset the Alchemy eval to avoid possible issues
alchemy.checkAlchemyReset()
# Check for the animation producer
alchemy.CheckAnimationProducer()


# Add a "press any key to continue" prompt
questions.PressAnyKey(None)