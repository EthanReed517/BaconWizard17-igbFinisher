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
        questions.printError(f"Choice of texture format did not line up with an existing operation. Selected texture format: {textureFormat}", True)
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
        # Determine the portrait type
        if portraitType == "XML1":
            # XML1 portrait
            # Set up file names
            XML1Name = common.setUpFileName2("", settings["XML1Num"][0:-2], "XX (Character Select Portrait).igb")
            XML2Name = None
        else:
            # XML2 portrait
            # Set up file names
            XML1Name = None
            XML2Name = common.setUpFileName2("", settings["XML2Num"][0:-2], "XX (Character Select Portrait).igb")
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