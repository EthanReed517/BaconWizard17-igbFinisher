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
        # Determine if cel shading needs to be asked about
        if ((textureFormat == "Wii") or ("Environment Texture: Wii" in textureFormat) or ("MUA1 PC" in textureFormat)):
            # Texture format that would not use cel shading
            celChoice = False
        else:
            # Texture format that could be with a cel shaded skin
            # Determine if the skin has cel shading or not
            celChoice = resources.confirm("Does the skin use cel shading?", False)
        # Filter based on cel shading choice
        if celChoice == True:
            # cel shading is used
            # Set up file names
            XML1Name = os.path.join(os.path.dirname(fullFileName), settings["XML1Num"] + "XX (Skin).igb")
            XML2Name = os.path.join(os.path.dirname(fullFileName), settings["XML2Num"] + "XX (Skin).igb")
            MUA1Name = None
            MUA2Name = None
        else:
            # cel shading is not used
            # set up file names
            XML1Name = os.path.join(os.path.dirname(fullFileName), settings["XML1Num"] + "XX (Skin - No Cel).igb")
            XML2Name = os.path.join(os.path.dirname(fullFileName), settings["XML2Num"] + "XX (Skin - No Cel).igb")
            MUA1Name = os.path.join(os.path.dirname(fullFileName), settings["MUA1Num"] + "XX (Skin).igb")
            MUA2Name = os.path.join(os.path.dirname(fullFileName), settings["MUA2Num"] + "XX (Skin).igb")
        # Copy the files
        for num, name in zip([settings["XML1Num"], settings["XML2Num"], settings["MUA1Num"], settings["MUA2Num"]], [XML1Name, XML2Name, MUA1Name, MUA2Name]):
            # Determine if the number is used
            if (not(num == "") and not(name == None) and not(os.path.exists(name))):
                # Number isn't empty, need to copy
                # Perform the copying
                copy(fullFileName, name)
        # Perform the hex editing
        resources.hexEdit([settings["XML1Num"], settings["XML2Num"], settings["MUA1Num"], settings["MUA2Num"]], [XML1Name, XML2Name, MUA1Name, MUA2Name], "Skin")
        # Process the file
        complete = resources.process3D("Skin", textureFormat, XML1Name, XML2Name, MUA1Name, MUA2Name, XMLPath, MUAPath, settings)
    else:
        # A texture format was not chosen
        complete = false
    # Delete the lingering files
    resources.deleteLingering([XML1Name, XML2Name, MUA1Name, MUA2Name])
    # Return the collected value
    return complete