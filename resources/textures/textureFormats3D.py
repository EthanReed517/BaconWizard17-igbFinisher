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
def get3DTextureFormat(assetType, settings):
    # Determine the texture size
    textureSize = resources.select("What is the original size of the .xcf file of the main texture?", ["256x256 or less", "Over 256x256"])
    # Determine if any transparency was used
    someTransparent = resources.confirm("Does this texture use any transparent textures (plain .png or DXT5 .dds)?", False)
    # Determine next question based on response
    if someTransparent == True:
        # Yes, at least some transparent
        # Print the warning message about transparent textures
        resources.printWarning("WARNING: It is strongly recommended to do any compatibility operations (i.e., converting igBlend to igAlpha) on the transparent texture prior to running igbFinisher. This program does not do that for you.")
        # Determine if transparency was used on all textures
        transparent = resources.confirm("Does this texture only use transparent textures (plain .png or DXT5 .dds)?", False)
    else:
        # No transparency
        # Set the transparent variable
        transparent = False
    # Determine if this is transparent and oversized
    if ((textureSize == "Over 256x256") and (transparent == True) and (settings["pcOnly"] == False)):
        # Oversized and transparent
        # Determine if this is a big character
        bigChar = resources.confirm("Is this a large character?", False)
    else:
        # Not transparent and oversized
        # Doesn't matter if it's a big character, set false
        bigChar = False
    # Determine if transparency was used
    envMaps = resources.confirm("Were environment maps used?", False)
    # Determine if it's necessary to ask about secondary skins
    if ((textureSize == "256x256 or less") and (settings["pcOnly"] == False) and not(assetType == "Other")):
        # Need to ask about secondary skins
        # Determine if this is a primary or secondary skin
        skinType = resources.select("Is this for a primary skin or secondary skin?", ["Primary skin", "Secondary skin"])
    else:
        # Do not need to ask about a secondary skin
        # Treat it like a primary skin
        skinType = "Primary skin"
    # Determine if this should be treated as a primary or secondary skin
    if skinType == "Primary skin":
        # Treat like a primary skin
        # Determine the main texture size
        if textureSize == "256x256 or less":
            # Standard sized texture
            # Determine if there are transparent textures
            if transparent == False:
                # No transparent textures
                # Determine if environment maps are used
                if envMaps == False:
                    # No environment maps
                    # Determine if this is for PC or no
                    if settings["pcOnly"] == False:
                        # For all consoles
                        # Initialize the list with the main format
                        textureFormatList = ["PC, PS2, Xbox, and MUA1 360"]
                        # Determine if MUA1/MUA2-specific format is needed
                        if ((not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")) and not(assetType == "3D Head")):
                            # MUA1 or MUA2 are in use
                            # Add the texture option
                            textureFormatList.append("Wii")
                        # Add the remaining texture option
                        textureFormatList.append("GameCube, PSP, and MUA2 PS2")
                    else:
                        # For PC only
                        # Determine if XML2 PC and MUA1 PC are in use
                        if (not(settings["XML2Num"] == "") or not(settings["MUA1Num"] == "")):
                            # A PC-compatible console is in use
                            # Initialize the list with the main format
                            textureFormatList = ["PC"]
                        else:
                            # PC not in use
                            textureFormatList = []
                else:
                    # Has environment maps
                    # Determine if this is for PC or no
                    if settings["pcOnly"] == False:
                        # For all consoles
                        # Initialize the list with the main format
                        textureFormatList = ["Main texture: PC, PS2, Xbox, and MUA1 360 / Environment Texture: PC and MUA1 360"]
                        # Add the Xbox-specific format
                        textureFormatList.append("Main texture: PC, PS2, Xbox, and MUA1 360 / Environment Texture: Xbox")
                        # Add the PS2-specific format
                        textureFormatList.append("Main texture: PC, PS2, Xbox, and MUA1 360 / Environment Texture: PS2")
                        # Determine if MUA1/MUA2-specific format is needed
                        if ((not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")) and not(assetType == "3D Head")):
                            # MUA1 or MUA2 are in use
                            # Add the texture option
                            textureFormatList.append("Main texture: Wii / Environment Texture: Wii")
                        # Add the remaining texture option
                        textureFormatList.append("Main texture: GameCube, PSP, and MUA2 PS2 / Environment Texture: GameCube, PSP, and MUA2 PS2")
                    else:
                        # For PC only
                        # Determine if XML2 PC and MUA1 PC are in use
                        if (not(settings["XML2Num"] == "") or not(settings["MUA1Num"] == "")):
                            # A PC-compatible console is in use
                            # Initialize the list with the main format
                            textureFormatList = ["Main texture: PC / Environment Texture: PC"]
                        else:
                            # PC not in use
                            textureFormatList = []
            else:
                # Transparent textures
                # Determine if environment maps are used
                if envMaps == False:
                    # No environment maps
                    # Determine if this is for PC or no
                    if settings["pcOnly"] == False:
                        # For all consoles
                        # Initialize the list with the two formats
                        textureFormatList = ["PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360", "GameCube, PSP, and MUA2 PS2"]
                    else:
                        # For PC only
                        # Determine if XML2 PC and MUA1 PC are in use
                        if (not(settings["XML2Num"] == "") or not(settings["MUA1Num"] == "")):
                            # A PC-compatible console is in use
                            # Initialize the list with the main format
                            textureFormatList = ["PC and MUA1 Steam"]
                        else:
                            # PC not in use
                            textureFormatList = []
                else:
                    # Has environment maps
                    # Determine if this is for PC or no
                    if settings["pcOnly"] == False:
                        # For all consoles
                        # Initialize the list with the main format
                        textureFormatList = ["Main texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment Texture: PC and MUA1 360"]
                        # Add the Xbox-specific format
                        textureFormatList.append("Main texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment Texture: Xbox")
                        # Add the PS2-specific format
                        textureFormatList.append("Main texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment Texture: PS2")
                        # Determine if MUA1/MUA2-specific format is needed
                        if ((not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")) and not(assetType == "3D Head")):
                            # MUA1 or MUA2 are in use
                            # Add the texture option
                            textureFormatList.append("Main texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment Texture: Wii")
                        # Add the remaining texture option
                        textureFormatList.append("Main texture: GameCube, PSP, and MUA2 PS2 / Environment Texture: GameCube, PSP, and MUA2 PS2")
                    else:
                        # For PC only
                        # Determine if XML2 PC and MUA1 PC are in use
                        if (not(settings["XML2Num"] == "") or not(settings["MUA1Num"] == "")):
                            # A PC-compatible console is in use
                            # Initialize the list with the main format
                            textureFormatList = ["Main texture: PC and MUA1 Steam / Environment Texture: PC"]
                        else:
                            # PC not in use
                            textureFormatList = []
        else:
            # Oversized texture
            # Determine if there are transparent textures
            if transparent == False:
                # No transparent textures
                # Determine if environment maps are used
                if envMaps == False:
                    # No environment maps
                    # Determine if this is for PC or no
                    if settings["pcOnly"] == False:
                        # For all consoles
                        # Start with an empty list
                        textureFormatList = []
                        # Check if MUA1-Specific format is needed
                        if (not(settings["MUA1Num"] == "") and not(assetType == "3D Head")):
                            # MUA1 is in use
                            # Append the texture option
                            textureFormatList.append("MUA1 PC, Steam, 360, and PS3")
                        # Add remaining texture options
                        textureFormatList.extend(["XML2 PC, Xbox, and Wii", "PS2", "GameCube, PSP, and MUA2 PS2"])
                    else:
                        # For PC only
                        # Start with an empty list
                        textureFormatList = []
                        # Check if MUA1-Specific format is needed
                        if (not(settings["MUA1Num"] == "") and not(assetType == "3D Head")):
                            # MUA1 is in use
                            # Append the texture option
                            textureFormatList.append("MUA1 PC and Steam")
                        # Check if the XML2-specific format is needed
                        if (not(settings["XML2Num"] == "") and not(assetType == "Mannequin")):
                            # XML2 is in use
                            # Append the texture option
                            textureFormatList.append("XML2 PC")
                else:
                    # Has environment maps
                    # Determine if this is for PC or no
                    if settings["pcOnly"] == False:
                        # For all consoles
                        # Start with an empty list
                        textureFormatList = []
                        # Check if MUA1-Specific format is needed
                        if (not(settings["MUA1Num"] == "") and not(assetType == "3D Head")):
                            # MUA1 is in use
                            # Append the texture option
                            textureFormatList.append("Main texture: MUA1 PC, Steam, 360, and PS3 / Environment Texture: PC and MUA1 360")
                        # Check if the XML2 PC-specific option is needed
                        if (not(settings["XML2Num"] == "") and not(assetType == "Mannequin")):
                            # XML2 PC is in use
                            # Add the XML2 PC option
                            textureFormatList.append("Main texture: XML2 PC, Xbox, and Wii / Environment Texture: PC and MUA1 360")
                        # Add the Xbox option
                        textureFormatList.append("Main texture: XML2 PC, Xbox, and Wii / Environment Texture: Xbox")
                        # Check if Wii-Specific format is needed
                        if ((not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")) and not(assetType == "3D Head")):
                            # Wii is in use
                            # Add the Wii option
                            textureFormatList.append("Main texture: XML2 PC, Xbox, and Wii / Environment Texture: Wii")
                        # Add the PS2 option
                        textureFormatList.append("Main texture: PS2 / Environment Texture: PS2")
                        # Add the remaining texture option
                        textureFormatList.append("Main texture: GameCube, PSP, and MUA2 PS2 / Environment Texture: GameCube, PSP, and MUA2 PS2")
                    else:
                        # For PC only
                        # Start with an empty list
                        textureFormatList = []
                        # Check if MUA1-Specific format is needed
                        if (not(settings["MUA1Num"] == "") and not(assetType == "3D Head")):
                            # MUA1 is in use
                            # Append the texture option
                            textureFormatList.append("Main texture: MUA1 PC and Steam / Environment Texture: PC and MUA1 360")
                        # Check if the XML2-specific format is needed
                        if (not(settings["XML2Num"] == "") and not(assetType == "Mannequin")):
                            # XML2 is in use
                            # Append the texture option
                            textureFormatList.append("Main texture: XML2 PC / Environment Texture: PC and MUA1 360")
            else:
                # Transparent textures
                # Determine if environment maps are used
                if envMaps == False:
                    # No environment maps
                    # Determine if this is for PC or no
                    if settings["pcOnly"] == False:
                        # For all consoles
                        # Determine if this is a big character
                        if bigChar == False:
                            # Not a big character
                            # Initialize the list
                            textureFormatList = ["PC, Wii, Xbox, MUA1 Steam, PS3, and 360", "PS2"]
                        else:
                            # Big character
                            # Initialize the list
                            textureFormatList = ["PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360"]
                        # Regardless of character size, add GC, PSP, and MUA2 PS2
                        textureFormatList.append("GameCube, PSP, and MUA2 PS2")
                    else:
                        # For PC only
                        # Determine if XML2 PC and MUA1 PC are in use
                        if (not(settings["XML2Num"] == "") or not(settings["MUA1Num"] == "")):
                            # A PC-compatible console is in use
                            # Create the list
                            textureFormatList = ["PC and MUA1 Steam"]
                        else:
                            # PC not in use
                            textureFormatList = []
                else:
                    # Has environment maps
                    # Determine if this is for PC or no
                    if settings["pcOnly"] == False:
                        # For all consoles
                        # Determine if this is a big character
                        if bigChar == False:
                            # Not a big character
                            # Initialize the list
                            textureFormatList = ["Main Texture: PC, Wii, Xbox, MUA1 Steam, PS3, and 360 / Environment Texture: PC and MUA1 360"]
                            # Determine if the wii-specific format is needed
                            if ((not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")) and not(assetType == "3D Head")):
                                # Wii is needed
                                # Add Wii
                                textureFormatList.append("Main Texture: PC, Wii, Xbox, MUA1 Steam, PS3, and 360 / Environment Texture: Wii")
                            # Add Xbox
                            textureFormatList.append("Main Texture: PC, Wii, Xbox, MUA1 Steam, PS3, and 360 / Environment Texture: Xbox")
                            # Add PS2
                            textureFormatList.append("Main Texture: PS2 / Environment Texture: PS2")
                        else:
                            # Big character
                            # Initialize the list
                            textureFormatList = ["Main Texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment Texture: PC and MUA1 360"]
                            # Determine if the wii-specific format is needed
                            if ((not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")) and not(assetType == "3D Head")):
                                # Wii is needed
                                # Add Wii
                                textureFormatList.append("Main Texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment Texture: Wii")
                            # Add Xbox
                            textureFormatList.append("Main Texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment Texture: Xbox")
                            # Add PS2
                            textureFormatList.append("Main Texture: PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360 / Environment Texture: PS2")
                        # Regardless of character size, add GC, PSP, and MUA2 PS2
                        textureFormatList.append("Main texture: GameCube, PSP, and MUA2 PS2 / Environment Texture: GameCube, PSP, and MUA2 PS2")
                    else:
                        # For PC only
                        # For PC only
                        # Determine if XML2 PC and MUA1 PC are in use
                        if (not(settings["XML2Num"] == "") or not(settings["MUA1Num"] == "")):
                            # A PC-compatible console is in use
                            # Create the list
                            textureFormatList = ["Main texture: PC and MUA1 Steam / Environment Texture: PC and MUA1 360"]
                        else:
                            # PC not in use
                            textureFormatList = []
    else:
        # Treat like a secondary skin. You only get here if it's a skin with a standard-sized texture and the secondary option is chosen, and must be for all consoles
        # Determine if there are transparent textures
        if transparent == False:
            # No transparent textures
            # Determine if environment maps are used
            if envMaps == False:
                # No environment maps
                # Initialize the list with the main format
                textureFormatList = ["PC, Xbox, and MUA1 360"]
                # Determine if MUA1/MUA2-specific format is needed
                if ((not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")) and not(assetType == "3D Head")):
                    # MUA1 or MUA2 are in use
                    # Add the texture option
                    textureFormatList.append("Wii")
                # Add PS2
                textureFormatList.append("PS2")
                # Add the remaining texture option
                textureFormatList.append("GameCube, PSP, and MUA2 PS2")
            else:
                # Has environment maps
                # Determine if this is for PC or no
                if settings["pcOnly"] == False:
                    # For all consoles
                    # Initialize the list with the main format
                    textureFormatList = ["Main texture: PC, Xbox, and MUA1 360 / Environment Texture: PC and MUA1 360"]
                    # Add the Xbox-specific format
                    textureFormatList.append("Main texture: PC, Xbox, and MUA1 360 / Environment Texture: Xbox")
                    # Determine if MUA1/MUA2-specific format is needed
                    if ((not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")) and not(assetType == "3D Head")):
                        # MUA1 or MUA2 are in use
                        # Add the texture option
                        textureFormatList.append("Main texture: Wii / Environment Texture: Wii")
                    # Add the PS2-specific format
                    textureFormatList.append("Main texture: PS2 / Environment Texture: PS2")
                    # Add the remaining texture option
                    textureFormatList.append("Main texture: GameCube, PSP, and MUA2 PS2 / Environment Texture: GameCube, PSP, and MUA2 PS2")
        else:
            # Transparent textures
            # Determine if environment maps are used
            if envMaps == False:
                # No environment maps
                # Initialize the list with the available formats
                textureFormatList = ["PC, Wii, Xbox, MUA1 Steam, PS3, and 360", "PS2", "GameCube, PSP, and MUA2 PS2"]
            else:
                # Has environment maps
                # Initialize the list with the main format
                textureFormatList = ["Main texture: PC, Wii, Xbox, MUA1 Steam, PS3, and 360 / Environment Texture: PC and MUA1 360"]
                # Add the Xbox-specific format
                textureFormatList.append("Main texture: PC, Wii, Xbox, MUA1 Steam, PS3, and 360 / Environment Texture: Xbox")
                # Determine if MUA1/MUA2-specific format is needed
                if ((not(settings["MUA1Num"] == "") or not(settings["MUA2Num"] == "")) and not(assetType == "3D Head")):
                    # MUA1 or MUA2 are in use
                    # Add the texture option
                    textureFormatList.append("Main texture: PC, Wii, Xbox, MUA1 Steam, PS3, and 360 / Environment Texture: Wii")
                # Add the PS2-specific format
                textureFormatList.append("Main texture: PS2 / Environment Texture: PS2")
                # Add the remaining texture option
                textureFormatList.append("Main texture: GameCube, PSP, and MUA2 PS2 / Environment Texture: GameCube, PSP, and MUA2 PS2")
    # Get the texture format from the list
    textureFormat = resources.getTextureFormatFromList(textureFormatList)
    # Return the collected value
    return textureFormat