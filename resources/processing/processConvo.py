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
# To be able to 
from os import remove
# To be able to copy files
from shutil import copy


# ######### #
# FUNCTIONS #
# ######### #
# Define the function for getting the file names
def getFileNamesAndNumbers(settings, fullFileName, suffix):
    # Initialize a list of names
    nameList = []
    # Cycle through the list of games
    for game in ["XML1", "XML2", "MUA1", "MUA2"]:
        # Determine if the game is in use
        if not(settings[game + "Num"] == None):
            # The game is in use
            # Determine if the number ends in 01
            if not(settings[game + "Num"][-2:] == "01"):
                # The number does not end in 01
                # Warn the user that this isn't recommended.
                resources.printWarning("The skin number for " + str(game) + " is set to " + settings[game + "Num"] + ". It's recommended for the last two digits of the skin number to be 01 outside of special cases.")
                # Ask the user what they want to do.
                numChoice = resources.select("What do you want to do for the " + game + "number?", ["Update the number to " + settings[game + "Num"][0:-2] + "01 (does not overwrite settings.ini).", "Leave the number as-is. I want to use a specific skin number."])
                if numChoice == "Update the number to " + settings[game + "Num"][0:-2] + "01 (does not overwrite settings.ini).":
                    # The user wants to update the number
                    # Update the number to end in 01
                    settings[game + "Num"] = settings[game + "Num"][0:-2] + "01"
            # Determine what the number is
            if settings[game + "Num"][-2:] == "01":
                # Standard numbering, can end the number in "XX"
                # Set the file name
                nameList.append(resources.setUpFileName(fullFileName, "hud_head_", settings[game + "Num"][0:-2] + "XX", suffix + ".igb"))
            else:
                # Non-standard file name
                # Set the file name
                nameList.append(resources.setUpFileName(fullFileName, "hud_head_", settings[game + "Num"], suffix + ".igb"))
        else:
            # The game is not not in use
            # Set no name
            nameList.append(None)
    # Break out the list into the specific variables
    XML1Name = nameList[0]
    XML2Name = nameList[1]
    MUA1Name = nameList[2]
    MUA2Name = nameList[3]
    # Return the collected values
    return (XML1Name, XML2Name, MUA1Name, MUA2Name)

# Define the function to export the portraits
def processConvo(settings, textureFormat, XML1Name, XML2Name, MUA1Name, MUA2Name, XMLPath, MUAPath, suffix, fullFileName):
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
        if suffix == " (Next-Gen Style)":
            # Next-gen style
            # Determine if the numbers are the same
            if settings["MUA1Num"] == settings["MUA2Num"]:
                # MUA1 and MUA2 are the same
                # Copy the files
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii) and MUA2 (Wii)")
            else:
                # MUA1 and MUA2 are not the same
                # Copy the files
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii)")
                resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
        # Perform the first Alchemy operation
        resources.callAlchemy(MUA1Name, "stat1-1.ini")
        # Copy the first optimized alchemy file
        resources.resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC and 360)")
        # Perform the second Alchemy operation
        resources.callAlchemy(MUA1Name, "stat1-2.ini")
        # Copy the second optimized alchemy file
        resources.resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Steam and PS3)")
        # Determine if PSP should be included
        if not("except PSP" in textureFormat):
            # Include PSP
            # List the files to delete and recreate
            for num, name in zip([settings["XML2Num"], settings["MUA1Num"], settings["MUA2Num"]], [XML2Name, MUA1Name, MUA2Name]):
                # Determine if the file exists
                if os.path.isfile(name):
                    # File exists
                    # Delete it
                    remove(name)
                # Determine if the number is used
                if (not(num == None) and not(name == None) and not(os.path.exists(name))):
                    # Number isn't empty, need to copy
                    # Perform the copying
                    copy(fullFileName, name)
            # Determine if the MUA1 and MUA2 numbers are the same
            if settings["MUA1Num"] == settings["MUA2Num"]:
                # MUA1 and MUA2 are the same
                # Run alchemy
                resources.callAlchemy(MUA1Name, "stat3.ini")
                # Copy the files
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP) and MUA2 (PSP)")
            else:
                # MUA1 and MUA2 are not the same
                resources.callAlchemy(MUA1Name, "stat3.ini")
                resources.callAlchemy(MUA2Name, "stat3.ini")
                # Copy the files
                resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP)")
                resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (PSP)")
            # Optimize the file for XML2 PSP
            resources.callAlchemy(XML2Name, "stat2.ini")
            # Copy the file for XML2 PSP
            resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PSP)")
    elif textureFormat == "Wii":
        # Wii only format
        # Determine if the numbers are the same
        if settings["MUA1Num"] == settings["MUA2Num"]:
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
        if settings["MUA1Num"] == settings["MUA2Num"]:
            # MUA1 and MUA2 are the same
            # Run alchemy
            resources.callAlchemy(MUA1Name, "stat3.ini")
            # Copy the files
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP) and MUA2 (PSP)")
        else:
            # MUA1 and MUA2 are not the same
            resources.callAlchemy(MUA1Name, "stat3.ini")
            resources.callAlchemy(MUA2Name, "stat3.ini")
            # Copy the files
            resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP)")
            resources.copyToDestination(MUA2Name, MUAPath, "for MUA2 (PSP)")
        # Optimize the file for XML2 PSP
        resources.callAlchemy(XML2Name, "stat2.ini")
        # Copy the file for XML2 PSP
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PSP)")
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
            if settings["MUA1Num"] == settings["MUA2Num"]:
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
        resources.callAlchemy(MUA1Name, "stat1-1.ini")
        # Copy the optimized alchemy file
        resources.resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC, Steam, PS3, and 360)")
    elif textureFormat == "PC":
        # Common PC format (128x128 or 64x64)
        # Copy the XML2 file
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC)")     
        # Perform the first Alchemy operation
        resources.callAlchemy(MUA1Name, "stat1-1.ini")
        # Copy the first optimized alchemy file
        resources.resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC)")
        # Perform the second Alchemy operation
        resources.callAlchemy(MUA1Name, "stat1-2.ini")
        # Copy the second optimized alchemy file
        resources.resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (Steam)")
    elif "PC and Steam" in textureFormat:
        # PC-only transparent HD format
        # Copy the XML2 file
        resources.copyToDestination(XML2Name, XMLPath, "for XML2 (PC)")
        # Perform the Alchemy operation
        resources.callAlchemy(MUA1Name, "stat1-1.ini")
        # Copy the optimized alchemy file
        resources.resources.copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC and Steam)")   
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
def convoProcessing(fullFileName, settings, XMLPath, MUAPath):
    # Determine the texture format
    (textureFormat, suffix) = resources.getConvoTextureFormat(settings, fullFileName)
    # Confirm that a texture format was chosen
    if not(textureFormat == None):
        # A texture format was chosen
        # Set up the file names
        (XML1Name, XML2Name, MUA1Name, MUA2Name) = getFileNamesAndNumbers(settings, fullFileName, suffix)
        # Copy the files
        for num, name in zip([settings["XML1Num"], settings["XML2Num"], settings["MUA1Num"], settings["MUA2Num"]], [XML1Name, XML2Name, MUA1Name, MUA2Name]):
            # Determine if the number is used
            if (not(num == None) and not(name == None) and not(os.path.exists(name))):
                # Number isn't empty, need to copy
                # Perform the copying
                copy(fullFileName, name)
        # Perform the hex editing
        resources.hexEdit([settings["XML1Num"], settings["XML2Num"], settings["MUA1Num"], settings["MUA2Num"]], [XML1Name, XML2Name, MUA1Name, MUA2Name], "Conversation Portrait")
        # Process the file
        complete = processConvo(settings, textureFormat, XML1Name, XML2Name, MUA1Name, MUA2Name, XMLPath, MUAPath, suffix, fullFileName)
        # Delete the lingering files
        resources.deleteLingering([XML1Name, XML2Name, MUA1Name, MUA2Name])
    else:
        # A texture format was not chosen
        complete = False
    # Return the collected value
    return complete