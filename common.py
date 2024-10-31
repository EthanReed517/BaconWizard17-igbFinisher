# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Other modules
import os.path
from os import mkdir, remove
from shutil import copy


# ######### #
# FUNCTIONS #
# ######### #
# Define the function to set up file names
def setUpFileName(fullFileName, prefix, gameNum, suffix):
    # Determine if the character number is None, meaning that the character is not used in this game and the name is not needed
    if gameNum == None:
        # The character number is None, so no name is needed
        # set the file name to None
        gameName = None
    else:
        # The character number is not None, so the file name needs to get set up
        # Set up the file name accordingly
        gameName = os.path.join(os.path.dirname(fullFileName), f"{prefix}{gameNum}{suffix}")
    # Return the collected file name
    return gameName

# Define the alternate function to set up file names
def setUpFileName2(prefix, gameNum, suffix):
    # Determine if the character number is None, meaning that the character is not used in this game and the name is not needed
    if gameNum == None:
        # The character number is None, so no name is needed
        # set the file name to None
        gameName = None
    else:
        # The character number is not None, so the file name needs to get set up
        # Set up the file name accordingly
        gameName = f"{prefix}{gameNum}{suffix}"
    # Return the collected file name
    return gameName

# Define the function to copy files to the necessary destination
def copyToDestination(fileName, releasePath, folderName):
    # Verify that the file name is not a None
    if not(fileName == None):
        # File name is not none
        # Verify that the file exists before copying
        if os.path.isfile(fileName):
            # The file exists
            # Verify that the file path is populated
            if not(releasePath == None):
                # The path is populated
                # Create the path to the game-specific release folder
                gamePath = os.path.join(releasePath, folderName)
                # Verify if the folder already exists
                if not(os.path.exists(gamePath)):
                    # Folder does not yet exist
                    # Create the folder
                    mkdir(gamePath)
                # Copy the file
                copy(fileName, gamePath)

# Define the function to delete lingering igb files
def deleteLingering(fileList):
    # Delete the lingering files
    for file in fileList:
        # Check if the file name is not a none type
        if not(file == None):
            # File is not a none type
            # Check if the file exists
            if os.path.isfile(file):
                # File exists
                # Delete the file
                remove(file)