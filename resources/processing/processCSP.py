# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Modules from this program
import resources
import alchemy
import common
import questions
# Other modules
import os.path
from shutil import copy


# ######### #
# FUNCTIONS #
# ######### #
# Define the function to export the portraits
def processCSP(textureFormat, XML1Name, XML2Name, XMLPath, portraitType):
    # Initialize the completion variable
    complete = True
    # Filter by texture type
    if "All" in textureFormat:
        # Common format
        # Copy the files
        common.copyToDestination(XML1Name, XMLPath, "for XML1 (GC)")
        common.copyToDestination(XML1Name, XMLPath, "for XML1 (PS2 and Xbox)")
        common.copyToDestination(XML2Name, XMLPath, "for XML2 (GC)")
        common.copyToDestination(XML2Name, XMLPath, "for XML2 (PC, PS2, and Xbox)")
        # Determine if PSP is included
        if not("except PSP" in textureFormat):
            # PSP is included
            # Optimize the file for XML2 PSP
            alchemy.callAlchemy(XML2Name, "stat2.ini")
            # Copy the file for XML2 PSP
            common.copyToDestination(XML2Name, XMLPath, "for XML2 (PSP)")            
    elif textureFormat == "GC, PS2, and Xbox":
        # Console format for XML2 HD
        # Copy the files
        common.copyToDestination(XML2Name, XMLPath, "for XML2 (GC)")
        common.copyToDestination(XML2Name, XMLPath, "for XML2 (PS2 and Xbox)")
    elif textureFormat == "PSP":
        # PSP-only format
        # Optimize the file for XML2 PSP
        alchemy.callAlchemy(XML2Name, "stat2.ini")
        # Copy the file for XML2 PSP
        common.copyToDestination(XML2Name, XMLPath, "for XML2 (PSP)")
    elif textureFormat == "PC":
        # PC only format
        # Copy the files
        common.copyToDestination(XML1Name, XMLPath, "for XML2 (PC)")
    else:
        # None of the above
        # Display an error message
        questions.printError("Choice of texture format did not line up with an existing operation. Selected texture format: " + textureFormat, True)
        # Set the completion status
        complete = False
        # Wait for the user to acknowledge the error
        questions.pressAnyKey(None)
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
            XML1Name = common.setUpFileName(fullFileName, "", settings["XML1Num"][0:-2], "XX (Character Select Portrait).igb")
            XML2Name = None
        else:
            # XML2 portrait
            # Set up file names
            XML1Name = None
            XML2Name = common.setUpFileName(fullFileName, "", settings["XML2Num"][0:-2], "XX (Character Select Portrait).igb")
        # Copy the files
        for num, name in zip([settings["XML1Num"], settings["XML2Num"]], [XML1Name, XML2Name]):
            # Determine if the number is used
            if (not(num == None) and not(name == None) and not(os.path.exists(name))):
                # Number isn't empty, need to copy
                # Perform the copying
                copy(fullFileName, name)
        # Process the file
        complete = processCSP(textureFormat, XML1Name, XML2Name, XMLPath, portraitType)
        # Delete the lingering files
        common.deleteLingering([XML1Name, XML2Name])
    else:
        # A texture format was not chosen
        complete = False
    # Return the collected value
    return complete