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
# Define the function to get texture formats for 3D assets
def getCSPTextureFormat(XML1Num, XML2Num, pcOnly):
    # Determine if any transparency was used
    portraitType = resources.select("What game is the portrait for?", ["XML1", "XML2"])
    # Determine the texture size
    textureSize = resources.selectDefault("What is the original size of the .xcf file of the texture?", ["64x64", "128x128", "256x256 or above"], "128x128")
    # Filter based on portrait type
    if portraitType == "XML1":
        # XML1
        # Determine if this is PC only and if an XML1 number is present
        if ((pcOnly == False) and not(XML1Num == "")):
            # Not PC only and XML1 is in use
            # Create the list
            textureFormatList = ["All"]
        else:
            # PC only or no XML1 number
            # Empty list
            textureFormatList = []
    else:
        # XML2
        # Make sure that there's an XML2 number
        if not(XML2Num == ""):
            # XML2 is in use
            # Filter by texture size
            if ((textureSize == "64x64") or (textureSize == "128x128")):
                # Console or SD resolution
                # Determine the console
                if pcOnly == False:
                    # All consoles
                    # Create the list
                    textureFormatList = ["All"]
                else:
                    # PC only
                    # Create the list
                    textureFormatList = ["PC"]
            else:
                # HD resolution
                # Create the list
                textureFormatList = ["PC"]
                # Determine the console
                if pcOnly == False:
                    # All consoles
                    textureFormatList.append("Consoles")
        else:
            # XML2 is not in use
            # Create an empty list
            textureFormatList = []
    # Get the texture format from the list
    textureFormat = resources.getTextureFormatFromList(textureFormatList)
    # Return the collected value
    return textureFormat, portraitType