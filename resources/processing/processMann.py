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
def mannProcessing(assetType, fullFileName, XML1Num, XML2Num, MUA1Num, MUA2Num, XMLPath, MUAPath, pcOnly, hexEditChoice, runAlchemyChoice, multiPose):
    # Determine the texture format
    textureFormat = resources.get3DTextureFormat(assetType, XML2Num, MUA1Num, MUA2Num, pcOnly)
    # Confirm that a texture format was chosen
    if not(textureFormat == None):
        # A texture format was chosen
        # Filter names based on whether or not the character uses multiple mannequin poses
        if multiPose == True:
            # Character uses multiple poses
            # determine the pose name
            mannequinPose = resources.select("Which mannequin pose is being used?", ["MUA1 Pose", "MUA1 Last-Gen Pose", "MUA1 Next-Gen Pose", "MUA2 Pose", "OCP Pose", "Custom Pose"])
            # Set up file names
            MUA1Name = os.path.join(os.path.dirname(fullFileName), MUA1Num + "XX (Mannequin - " + mannequinPose + ").igb")
            MUA2Name = os.path.join(os.path.dirname(fullFileName), MUA2Num + "XX (Mannequin - " + mannequinPose + ").igb")
        else:
            # Character uses one pose
            # set up file names
            MUA1Name = os.path.join(os.path.dirname(fullFileName), MUA1Num + "XX (Mannequin).igb")
            MUA2Name = os.path.join(os.path.dirname(fullFileName), MUA2Num + "XX (Mannequin).igb")
        # Set the XML1/XML2 names
        XML1Name = None
        XML2Name = None
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