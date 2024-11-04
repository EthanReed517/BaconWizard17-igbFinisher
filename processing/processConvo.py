# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import common
import hex
import processing
import questions
import textures
# External modules
import os.path
from os import remove
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
        if settings[f"{game}Num"] is not None:
            # The game is in use
            # Determine if the number ends in 01
            if not(settings[f"{game}Num"][-2:] == "01"):
                # The number does not end in 01
                # Warn the user that this isn't recommended.
                questions.printWarning(f"The skin number for {game} is set to {settings[f'{game}Num']}. It's recommended for the last two digits of the skin number to be 01 outside of special cases.")
                # Ask the user what they want to do.
                numChoice = questions.select(f"What do you want to do for the {game} number?", [f"Update the number to {settings[f'{game}Num'][0:-2]}01 (does not overwrite settings.ini).", "Leave the number as-is. I want to use a specific skin number."])
                if numChoice == f"Update the number to {settings[f'{game}Num'][0:-2]}01 (does not overwrite settings.ini).":
                    # The user wants to update the number
                    # Update the number to end in 01
                    settings[f"{game}Num"] = f"{settings[f'{game}Num'][0:-2]}01"
            # Determine what the number is
            if settings[f"{game}Num"][-2:] == "01":
                # Standard numbering, can end the number in "XX"
                # Set the file name
                nameList.append(common.setUpFileName2("hud_head_", f"{settings[f'{game}Num'][0:-2]}XX", f"{suffix}.igb"))
            else:
                # Non-standard file name
                # Set the file name
                nameList.append(common.setUpFileName2("hud_head_", settings[f"{game}Num"], f"{suffix}.igb"))
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
def processConvo(assetType, sourceFileName, textureFormat, numsDict, nameDict, pathDict):
    # Set up the dictionary of necessary operations for each texture type
    processDict = {
        # PSP-only, which could be next-gen style (plain PNG) or PNG8
        "PSP": [
            {"function": processing.processPSPFiles, "kwargs": {"nums": numsDict, "files": nameDict, "paths": pathDict, "prefix": "stat"}}
        ],
        # Next-Gen Style (plain PNG), all consoles
        "All": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC, PS2, and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and 360)", "optList": ["stat1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam and PS3)", "optList": ["stat1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA2"], "file": nameDict["MUA2"], "path": pathDict["MUA"], "folder": "for MUA2 (PS2)", "optList": ["stat3.ini"]}},
            {"function": processing.processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}},
            {"function": processing.processPSPFiles, "kwargs": {"nums": numsDict, "files": nameDict, "paths": pathDict, "prefix": "stat"}}
        ],
        "All except PSP": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC, PS2, and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and 360)", "optList": ["stat1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam and PS3)", "optList": ["stat1-1.ini", "stat1-2.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA2"], "file": nameDict["MUA2"], "path": pathDict["MUA"], "folder": "for MUA2 (PS2)", "optList": ["stat3.ini"]}},
            {"function": processing.processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        "PC and Next-Gen": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC, Steam, PS3, and 360)", "optList": ["stat1-1.ini"]}}
        ],
        "Last-Gen": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA2"], "file": nameDict["MUA2"], "path": pathDict["MUA"], "folder": "for MUA2 (PS2)", "optList": ["stat3.ini"]}},
            {"function": processing.processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        # Next-Gen Style (plain PNG), PC only
        "PC and Steam": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and Steam)", "optList": ["stat1-1.ini"]}}
        ],
        # PNG8 format, all consoles
        "Main": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC, PS2, and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and 360)", "optList": ["stat1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam and PS3)", "optList": ["stat1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA2"], "file": nameDict["MUA2"], "path": pathDict["MUA"], "folder": "for MUA2 (PS2)", "optList": ["stat3.ini"]}},
            {"function": processing.processPSPFiles, "kwargs": {"nums": numsDict, "files": nameDict, "paths": pathDict, "prefix": "stat"}}
        ],
        "Main except PSP": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC, PS2, and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and 360)", "optList": ["stat1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam and PS3)", "optList": ["stat1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA2"], "file": nameDict["MUA2"], "path": pathDict["MUA"], "folder": "for MUA2 (PS2)", "optList": ["stat3.ini"]}}
        ],
        "GC, PS2, and Xbox": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2 and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA2"], "file": nameDict["MUA2"], "path": pathDict["MUA"], "folder": "for MUA2 (PS2)", "optList": ["stat3.ini"]}}
        ],
        # PNG8 format, PC only
        "PC": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC)", "optList": ["stat1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam)", "optList": ["stat1-1.ini", "stat1-2.ini"]}}
        ],
        # DXT1 format, all consoles
        "Wii": [
            {"function": processing.processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        "XML2 PC": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        "MUA1 PC and Next-Gen": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and 360)", "optList": ["stat1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam and PS3)", "optList": ["stat1-1.ini"]}}
        ],
        # DXT1 format, PC only
        "MUA1 PC and Steam": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and Steam)", "optList": ["stat1-1.ini"]}}
        ]
    }
    # Start a variable that assumes completion
    complete = True
    # Attempt to process
    try:
        # Loop through the possible files for the selected texture format
        for file in processDict[textureFormat]:
            # Process the file using its necessary function and arguments
            file["function"](sourceFileName, assetType, **file["kwargs"])
    except KeyError:
        # The selected texture format doesn't have an entry in the dictionary
        # Print an error
        questions.printError(f"Choice of texture format did not line up with an existing operation. Selected texture format: {textureFormat}", True)
        # Update the completion variable to indicate that nothing was processed
        complete = False
    # Return the completion variable
    return complete

# Define the function to process conversation portraits
def convoProcessing(fullFileName, settings, XMLPath, MUAPath):
    # Determine the texture format
    (textureFormat, suffix) = textures.getConvoTextureFormat(settings, fullFileName)
    # Confirm that a texture format was chosen
    if textureFormat is not None:
        # A texture format was chosen
        # Set up the file names
        (XML1Name, XML2Name, MUA1Name, MUA2Name) = getFileNamesAndNumbers(settings, fullFileName, suffix)
        # Set up the dictionaries for processing
        numsDict = {"XML1": settings["XML1Num"], "XML2": settings["XML2Num"], "MUA1": settings["MUA1Num"], "MUA2": settings["MUA2Num"]}
        nameDict = {"XML1": XML1Name, "XML2": XML2Name, "MUA1": MUA1Name, "MUA2": MUA2Name}
        pathDict = {"XML": XMLPath, "MUA": MUAPath}
        # Process the file
        complete = processConvo("Conversation Portrait", fullFileName, textureFormat, numsDict, nameDict, pathDict)
    else:
        # A texture format was not chosen
        complete = False
    # Return the collected value
    return complete