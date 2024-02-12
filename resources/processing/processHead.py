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
def headProcessing(assetType, fullFileName, XML1Num, XML2Num, MUA1Num, MUA2Num, XMLPath, MUAPath, pcOnly, hexEditChoice, runAlchemyChoice):
    # Determine the texture format
    textureFormat = resources.get3DTextureFormat(assetType, XML2Num, MUA1Num, MUA2Num, pcOnly)
    # Confirm that a texture format was chosen
    if not(textureFormat == None):
        # A texture format was chosen
        # Set up the file names
        XML1Name = os.path.join(os.path.dirname(fullFileName), XML1Num + "XX (3D Head).igb")
        XML2Name = os.path.join(os.path.dirname(fullFileName), XML2Num + "XX (3D Head).igb")
        MUA1Name = None
        MUA2Name = None
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