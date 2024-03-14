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
# Define the function to process skins
def skinProcessing(fullFileName, settings, XMLPath, MUAPath):
    # Determine the texture format
    textureFormat = resources.get3DTextureFormat("Skin", settings, fullFileName)
    # Confirm that a texture format was chosen
    if not(textureFormat == None):
        # A texture format was chosen
        # Get the geometry names from the file
        geomNames = resources.GetModelStats(fullFileName)
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
            XML1Name = resources.setUpFileName(fullFileName, "", settings["XML1Num"], "XX (Skin).igb")
            XML2Name = resources.setUpFileName(fullFileName, "", settings["XML2Num"], "XX (Skin).igb")
            MUA1Name = None
            MUA2Name = None
        else:
            # cel shading is not used
            # set up file names
            XML1Name = resources.setUpFileName(fullFileName, "", settings["XML1Num"], "XX (Skin - No Cel).igb")
            XML2Name = resources.setUpFileName(fullFileName, "", settings["XML2Num"], "XX (Skin - No Cel).igb")
            MUA1Name = resources.setUpFileName(fullFileName, "", settings["MUA1Num"], "XX (Skin).igb")
            MUA2Name = resources.setUpFileName(fullFileName, "", settings["MUA2Num"], "XX (Skin).igb")
        # Copy the files
        for num, name in zip([settings["XML1Num"], settings["XML2Num"], settings["MUA1Num"], settings["MUA2Num"]], [XML1Name, XML2Name, MUA1Name, MUA2Name]):
            # Determine if the number is used
            if (not(num == None) and not(name == None) and not(os.path.exists(name))):
                # Number isn't empty, need to copy
                # Perform the copying
                copy(fullFileName, name)
        # Perform the hex editing
        resources.hexEdit([settings["XML1Num"], settings["XML2Num"], settings["MUA1Num"], settings["MUA2Num"]], [XML1Name, XML2Name, MUA1Name, MUA2Name], "Skin")
        # Process the file
        complete = resources.process3D("Skin", textureFormat, XML1Name, XML2Name, MUA1Name, MUA2Name, XMLPath, MUAPath, settings)
    else:
        # A texture format was not chosen
        complete = False
    # Delete the lingering files
    resources.deleteLingering([XML1Name, XML2Name, MUA1Name, MUA2Name])
    # Return the collected value
    return complete