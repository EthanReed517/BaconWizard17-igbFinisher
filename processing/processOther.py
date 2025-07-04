# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import common
import processing
import questions
import textures
# External modules
import os.path
from shutil import copy
from pathlib import Path


# ######### #
# FUNCTIONS #
# ######### #
# Define the function for getting other model names
def otherModelNameInput(charNum, gameName, fullFileName, celExt):
    # determine what to do based on whether or not the character number is defined.
    if charNum is None:
        # Not used with this game
        # no file name is needed
        fileName = None
    else:
        # used with this game
        # Create the question
        prompt = f'What is the name of this file in the game files for {gameName}? Do not include the file extension or "No Cel". Enter a blank value if the model is not used with this game.'
        # Get the default file name
        if ' (No Cel)' in fullFileName:
            default_file_name = fullFileName.replace(' (No Cel)', '')
        else:
            default_file_name = fullFileName
        # Ask the question
        fileName = questions.pathDefault(prompt, fileNameValidator, Path(default_file_name).stem)
        # Determine if a value was entered
        if fileName == "":
            # No file name was entered
            # Set the file name to None
            fileName = None
        else:
            # Something was added
            # add the file extension
            fileName = f"{fileName}{celExt}.igb"
    # return the collected value
    return fileName

# Define the validator for the file name
def fileNameValidator(fileName):
    if ".igb" in fileName:
        return "Do not include the file extension."
    else:
        return True

# Define the function to process skins
def otherProcessing(fullFileName, settings, XMLPath, MUAPath):
    # Determine the texture format
    textureFormat = textures.get3DTextureFormat("Other", settings, fullFileName)
    # Confirm that a texture format was chosen
    if textureFormat is not None:
        # A texture format was chosen
        # Get the geometry names from the file
        geomNames = alchemy.GetModelStats(fullFileName)
        # Set the cel shading option to False initially. It could be updated to True if cel shading is detected.
        celChoice = False
        # Loop through the geometry names.
        for name in geomNames:
            # Determine if the geometry name has "_outline" in it
            if "_outline" in name:
                # "_outline" is in a geometry name, meaning that this skin has cel shading.
                # Since cel shading was detected, set the cel shading choice to True.
                celChoice = True
        # Filter based on cel shading choice
        if celChoice == True:
            # cel shading is used
            # Set up file names
            XML1Name = otherModelNameInput(settings["XML1Num"], "XML1", fullFileName, "")
            XML2Name = otherModelNameInput(settings["XML2Num"], "XML2", fullFileName, "")
            MUA1Name = None
            MUA2Name = None
            # Determine if the PSP format is used.
            if textureFormat == 'GameCube, PSP, and MUA2 PS2':
                # The PSP format is used.
                # Update the texture format to the special version for cel shading
                textureFormat = 'GameCube (Other Model with Cel)'
        else:
            # cel shading is not used
            # Determine if there will be any cel shaded assets
            if "No Cel" in fullFileName:
                # There will be a version with cel shading
                # set up file names
                XML1Name = otherModelNameInput(settings["XML1Num"], "XML1", fullFileName, " (No Cel)")
                XML2Name = otherModelNameInput(settings["XML2Num"], "XML2", fullFileName, " (No Cel)")
                # Determine if the PSP format is used
                if textureFormat == 'GameCube, PSP, and MUA2 PS2':
                    # The PSP format is used
                    # Update the texture format to the special variant that will not have " (No Cel)" in the PSP file's name
                    textureFormat = 'GameCube, PSP, and MUA2 PS2 (No Cel)'
            else:
                # There will not be a version with cel shading
                XML1Name = otherModelNameInput(settings["XML1Num"], "XML1", fullFileName, "")
                XML2Name = otherModelNameInput(settings["XML2Num"], "XML2", fullFileName, "")
            # Set up the other file names
            MUA1Name = otherModelNameInput(settings["MUA1Num"], "MUA1", fullFileName, "")
            MUA2Name = otherModelNameInput(settings["MUA2Num"], "MUA2", fullFileName, "")
        # Set up the dictionaries for processing
        numsDict = {"XML1": settings["XML1Num"], "XML2": settings["XML2Num"], "MUA1": settings["MUA1Num"], "MUA2": settings["MUA2Num"]}
        nameDict = {"XML1": XML1Name, "XML2": XML2Name, "MUA1": MUA1Name, "MUA2": MUA2Name}
        pathDict = {"XML": XMLPath, "MUA": MUAPath}
        # Process the file
        complete = processing.process3D("Other", fullFileName, textureFormat, numsDict, nameDict, pathDict)
    else:
        # A texture format was not chosen
        complete = False
    # Delete the lingering files
    common.deleteLingering([XML1Name, XML2Name, MUA1Name, MUA2Name])
    # Return the collected value
    return complete