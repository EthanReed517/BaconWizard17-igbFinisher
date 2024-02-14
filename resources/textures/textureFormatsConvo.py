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
def getConvoTextureFormat(settings):
    # Determine if any transparency was used
    portraitType = resources.select("What type of portrait is this?", ["Standard Style", "MUA1 Next-Gen Style"])
    # Determine the texture size
    textureSize = resources.selectDefault("What is the original size of the .xcf file of the texture?", ["64x64", "128x128", "256x256 or above"], "128x128")
    # Filter based on portrait type
    if portraitType == "Standard Style":
        # Standard portrait
        # Filter by texture size
        if textureSize == "64x64":
            # Console resolution
            # Determine which consoles are in use
            if settings["pcOnly"] == False:
                # All consoles
                # Create the list
                textureFormatList = ["Main"]
                # Determine if the MUA-specific format should be used
                if (not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")):
                    # MUA is in use
                    # Add the format
                    textureFormatList.append("Wii")
            else:
                # PC only
                # Create the list
                textureFormatList = []
                # Determine if XML2 PC and MUA1 PC are in use
                if (not(settings["XML2Num"] == "") or not(settings["MUA1Num"] == "")):
                    # A PC-compatible console is in use
                    # Add the format
                    textureFormatList.append("PC")
                # Determine if MUA1 is in use
                if not(settings["MUA1Num"] == ""):
                    # MUA1 is in use
                    # Add the Steam format
                    textureFormatList.append("Steam")
        elif textureSize == "128x128":
            # SD resolution
            # Determine which consoles are in use
            if settings["pcOnly"] == False:
                # All consoles
                # Create the list
                textureFormatList = ["Main except PSP"]
                # Determine if the MUA-specific format should be used
                if (not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")):
                    # MUA is in use
                    # Add the formats
                    textureFormatList.extend(["Wii", "PSP"])
            else:
                # PC only
                # Create the list
                textureFormatList = []
                # Determine if XML2 PC and MUA1 PC are in use
                if (not(settings["XML2Num"] == "") or not(settings["MUA1Num"] == "")):
                    # A PC-compatible console is in use
                    # Add the format
                    textureFormatList.append("PC")
                # Determine if MUA1 is in use
                if not(settings["MUA1Num"] == ""):
                    # MUA1 is in use
                    # Add the Steam format
                    textureFormatList.append("Steam")   
        else:
            # HD resolution and above
            # Initialize the list
            textureFormatList = []
            # Determine if the XML2-specific format is needed
            if not(settings["XML2Num"] == ""):
                # XML2 is in use
                # Add the format
                textureFormatList.append("XML2 PC")
            # Determine which consoles are in use
            if settings["pcOnly"] == False:
                # All consoles
                # Determine if the MUA1-specific format is needed
                if not(settings["MUA1Num"] == ""):
                    # MUA1 is in use
                    # Add the format
                    textureFormatList.append("MUA1 PC and Next-Gen")
                # Determine if the MUA-specific format is needed
                if (not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")):
                    # MUA is in use
                    # Add the formats
                    textureFormatList.append("Wii")
                # Add the common format
                textureFormatList.append("GC, PS2, and Xbox")
            else:
                # PC only
                # Determine if the MUA1-specific format is needed
                if not(settings["MUA1Num"] == ""):
                    # MUA1 is in use
                    # Add the format
                    textureFormatList.append("MUA1 PC and Steam")
    else:
        # Next-gen style
        # Filter by texture size
        if textureSize == "64x64":
            # Console resolution
            # Determine which consoles are in use
            if settings["pcOnly"] == False:
                # All consoles
                # Create the list
                textureFormatList = ["All"]
            else:
                # PC only
                # Create the list
                textureFormatList = []
                # Determine if XML2 PC and MUA1 PC are in use
                if (not(settings["XML2Num"] == "") or not(settings["MUA1Num"] == "")):
                    # A PC-compatible console is in use
                    # Add the format
                    textureFormatList.append("PC and Steam")
        elif textureSize == "128x128":
            # SD resolution
            # Determine which consoles are in use
            if settings["pcOnly"] == False:
                # All consoles
                # Create the list
                textureFormatList = ["All except PSP"]
                # Determine if the MUA-specific format is needed
                if (not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")):
                    # MUA is in use
                    # Add the formats
                    textureFormatList.append("PSP")
            else:
                # PC only
                # Create the list
                textureFormatList = []
                # Determine if XML2 PC and MUA1 PC are in use
                if (not(settings["XML2Num"] == "") or not(settings["MUA1Num"] == "")):
                    # A PC-compatible console is in use
                    # Add the format
                    textureFormatList.append("PC and Steam")
        else:
            # HD resolution and above
            # Determine which consoles are in use
            if settings["pcOnly"] == False:
                # Create the list
                textureFormatList = []
                # Determine if XML2 PC and MUA1 PC are in use
                if (not(settings["XML2Num"] == "") or not(settings["MUA1Num"] == "")):
                    # A PC-compatible console is in use
                    # Add the format
                    textureFormatList.append("PC and Next-Gen")
                # Add the common format
                textureFormatList.append("Last-Gen")
                # Determine if the MUA-specific format is needed
                if (not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")):
                    # MUA is in use
                    # Add the formats
                    textureFormatList.append("PSP")
            else:
                # PC only
                # Create the list
                textureFormatList = []
                # Determine if XML2 PC and MUA1 PC are in use
                if (not(settings["XML2Num"] == "") or not(settings["MUA1Num"] == "")):
                    # A PC-compatible console is in use
                    # Add the format
                    textureFormatList.append("PC and Steam")
    # Get the texture format from the list
    textureFormat = resources.getTextureFormatFromList(textureFormatList)
    # Return the collected value
    return textureFormat, portraitType