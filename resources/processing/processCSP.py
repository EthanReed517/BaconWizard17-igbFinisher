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
# Define the function to export the portraits
def processCSP(textureFormat, XML1Name, XML2Name, XMLPath, portraitType):
    # Initialize the completion variable
    complete = True
    # Filter by texture type
    if textureFormat == "All":
        # Common format
        # Copy the files
        resources.copyToDestination(XML1Name, XMLPath, "for XML1 (GC)")
        resources.copyToDestination(XML1Name, XMLPath, "for XML1 (PS2 and Xbox)")
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (GC)")
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC, PS2, and Xbox)")
    elif textureFormat == "Consoles":
        # Console format for XML2 HD
        # Copy the files
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (GC)")
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PS2 and Xbox)")
    elif textureFormat == "PC":
        # PC only format
        # Copy the files
        resources.copyToDestination(XML1Name, XMLPath, "for XML2 (PC)")
    else:
        # None of the above
        # Display an error message
        resources.printError("Choice of texture format did not line up with an existing operation. Selected texture format: " + textureFormat, True)
        # Set the completion status
        complete = False
        # Wait for the user to acknowledge the error
        resources.pressAnyKey(None)
    # Return the completion variable
    return complete

# Define the function to process conversation portraits
def CSPProcessing(fullFileName, settings, XMLPath):
    # Determine the texture format
    (textureFormat, portraitType) = resources.getCSPTextureFormat(settings, fullFileName)
    # Confirm that a texture format was chosen
    if not(textureFormat == None):
        # A texture format was chosen
        # Determine the portrait type
        if portraitType == "XML1":
            # XML1 portrait
            # Set up file names
            XML1Name = os.path.join(os.path.dirname(fullFileName), settings["XML1Num"] + "XX (Character Select Portrait).igb")
            XML2Name = None
        else:
            # XML2 portrait
            # Set up file names
            XML1Name = None
            XML2Name = os.path.join(os.path.dirname(fullFileName), settings["XML2Num"] + "XX (Character Select Portrait).igb")
        # Copy the files
        for num, name in zip([settings["XML1Num"], settings["XML2Num"]], [XML1Name, XML2Name]):
            # Determine if the number is used
            if (not(num == "") and not(name == None) and not(os.path.exists(name))):
                # Number isn't empty, need to copy
                # Perform the copying
                copy(fullFileName, name)
        # Process the file
        complete = processCSP(textureFormat, XML1Name, XML2Name, XMLPath, portraitType)
    else:
        # A texture format was not chosen
        complete = False
    # Delete the lingering files
    resources.deleteLingering([XML1Name, XML2Name])
    # Return the collected value
    return complete