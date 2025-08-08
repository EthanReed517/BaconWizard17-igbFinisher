# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import common
import processing
import questions
import textures


# ######### #
# FUNCTIONS #
# ######### #
# Define the function for getting the file names
def getCSPFileNamesAndNumbers(settings, fullFileName, portraitType):
    # Initialize a list of names
    nameList = []
    # Cycle through the list of games
    for game in ["XML1", "XML2"]:
        # Set the default description for the file
        description = "Character Select Portrait"
        # Determine if the portrait type matches the current game
        if portraitType == game:
            # The portrait is used with this game
            # Determine if the game is used
            if settings[f"{game}Num"] is not None:
                # This game is used
                # Determine if the number ends in 01
                if settings[f"{game}Num"][-2:] == "01":
                    # The number ends in 01, which is okay
                    # Just pass to move on
                    pass
                elif settings[f"{game}Num"][-2:] == "XX":
                    # The number ends in XX, which is also okay
                    # Update the number to end in 01 for proper processing
                    settings[f"{game}Num"] = settings[f'{game}Num'][0:-2] + "01"
                else:
                    # The number does not end in 01 or XX
                    # Warn the user that the number should end in 01 or XX
                    questions.PrintWarning(f"The skin number for {game} is set to {settings[f'{game}Num']}. Unless this is a special case, it's recommended that the skin number in the settings ends with \"XX\" or 01, which will process the CSP with the number ending in 01 and the standard descriptor.")
                    # Ask the user what they want to do.
                    numChoice = questions.Select(f"What do you want to do for the {game} number?", [f"Update the number to {settings[f'{game}Num'][0:-2]}XX (does not overwrite settings.ini).", "Leave the number as-is. I want to use a specific skin number and not have any descriptor."])
                    # Determine what the user picked.
                    if numChoice == f"Update the number to {settings[f'{game}Num'][0:-2]}XX (does not overwrite settings.ini).":
                        # The user wanted to update the skin number to end in 01.
                        # Update the settings for this game.
                        settings[f"{game}Num"] = f"{settings[f'{game}Num'][0:-2]}01"
                    else:
                        # The user wants to leave the number as-is
                        # Set an empty descriptor
                        description = None
                # Determine if there is any description
                if description is None:
                    # There is no description
                    # Set the file name
                    nameList.append(common.setUpFileName2("", settings[f'{game}Num'], ".igb"))
                else:
                    # There is a description
                    # Add the new name to the list
                    nameList.append(common.setUpFileName2("", f"{settings[f'{game}Num'][0:-2]}XX", f" ({description}).igb"))
        else:
            # The portrait is not used with this game
            # Set the name to None
            nameList.append(None)
    # Add two None entries for MUA1 and MUA2.
    nameList.extend([None, None])
    # Break out the list into the specific variables
    XML1Name = nameList[0]
    XML2Name = nameList[1]
    MUA1Name = nameList[2]
    MUA2Name = nameList[3]
    # Return the collected values
    return (settings, XML1Name, XML2Name, MUA1Name, MUA2Name)

# Define the function to export the portraits
def processCSP(assetType, sourceFileName, textureFormat, numsDict, nameDict, pathDict):
    # Set up the dictionary of necessary operations for each texture type
    processDict = {
        # Common format for 64x64 starting size
        "All": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PSP)", "optList": ["stat2.ini"]}}
        ],
        # Common format for 128x128 starting size
        "All except PSP": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC and Xbox)", "optList": None}}
        ],
        # Console format for XML2 256x256 size
        "GC, PS2, and Xbox": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}}
        ],
        # PSP-specific format, only used with XML2 and when the starting size is over 64x64
        "PSP": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PSP)", "optList": ["stat2.ini"]}}
        ],
        # PC-only format, which can be DXT1 or PNG8 depending on texture size
        "PC": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ]
    }
    # Initialize the completion variable
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
        questions.PrintError(f"Choice of texture format did not line up with an existing operation. Selected texture format: {textureFormat}")
        # Update the completion variable to indicate that nothing was processed
        complete = False
    # Return the completion variable
    return complete

# Define the function to process conversation portraits
def CSPProcessing(fullFileName, settings, XMLPath, MUAPath):
    # Determine the texture format
    (textureFormat, portraitType) = textures.getCSPTextureFormat(settings, fullFileName)
    # Confirm that a texture format was chosen
    if textureFormat is not None:
        # A texture format was chosen
        # Set up the file names
        (settings, XML1Name, XML2Name, MUA1Name, MUA2Name) = getCSPFileNamesAndNumbers(settings, fullFileName, portraitType)
        # Set up the dictionaries for processing
        numsDict = {"XML1": settings["XML1Num"], "XML2": settings["XML2Num"], "MUA1": settings["MUA1Num"], "MUA2": settings["MUA2Num"]}
        nameDict = {"XML1": XML1Name, "XML2": XML2Name, "MUA1": None, "MUA2": None}
        pathDict = {"XML": XMLPath, "MUA": MUAPath}
        # Process the file
        complete = processCSP("Character Select Portrait", fullFileName, textureFormat, numsDict, nameDict, pathDict)
    else:
        # A texture format was not chosen
        complete = False
    # Return the collected value
    return complete