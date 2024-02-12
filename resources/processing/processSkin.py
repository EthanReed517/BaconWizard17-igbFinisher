# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Resources for this program
import resources
# To be able to perform os operations
import os
# To be able to perform shell operations
import shutil


# ######### #
# FUNCTIONS #
# ######### #
# Define the function to process skins
def skinProcessing(assetType, fullFileName, XML1Num, XML2Num, MUA1Num, MUA2Num, XMLPath, MUAPath, pcOnly, hexEditChoice, runAlchemyChoice):
    # Determine the texture format
    textureFormat = resources.get3DTextureFormat(assetType, XML2Num, MUA1Num, MUA2Num, pcOnly)
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
            XML1Name = os.path.join(os.path.dirname(fullFileName), XML1Num + "XX (Skin).igb")
            XML2Name = os.path.join(os.path.dirname(fullFileName), XML2Num + "XX (Skin).igb")
            MUA1Name = None
            MUA2Name = None
        else:
            # cel shading is not used
            # set up file names
            XML1Name = os.path.join(os.path.dirname(fullFileName), XML1Num + "XX (Skin - No Cel).igb")
            XML2Name = os.path.join(os.path.dirname(fullFileName), XML2Num + "XX (Skin - No Cel).igb")
            MUA1Name = os.path.join(os.path.dirname(fullFileName), MUA1Num + "XX (Skin).igb")
            MUA2Name = os.path.join(os.path.dirname(fullFileName), MUA2Num + "XX (Skin).igb")
        # Copy the files
        for num, name in zip([XML1Num, XML2Num, MUA1Num, MUA2Num], [XML1Name, XML2Name, MUA1Name, MUA2Name]):
            # Determine if the number is used
            if (not(num == "") and not(name == None) and not(os.path.exists(name))):
                # Number isn't empty, need to copy
                # Perform the copying
                shutil.copy(fullFileName, name)
        # Determine if hex editing is needed
        if hexEditChoice == True:
            # Hex editing is needed
            # Perform the hex editing
            resources.hexEdit([XML1Num, XML2Num, MUA1Num, MUA2Num], [XML1Name, XML2Name, MUA1Name, MUA2Name], assetType)
        # Process the file
        complete = resources.process3D(assetType, textureFormat, XML1Name, XML2Name, MUA1Name, MUA2Name, MUA1Num, MUA2Num, XMLPath, MUAPath, runAlchemyChoice)
    else:
        # A texture format was not chosen
        complete = false
    # Delete the lingering files
    resources.deleteLingering([XML1Name, XML2Name, MUA1Name, MUA2Name])
    # Return the collected value
    return complete