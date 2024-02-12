# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Resources for this program
import resources


# ######### #
# FUNCTIONS #
# ######### #
# Define the function for getting the texture format from the list.
def getTextureFormatFromList(textureFormatList):
    # Determine how many texture format options there are
    if len(textureFormatList) > 1:
        # Multiple options
        # Ask which texture format was used
        textureFormat = resources.select("What texture format was used for this asset?", textureFormatList)
    elif len(textureFormatList) == 0:
        # No texture was chosen
        # Print an error message
        resources.printError("ERROR: Choice of settings and assets did not produce a possible texture format. Please make sure the proper character numbers are filled out, double check your answers to the previous questions, and try again.")
        # Set no texture format
        textureFormat = None
        # Wait for the user to acknowledge the error
        resources.pressAnyKey(None)
    else:
        # Only one option was available
        # Automatically set the option
        textureFormat = textureFormatList[0]
    # Return the collected value
    return textureFormat