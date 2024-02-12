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
# Define the function to export the portraits
def processConvo(textureFormat, XML1Name, XML2Name, MUA1Name, MUA2Name, MUA1Num, MUA2Num, XMLPath, MUAPath, runAlchemyChoice, portraitType):
    # Initialize the completion variable
    complete = True
    # Filter by texture type
    if (("Main" in textureFormat) or ("All" in textureFormat)):
        # Common format
        # Copy any files that don't need optimization.
        resources.copyToDestination(XML1Name, XMLPath, "for XML1 (GC)")
        resources.copyToDestination(XML1Name, XMLPath, "for XML1 (PS2 and Xbox)")
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (GC)")
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC, PS2, and Xbox)")
        resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2 and Xbox)")
        resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (PS2)")
        # Determine if next-gen Wii portraits are needed
        if portraitType == "MUA1 Next-Gen Style":
            # Next-gen style
            # Determine if the numbers are the same
            if MUA1Num == MUA2Num:
                # MUA1 and MUA2 are the same
                # Copy the files
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii) and MUA2 (Wii)")
            else:
                # MUA1 and MUA2 are not the same
                # Copy the files
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii)")
                resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
        # Perform the first Alchemy operation
        resources.callAlchemy(MUA1Name, "stat1-1.ini", runAlchemyChoice)
        # Copy the first optimized alchemy file
        resources.resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC and 360)")
        # Perform the second Alchemy operation
        resources.callAlchemy(MUA1Name, "stat1-2.ini", runAlchemyChoice)
        # Copy the second optimized alchemy file
        resources.resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Steam and PS3)")
        # Determine if PSP should be included
        if not("except PSP" in textureFormat):
            # Include PSP
            # List the files to delete and recreate
            for num, name in zip([MUA1Num, MUA2Num], [MUA1Name, MUA2Name]):
                # Determine if the file exists
                if os.path.isfile(name):
                    # File exists
                    # Delete it
                    os.remove(name)
                # Determine if the number is used
                if (not(num == "") and not(name == None) and not(os.path.exists(name))):
                    # Number isn't empty, need to copy
                    # Perform the copying
                    shutil.copy(fullFileName, name)
            # Determine if the MUA1 and MUA2 numbers are the same
            if MUA1Num == MUA2Num:
                # MUA1 and MUA2 are the same
                # Run alchemy
                resources.callAlchemy(MUA1Name, "stat3.ini", runAlchemyChoice)
                # Copy the files
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP) and MUA2 (PSP)")
            else:
                # MUA1 and MUA2 are not the same
                resources.callAlchemy(MUA1Name, "stat3.ini", runAlchemyChoice)
                resources.callAlchemy(MUA2Name, "stat3.ini", runAlchemyChoice)
                # Copy the files
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP)")
                resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (PSP)")
    elif textureFormat == "Wii":
        # Wii only format
        # Determine if the numbers are the same
        if MUA1Num == MUA2Num:
            # MUA1 and MUA2 are the same
            # Copy the files
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii) and MUA2 (Wii)")
        else:
            # MUA1 and MUA2 are not the same
            # Copy the files
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii)")
            resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
    elif textureFormat == "PSP":
        # PSP only format
        # Determine if the MUA1 and MUA2 numbers are the same
        if MUA1Num == MUA2Num:
            # MUA1 and MUA2 are the same
            # Run alchemy
            resources.callAlchemy(MUA1Name, "stat3.ini", runAlchemyChoice)
            # Copy the files
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP) and MUA2 (PSP)")
        else:
            # MUA1 and MUA2 are not the same
            resources.callAlchemy(MUA1Name, "stat3.ini", runAlchemyChoice)
            resources.callAlchemy(MUA2Name, "stat3.ini", runAlchemyChoice)
            # Copy the files
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP)")
            resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (PSP)")
    elif ((textureFormat == "GC, PS2, and Xbox") or (textureFormat == "Last-Gen")):
        # Common last-gen format for HD
        # Copy any files that don't need optimization.
        resources.copyToDestination(XML1Name, XMLPath, "for XML1 (GC)")
        resources.copyToDestination(XML1Name, XMLPath, "for XML1 (PS2 and Xbox)")
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (GC)")
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PS2 and Xbox)")
        resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2 and Xbox)")
        resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (PS2)")
        # Determine if Wii is needed
        if textureFormat == "Last Gen":
            # Wii is needed
            # Determine if the numbers are the same
            if MUA1Num == MUA2Num:
                # MUA1 and MUA2 are the same
                # Copy the files
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii) and MUA2 (Wii)")
            else:
                # MUA1 and MUA2 are not the same
                # Copy the files
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii)")
                resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
    elif textureFormat == "XML2 PC":
        # XML2-specific HD format
        # Copy the file
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC)")
    elif "PC and Next-Gen" in textureFormat:
        # Common HD format
        # Determine if this is MUA1 only
        if not("MUA1" in textureFormat):
            # Not MUA1 only
            # Copy the XML2 file
            resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC)")
        # Perform the Alchemy operation
        resources.callAlchemy(MUA1Name, "stat1-1.ini", runAlchemyChoice)
        # Copy the optimized alchemy file
        resources.resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC, Steam, PS3, and 360)")
    elif textureFormat == "PC":
        # Common PC format (128x128 or 64x64)
        # Copy the XML2 file
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC)")     
        # Perform the first Alchemy operation
        resources.callAlchemy(MUA1Name, "stat1-1.ini", runAlchemyChoice)
        # Copy the first optimized alchemy file
        resources.resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC)")
        # Perform the second Alchemy operation
        resources.callAlchemy(MUA1Name, "stat1-2.ini", runAlchemyChoice)
        # Copy the second optimized alchemy file
        resources.resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Steam)")
    elif "PC and Steam" in textureFormat:
        # PC-only transparent HD format
        # Copy the XML2 file
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC)")
        # Perform the Alchemy operation
        resources.callAlchemy(MUA1Name, "stat1-1.ini", runAlchemyChoice)
        # Copy the optimized alchemy file
        resources.resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC and Steam)")   
    else:
        # None of the above
        # Display an error message
        resources.printError("ERROR: Choice of texture format did not line up with an existing operation. Please contact the program author. Selected texture format: " + textureFormat)
        # Set the completion status
        complete = False
        # Wait for the user to acknowledge the error
        resources.pressAnyKey(None)
    # Return the completion variable
    return complete

# Define the function to process conversation portraits
def convoProcessing(assetType, fullFileName, XML1Num, XML2Num, MUA1Num, MUA2Num, XMLPath, MUAPath, pcOnly, hexEditChoice, runAlchemyChoice):
    # Determine the texture format
    (textureFormat, portraitType) = resources.getConvoTextureFormat(assetType, XML2Num, MUA1Num, MUA2Num, pcOnly)
    # Confirm that a texture format was chosen
    if not(textureFormat == None):
        # A texture format was chosen
        # Determine the portrait type
        if portraitType == "Standard Style":
            # Standard portrait
            # Set up the list of outline types
            outlineTypeList = ["No Outline", "Blue Hero Outline", "Red Villain Outline", "Green Villain Outline"]
            # Set up the list of file name suffixes
            nameSuffixList = ["", " (Hero)", " (Villain)", " (Villain/Possessed)"]
            # Ask about the outline type
            outlineType = resources.selectDefault("What type of outline does the portrait have?", outlineTypeList, "Blue Hero Outline")
            # Go through the outline types and name suffixes
            for outline, name in zip(outlineTypeList, nameSuffixList):
                # Determine if the outline matches with the selection
                if outlineType == outline:
                    # The selections match
                    # Set up the suffix
                    suffix = name
        else:
            # Next-Gen portrait
            # Set up the suffix
            suffix = " (Next-Gen Style)"
        # Set up the file names
        XML1Name = os.path.join(os.path.dirname(fullFileName), "hud_head_" + XML1Num + "XX" + suffix + ".igb")
        XML2Name = os.path.join(os.path.dirname(fullFileName), "hud_head_" + XML2Num + "XX" + suffix + ".igb")
        MUA1Name = os.path.join(os.path.dirname(fullFileName), "hud_head_" + MUA1Num + "XX" + suffix + ".igb")
        MUA2Name = os.path.join(os.path.dirname(fullFileName), "hud_head_" + MUA2Num + "XX" + suffix + ".igb")
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
        complete = processConvo(textureFormat, XML1Name, XML2Name, MUA1Name, MUA2Name, MUA1Num, MUA2Num, XMLPath, MUAPath, runAlchemyChoice, portraitType)
    else:
        # A texture format was not chosen
        complete = false
    # Delete the lingering files
    resources.deleteLingering([XML1Name, XML2Name, MUA1Name, MUA2Name])
    # Return the collected value
    return complete