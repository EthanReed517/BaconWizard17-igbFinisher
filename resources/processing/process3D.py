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
# Define the function for processing assets
def process3D(assetType, textureFormat, XML1Name, XML2Name, MUA1Name, MUA2Name, XMLPath, MUAPath, settings):
    # Determine the asset type
    if assetType == "Skin":
        # This is a skin
        # Set the ini prefix
        iniPrefix = "skin"
    else:
        # Not a skin
        # Set the ini prefix
        iniPrefix = "stat"
    # Initialize the completion variable
    complete = True
    # Filter by texture type
    if (("PC, PS2, Xbox, and MUA1 360" in textureFormat) or ("PC, Xbox, and MUA1 360" in textureFormat)):
        # The main texture type
        # Determine if environment maps are used
        if not("Environment Texture" in textureFormat):
            # No environment maps
            # Determine if PS2 should be included
            if ("PS2" in textureFormat):
                # Has PS2 (Primary skin)
                # Copy the files that don't need optimization
                resources.copyToDestination(XML1Name, XMLPath, "for XML1 (PS2 and Xbox)")
                resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC, PS2, and Xbox)")
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2 and Xbox)")
            else:
                # No PS2 (Secondary skin)
                # Copy any files that don't need optimization.
                resources.copyToDestination(XML1Name, XMLPath, "for XML1 (Xbox)")
                resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC and Xbox)")
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Xbox)")
            # Perform the first Alchemy operation
            resources.callAlchemy(MUA1Name, iniPrefix + "1-1.ini")
            # Copy the first optimized alchemy file
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC and 360)")
            # Perform the second Alchemy operation
            resources.callAlchemy(MUA1Name, iniPrefix + "1-2.ini")
            # Copy the second optimized alchemy file
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Steam and PS3)")
        else:
            # Has environment maps
            # Filter based on environment map type
            if ("Environment Texture: PC and MUA1 360" in textureFormat):
                # PC and MUA1 360
                # Copy the XML2 PC file
                resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC)")
                # Perform the first Alchemy operation
                resources.callAlchemy(MUA1Name, iniPrefix + "1-1.ini")
                # Copy the first optimized alchemy file
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC and 360)")
                # Perform the second Alchemy operation
                resources.callAlchemy(MUA1Name, iniPrefix + "1-2.ini")
                # Copy the second optimized alchemy file
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Steam and PS3)")
            elif ("Environment Texture: Xbox" in textureFormat):
                # Xbox
                # Copy the files
                resources.copyToDestination(XML1Name, XMLPath, "for XML1 (Xbox)")
                resources.copyToDestination(XML2Name, XMLPath, "for XML2 (Xbox)")
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Xbox)")
            else:
                # PS2
                # Copy the files
                resources.copyToDestination(XML1Name, XMLPath, "for XML1 (PS2)")
                resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PS2)")
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2)")
    elif ((textureFormat == "Wii") or ("Environment Texture: Wii" in textureFormat)):
        # Wii stuff
        # Check if the MUA1 and MUA2 numbers are the same
        if settings["MUA1Num"] == settings["MUA2Num"]:
            # MUA1 and MUA2 are the same
            # Copy the files
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii) and MUA2 (Wii)")
        else:
            # MUA1 and MUA2 are not the same
            # Copy the files
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii)")
            resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
    elif textureFormat == "PS2":
        # PS2 only
        # Copy the files
        resources.copyToDestination(XML1Name, XMLPath, "for XML1 (PS2)")
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PS2)")
        resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2)")
    elif "GameCube, PSP, and MUA2 PS2" in textureFormat:
        # GameCube, PSP, and MUA2 PS2
        # Copy the files that don't need optimization
        resources.copyToDestination(XML1Name, XMLPath, "for XML1 (GC)")
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (GC)")
        # Check if the MUA1 and MUA2 numbers are the same
        if settings["MUA1Num"] == settings["MUA2Num"]:
            # MUA1 and MUA2 are the same
            # Run alchemy
            resources.callAlchemy(MUA1Name, iniPrefix + "3.ini")
            # Copy the files
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP) and MUA2 (PSP)")
            resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (PS2)")
        else:
            # MUA1 and MUA2 are not the same
            # Run alchemy
            resources.callAlchemy(MUA1Name, iniPrefix + "3.ini")
            resources.callAlchemy(MUA2Name, iniPrefix + "3.ini")
            # Copy the files
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP)")
            resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (PSP)")
            resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (PS2)")
    elif (("PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360" in textureFormat) or ("PC, Wii, Xbox, MUA1 Steam, PS3, and 360" in textureFormat)):
        # Transparent common texture
        # Determine if the skin has environment maps
        if not("Environment Texture" in textureFormat):
            # No environment maps
            # Determine if PS2 should be included
            if "PS2" in textureFormat:
                # Has PS2
                # Copy the files that don't need optimization
                resources.copyToDestination(XML1Name, XMLPath, "for XML1 (PS2 and Xbox)")
                resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC, PS2, and Xbox)")
                # Check if the MUA1 and MUA2 numbers are the same
                if settings["MUA1Num"] == settings["MUA2Num"]:
                    # MUA1 and MUA2 are the same
                    # Copy the files
                    resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2, Wii, and Xbox) and MUA2 (Wii)")
                else:
                    # MUA1 and MUA2 are not the same
                    # Copy the files
                    resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2, Wii, and Xbox)")
                    resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
            else:
                # No PS2 (Secondary skin)
                # Copy any files that don't need optimization.
                resources.copyToDestination(XML1Name, XMLPath, "for XML1 (Xbox)")
                resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC and Xbox)")
                # Check if the MUA1 and MUA2 numbers are the same
                if settings["MUA1Num"] == settings["MUA2Num"]:
                    # MUA1 and MUA2 are the same
                    # Copy the files
                    resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii and Xbox) and MUA2 (Wii)")
                else:
                    # MUA1 and MUA2 are not the same
                    # Copy the files
                    resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii and Xbox)")
                    resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
            # Perform the Alchemy operation
            resources.callAlchemy(MUA1Name, iniPrefix + "1-1.ini")
            # Copy the optimized file
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC, Steam, PS3, and 360)")
        else:
            # Has environment maps
            # Filter based on environment map type
            if ("Environment Texture: PC and MUA1 360" in textureFormat):
                # PC and MUA1 360
                # Copy the XML2 PC file
                resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC)")
                # Perform the first Alchemy operation
                resources.callAlchemy(MUA1Name, iniPrefix + "1-1.ini")
                # Copy the first optimized alchemy file
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC, Steam, PS3, and 360)")
            elif ("Environment Texture: Xbox" in textureFormat):
                # Xbox
                # Copy the files
                resources.copyToDestination(XML1Name, XMLPath, "for XML1 (Xbox)")
                resources.copyToDestination(XML2Name, XMLPath, "for XML2 (Xbox)")
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Xbox)")
            elif ("Environment Texture: Wii" in textureFormat):
                # Wii
                # Check if the MUA1 and MUA2 numbers are the same
                if settings["MUA1Num"] == settings["MUA2Num"]:
                    # MUA1 and MUA2 are the same
                    # Copy the files
                    resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii) and MUA2 (Wii)")
                else:
                    # MUA1 and MUA2 are not the same
                    # Copy the files
                    resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii)")
                    resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
            else:
                # PS2
                # Copy the files
                resources.copyToDestination(XML1Name, XMLPath, "for XML1 (PS2)")
                resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PS2)")
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2)")
    elif textureFormat == "MUA1 PC, Steam, 360, and PS3":
        # Oversized next-gen MUA1
        # Perform the first Alchemy operation
        resources.callAlchemy(MUA1Name, iniPrefix + "1-1.ini")
        # Copy the first optimized alchemy file
        resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC, Steam, PS3, and 360)")
    elif textureFormat == "Main texture: MUA1 PC, Steam, 360, and PS3 / Environment Texture: PC and MUA1 360":
        # Oversized next-gen MUA1 with environment maps
        # Perform the first Alchemy operation
        resources.callAlchemy(MUA1Name, iniPrefix + "1-1.ini")
        # Copy the first optimized alchemy file
        resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC and 360)")
        # Perform the second Alchemy operation
        resources.callAlchemy(MUA1Name, iniPrefix + "1-2.ini")
        # Copy the second optimized alchemy file
        resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Steam and PS3)")
    elif textureFormat == "XML2 PC, Xbox, and Wii":
        # Oversized XML2 PC, Xbox, and Wii
        # Copy the files
        resources.copyToDestination(XML1Name, XMLPath, "for XML1 (Xbox)")
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC and Xbox)")
        # Check if the MUA1 and MUA2 numbers are the same
        if settings["MUA1Num"] == settings["MUA2Num"]:
            # MUA1 and MUA2 are the same
            # Copy the files
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii and Xbox) and MUA2 (Wii)")
        else:
            # MUA1 and MUA2 are not the same
            # Copy the files
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii and Xbox)")
            resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
    elif "Main texture: XML2 PC, Xbox, and Wii" in textureFormat:
        # Oversized XML2 PC, Xbox, and Wii with environment maps
        # Determine which environment maps were used
        if "Environment Texture: PC and MUA1 360" in textureFormat:
            # XML2 PC
            # Copy the file
            resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC)")
        elif "Environment Texture: Wii" in textureFormat:
            # Wii
            # Check if the MUA1 and MUA2 numbers are the same
            if settings["MUA1Num"] == settings["MUA2Num"]:
                # MUA1 and MUA2 are the same
                # Copy the files
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii) and MUA2 (Wii)")
            else:
                # MUA1 and MUA2 are not the same
                # Copy the files
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii)")
                resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
        else:
            # Xbox
            # Copy the files
            resources.copyToDestination(XML1Name, XMLPath, "for XML1 (Xbox)")
            resources.copyToDestination(XML2Name, XMLPath, "for XML2 (Xbox)")
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Xbox)")
    elif ((textureFormat == "PC") or ("Environment Texture: PC" in textureFormat) or (textureFormat == "PC and MUA1 Steam")):
        # Standard sized opaque PC-only, or any size transparent PC-only
        # Copy the XML2 PC file
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC)")
        # Determine if it's transparent or not
        if not(textureFormat == "PC and MUA1 Steam"):
            # Not transparent, or has environment maps
            # Perform the first Alchemy operation
            resources.callAlchemy(MUA1Name, iniPrefix + "1-1.ini")
            # Copy the first optimized alchemy file
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC)")
            # Perform the second Alchemy operation
            resources.callAlchemy(MUA1Name, iniPrefix + "1-2.ini")
            # Copy the second optimized alchemy file
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Steam)")
        else:
            # Transparent
            # Perform the first Alchemy operation
            resources.callAlchemy(MUA1Name, iniPrefix + "1-1.ini")
            # Copy the first optimized alchemy file
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC and Steam)")
    elif textureFormat == "MUA1 PC and Steam":
        # Oversized PC-only for MUA1
        # Perform the first Alchemy operation
        resources.callAlchemy(MUA1Name, iniPrefix + "1-1.ini")
        # Copy the first optimized alchemy file
        resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC and Steam)")
    elif textureFormat == "Main texture: MUA1 PC and Steam / Environment Texture: PC and MUA1 360":
        # Oversized PC-only for MUA1 with environment maps
        # Perform the first Alchemy operation
        resources.callAlchemy(MUA1Name, iniPrefix + "1-1.ini")
        # Copy the first optimized alchemy file
        resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC)")
        # Perform the second Alchemy operation
        resources.callAlchemy(MUA1Name, iniPrefix + "1-2.ini")
        # Copy the second optimized alchemy file
        resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Steam)")
    elif ((textureFormat == "XML2 PC") or (textureFormat == "Main texture: XML2 PC / Environment Texture: PC and MUA1 360")):
        # Oversized PC-only for XML2
        # Copy the file
        resources.copyToDestination(MUA1Name, MUAPath, "for XML2 (PC)")
    else:
        # None of the above
        # Display an error message
        resources.printError("Choice of texture format did not line up with an existing operation. Please contact the program author. Selected texture format: " + textureFormat, True)
        # Set the completion status
        complete = False
        # Wait for the user to acknowledge the error
        resources.pressAnyKey(None)
    # Return the collected value
    return complete