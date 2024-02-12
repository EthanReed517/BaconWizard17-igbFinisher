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
# Define the function for getting other model names
def otherModelNameInput(charNum, gameName, fullFileName, celExt):
    # determine what to do based on whether or not the character number is defined.
    if charNum == "":
        # Not used with this game
        # no file name is needed
        fileName = None
    else:
        # used with this game
        # Create the question
        prompt = "What is the name of this file for " + gameName + "? Do not include the file extension."
        # Ask the question
        fileName = resources.path(prompt, fileNameValidator)
        # add the file extension
        fileName = os.path.join(os.path.dirname(fullFileName), fileName + celExt + ".igb")
    # return the collected value
    return fileName

# Define the validator for the file name
def fileNameValidator(fileName):
    if len(fileName) == 0:
        return "Please enter a file name."
    elif ".igb" in fileName:
        return "Do not include the file extension."
    else:
        return True

# Define the function to process skins
def otherProcessing(assetType, fullFileName, XML1Num, XML2Num, MUA1Num, MUA2Num, XMLPath, MUAPath, pcOnly, hexEditChoice, runAlchemyChoice):
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
            celChoice = resources.confirm("Does the model use cel shading?", False)
            # Determine if there will be a version with cel shading if this doesn't
            if celChoice == False:
                # Doesn't use cel shading
                # Ask if any version will
                celAny = resources.confirm("Will there be a version with cel shading?", False)
        # Filter based on cel shading choice
        if celChoice == True:
            # cel shading is used
            # Set up file names
            XML1Name = otherModelNameInput(XML1Num, "XML1", fullFileName, "")
            XML2Name = otherModelNameInput(XML2Num, "XML2", fullFileName, "")
            MUA1Name = None
            MUA2Name = None
        else:
            # cel shading is not used
            # Determine if there will be any cel shaded assets
            if celAny == True:
                # There will be a version with cel shading
                # set up file names
                XML1Name = otherModelNameInput(XML1Num, "XML1", fullFileName, " (No Cel)")
                XML2Name = otherModelNameInput(XML2Num, "XML2", fullFileName, " (No Cel)")
            else:
                # There will not be a version with cel shading
                XML1Name = otherModelNameInput(XML1Num, "XML1", fullFileName, "")
                XML2Name = otherModelNameInput(XML2Num, "XML2", fullFileName, "")
            # Set up the other file names
            MUA1Name = otherModelNameInput(MUA1Num, "MUA1", fullFileName, "")
            MUA2Name = otherModelNameInput(MUA2Num, "MUA2", fullFileName, "")
        # Copy the files
        for num, name in zip([XML1Num, XML2Num, MUA1Num, MUA2Num], [XML1Name, XML2Name, MUA1Name, MUA2Name]):
            # Determine if the number is used and the file doesn't exist
            if (not(num == "") and not(name == None) and not(os.path.exists(name))):
                # Number isn't empty, need to copy
                # Perform the copying
                shutil.copy(fullFileName, name)
        # Process the file
        complete = resources.process3D(assetType, textureFormat, XML1Name, XML2Name, MUA1Name, MUA2Name, MUA1Num, MUA2Num, XMLPath, MUAPath, runAlchemyChoice)
    else:
        # A texture format was not chosen
        complete = false
    # Delete the lingering files
    resources.deleteLingering([XML1Name, XML2Name, MUA1Name, MUA2Name])
    # Return the collected value
    return complete