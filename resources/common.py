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
# To be able to make folders and delete files
from os import mkdir, remove
# To be able to perform shell operations
from shutil import copy


# ######### #
# FUNCTIONS #
# ######### #
# Define the function to copy files to the necessary destination
def copyToDestination(fileName, releasePath, folderName):
    # Verify that the file name is not a None
    if not(fileName == None):
        # File name is not none
        # Verify that the file exists before copying
        if os.path.isfile(fileName):
            # The file exists
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