# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import assetRecognition
import basicXMLOps
import config
import questions
import processing
# External modules
import os.path
from os import rename, system
import tkinter as tk
import tkinter.ttk as ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk


# ######### #
# FUNCTIONS #
# ######### #
# Define the function to get local resources
def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    # Return the collected value
    return os.path.join(base_path, relative_path)

# Define the function to display the command prompt information
def displayInfo():
    # Display the title
    questions.printPlain("██╗ ██████╗ ██████╗ ███████╗██╗███╗   ██╗██╗███████╗██╗  ██╗███████╗██████╗ ")
    questions.printPlain("██║██╔════╝ ██╔══██╗██╔════╝██║████╗  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗")
    questions.printPlain("██║██║  ███╗██████╔╝█████╗  ██║██╔██╗ ██║██║███████╗███████║█████╗  ██████╔╝")
    questions.printPlain("██║██║   ██║██╔══██╗██╔══╝  ██║██║╚██╗██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗")
    questions.printPlain("██║╚██████╔╝██████╔╝██║     ██║██║ ╚████║██║███████║██║  ██║███████╗██║  ██║")
    questions.printPlain("╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝")
    # Print relevant info
    questions.printPlain("\nVersion 2.1.1")
    questions.printPlain("https://marvelmods.com/forum/index.php/topic,11440.0.html\n")

# Define the function to initialize the window
def initializeWindow():
    # Establish the main window. Drag and drop requires this instead of tk.Tk()
    window_dnd = TkinterDnD.Tk()
    # Set the window title
    window_dnd.title("Queue for BaconWizard17's igbFinisher")
    # Get the icon path
    iconPath = resource_path("icon.ico")
    # set the window icon
    window_dnd.iconbitmap(iconPath)
    # Make it so that the window can't be resized
    window_dnd.resizable(width=False, height=False)
    # Create a label to let the user know what to do
    lbl_dnd = ttk.Label(text="Drag and drop files below:")
    # Pack the label in the window
    lbl_dnd.pack()
    # Return the created window
    return window_dnd

# Define the function to initialize the drop zone
def initializeDropZone():
    # Get the image path
    imagePath = resource_path("images/dropZone.png")
    # Set up the image for the drop zone
    imageFile_dropZone = Image.open(imagePath)
    # Add the image
    image_dropZone = ImageTk.PhotoImage(imageFile_dropZone)
    # Set up the frame for the drop zone
    frame_drop = tk.Frame(relief=tk.SUNKEN, borderwidth=2)
    # Add the label where the image will be shown
    lbl_drop = tk.Label(image=image_dropZone, master=frame_drop)
    # set the image
    lbl_drop.image = image_dropZone
    # Register the label as a drag and drop location
    lbl_drop.drop_target_register(DND_FILES)
    # Set up the function for when a file is dropped
    lbl_drop.dnd_bind('<<Drop>>', fileDrop)\
    # Pack the frame into the UI
    frame_drop.pack()
    # Pack the label into the UI
    lbl_drop.pack()
    # Return the necessary elements for other operations
    return lbl_drop

# Define the function that will occur when a file is dropped
def fileDrop(fullFileName):
    # Clear the screen from the previous run
    system("cls")
    # Print the welcome information
    displayInfo()
    # Restore the settings from the ini file
    settings = config.parseConfig()
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
        XMLPath = getFilePath(fullFileName, settings, "XML", "XML1", "XML2")
    else:
        # Not XML-compatible (mannequin)
        # Set the path to none
        XMLPath = None
    # Determine if an MUA-compatible asset is being used
    if not((assetType == "Character Select Portrait") or (assetType == "3D Head")):
        # MUA-compatible asset is being used
        # Get the MUA file path
        MUAPath = getFilePath(fullFileName, settings, "MUA", "MUA1", "MUA2")
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
        questions.printSuccess(f"{assetType} {inputFileName} was successfully processed!")
    else:
        # The process was not completed
        # Print the error message
        questions.printError(f"{assetType} {inputFileName} was not able to be processed.", False)

# Define the function to get the character numbers
def getNumbers(settings):
    # Go through the different games.
    for game in ["XML1", "XML2", "MUA1", "MUA2"]:
        # Determine if the character number for that game needs to be asked about.s
        if settings[f"{game}Num"] == "Ask":
            # Need to ask about the character number.
            # Ask the user.
            settings[f"{game}Num"] = questions.textInput(f"Enter the 4 or 5 digit skin number for {game}:", questions.skinNumberValidator)
    # Return the updated settings.
    return settings

# Define the function to get the file path
def getFilePath(fullFileName, settings, series, game1Name, game2Name):
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
                if "sphereImage" in texturePaths:
                    texturePaths.remove("sphereImage")
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
                    xmlPathAbs = resource_path(xmlPath)
                    # Check if an xml file exists
                    if os.path.exists(xmlPathAbs):
                        # An xml file exists
                        # Open the xml file and get its root
                        pathsRoot = basicXMLOps.openGetTreeAndRoot(xmlPathAbs)
                        # Get the main release path
                        releaseElem = pathsRoot.find("release")
                        # Get the start of the path for the current series
                        pathStart = releaseElem.get(series)
                        # Get the skin's sub-folder
                        skinFolder = texturePaths[0].split("\\")[-3]
                        # Initialize a variable for the sub-folder
                        subFolder = None
                        # Get the skins element and loop through all the skins in it
                        skinsElem = pathsRoot.find("skins")
                        for skinElem in skinsElem.findall("skin"):
                            # Check if the element's texFolder attribute matches with the skin's subfolder
                            if skinElem.get("texFolder") == skinFolder:
                                subFolder = skinElem.get("outputFolder")
                        # Check if anything was found
                        if subFolder is not None:
                            # Something was found
                            # Create the path
                            filePath = os.path.join(pathStart, subFolder)
                            # Verify that the path exists
                            if not(os.path.exists(filePath)):
                                questions.printWarning(f"The value for the path for the {series} games was set to \"Detect\", but the output path for {skinFolder} ({filePath}) does not exist. Please enter a path instead.")
                        else:
                            # Nothing was found
                            questions.printWarning(f"The value for the path for the {series} games was set to \"Detect\", but {characterFolder}.xml does not contain a matching output folder for {skinFolder}. Please enter a path instead.")
                    else:
                        # No xml file exists
                        questions.printWarning(f"The value for the path for the {series} games was set to \"Detect\", but {characterFolder}.xml does not exist in the Detection folder. Please enter a path instead.")
                else:
                    # The paths are not all the same
                    questions.printWarning(f"The value for the path for the {series} games was set to \"Detect\", but the model contains textures that are in multiple folders. Detection does not support multiple folders. Please enter a path instead.")
            else:
                # There are no textures
                questions.printWarning(f"The value for the path for the {series} games was set to \"Detect\", but the model contains no textures. Please enter a path instead.")
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
                filePath = questions.path(message, questions.pathValidator)
                # Replace any incorrect slashes
                filePath = filePath.replace("\\", "/")
    # Return the path
    return filePath

# Define the function to correct the file name
def fileNameCorrection(fullFileName, assetType):
    # Define the asset type list
    assetTypeList = ["Skin", "Mannequin", "3D Head", "Conversation Portrait", "Character Select Portrait"]
    # Define the name list
    nameList = ["igActor01_Animation01DB.igb", "123XX (Mannequin).igb", "123XX (3D Head).igb", "hud_head_123XX.igb", "123XX (Character Select Portrait).igb"]
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
# Set the window title
system("title BaconWizard17's igb Finisher")
# Print the welcome information
displayInfo()
# Print the welcome message
questions.printImportant("Welcome to BaconWizard17's igb Finisher!\n")
# Read the settings
settings = config.parseConfig()
# Reset the Alchemy eval to avoid possible issues
alchemy.checkAlchemyReset()
# Initialize the window
window_dnd = initializeWindow()
# Initialize the drop zone
lbl_drop = initializeDropZone()
# Start the window loop
window_dnd.mainloop()
# Add a "press any key to continue" prompt
questions.pressAnyKey(None)