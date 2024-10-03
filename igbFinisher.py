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
# To be able to rename files and call command prompts
from os import rename, system
# To be able to set up UIs
import tkinter as tk
# For stylized UIs
import tkinter.ttk as ttk
# For drag and drop support
from tkinterdnd2 import DND_FILES, TkinterDnD
# For UI image support
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
    resources.printPlain("██╗ ██████╗ ██████╗ ███████╗██╗███╗   ██╗██╗███████╗██╗  ██╗███████╗██████╗ ")
    resources.printPlain("██║██╔════╝ ██╔══██╗██╔════╝██║████╗  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗")
    resources.printPlain("██║██║  ███╗██████╔╝█████╗  ██║██╔██╗ ██║██║███████╗███████║█████╗  ██████╔╝")
    resources.printPlain("██║██║   ██║██╔══██╗██╔══╝  ██║██║╚██╗██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗")
    resources.printPlain("██║╚██████╔╝██████╔╝██║     ██║██║ ╚████║██║███████║██║  ██║███████╗██║  ██║")
    resources.printPlain("╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝")
    # Print relevant info
    resources.printPlain("\nVersion 2.0.2")
    resources.printPlain("https://marvelmods.com/forum/index.php/topic,11440.0.html\n")

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
    settings = resources.parseConfig()
    # Trim the curly brackets off the file name
    fullFileName = fullFileName.data.replace("{", "").replace("}", "")
    # Get the file name
    inputFileName = os.path.basename(fullFileName)
    # Determine the numbers
    settings = getNumbers(settings)
    # Determine the asset type
    (assetType, fileName) = resources.assetRecognition(inputFileName, fullFileName, settings)
    # Determine if an XML-compatible asset is being used
    if not(assetType == "Mannequin"):
        # XML-compatible asset is being used
        # Get the XML file path
        XMLPath = getFilePath(settings, "XML", "XML1", "XML2")
    else:
        # Not XML-compatible (mannequin)
        # Set the path to none
        XMLPath = None
    # Determine if an MUA-compatible asset is being used
    if not((assetType == "Character Select Portrait") or (assetType == "3D Head")):
        # MUA-compatible asset is being used
        # Get the MUA file path
        MUAPath = getFilePath(settings, "MUA", "MUA1", "MUA2")
    else:
        # Not MUA-compatible (CSP or 3D Head)
        # Set the path to none
        MUAPath = None
    # Determine if the file name is known
    if not(fileName == "Known"):
        # Name unknown, need to update
        fullFileName = fileNameCorrection(fullFileName, assetType)
    # Begin processing
    if assetType == "Skin":
        # Skin
        # Call the skin processing function
        complete = resources.skinProcessing(fullFileName, settings, XMLPath, MUAPath)
    elif assetType == "Mannequin":
        # Mannequin
        # Call the mannequin processing function
        complete = resources.mannProcessing(fullFileName, settings, XMLPath, MUAPath)
    elif assetType == "3D Head":
        # 3D Head
        # Call the 3D head processing function
        complete = resources.headProcessing(fullFileName, settings, XMLPath, MUAPath)
    elif assetType == "Conversation Portrait":
        # Conversation portrait
        # Call the conversation portrait processing function
        complete = resources.convoProcessing(fullFileName, settings, XMLPath, MUAPath)
    elif assetType == "Character Select Portrait":
        # Character select portrait
        # Call the mannequin processing function
        complete = resources.CSPProcessing(fullFileName, settings, XMLPath)
    else:
        # Other models
        complete = resources.otherProcessing(fullFileName, settings, XMLPath, MUAPath)
    # Clear the screen from the previous run
    system("cls")
    # Print the welcome information
    displayInfo()
    # Determine if the process was complete
    if complete == True:
        # The process was completed
        # Print the completion message
        resources.printSuccess(assetType + " " + inputFileName + " was successfully processed!")
    else:
        # The process was not completed
        # Print the error message
        resources.printError(assetType + " " + inputFileName + "was not able to be processed.", False)

# Define the function to get the character numbers
def getNumbers(settings):
    # Go through the different games.
    for game in ["XML1", "XML2", "MUA1", "MUA2"]:
        # Determine if the character number for that game needs to be asked about.s
        if settings[game + "Num"] == "Ask":
            # Need to ask about the character number.
            # Ask the user.
            settings[game + "Num"] = resources.textInput("Enter the 4 or 5 digit skin number for " + game + ":", resources.skinNumberValidator)
    # Return the updated settings.
    return settings

# Define the function to get the file path
def getFilePath(settings, series, game1Name, game2Name):
    # Set up the numbers
    game1Num = settings[game1Name + "Num"]
    game2Num = settings[game2Name + "Num"]
    # Determine if a path should be collected
    if settings[series + "Path"] == None:
        # No path, so just set it to none
        filePath = None
    elif settings[series + "Path"] == "Ask":
        # Need to ask about the path
        # Determine which games are in use
        if (game1Num == None) and (game2Num == None):
            # Neither game is in use
            filePath = None
        else:
            # At least one game is in use
            if not(game1Num == None):
                # game 1 is in use
                if not(game2Num == None):
                    # game 1 and game 2 are in use
                    games = game1Name + "/" + game2Name
                else:
                    # Only game 1 is in use
                    games = game1Name
            else:
                # Only game 2 is in use
                games = game2Name
            # Create the message for the prompt
            message = "Enter the path to the folder for the " + games + " release:"
            # Ask the question
            filePath = resources.path(message, resources.pathValidator)
            # Replace any incorrect slashes
            filePath = filePath.replace("\\", "/")
    else:
        # The path is already in the settings
        filePath = settings[series + "Path"]
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
resources.printImportant("Welcome to BaconWizard17's igb Finisher!\n")
# Read the settings
settings = resources.parseConfig()
# Reset the Alchemy eval to avoid possible issues
resources.resetAlchemy()
# Initialize the window
window_dnd = initializeWindow()
# Initialize the drop zone
lbl_drop = initializeDropZone()
# Start the window loop
window_dnd.mainloop()
# Add a "press any key to continue" prompt
resources.pressAnyKey(None)