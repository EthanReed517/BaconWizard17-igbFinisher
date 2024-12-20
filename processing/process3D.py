# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import processing
import questions


# ######### #
# FUNCTIONS #
# ######### #
# Define the function for processing files with no textures
def processNoTexFile(sourceFileName, assetType, nums, files, paths, prefix):
    # Set up the list of folder options
    folderOptions = ["Like a model with a 256x256 or less texture", "Like a model with a larger than 256x256 texture", "Using as few folders as possible"]
    # Determine how the user wants to process the file
    folderOption = questions.select("What folder structure should be used?", folderOptions)
    # Determine what the user picked
    if folderOption == folderOptions[0]:
        # Send out like a model with a 256x256 or less texture
        processing.processFile(sourceFileName, assetType, nums["XML1"], files["XML1"], paths["XML"], "for XML1 (GC)", None)
        processing.processFile(sourceFileName, assetType, nums["XML1"], files["XML1"], paths["XML"], "for XML1 (PS2)", None)
        processing.processFile(sourceFileName, assetType, nums["XML1"], files["XML1"], paths["XML"], "for XML1 (Xbox)", None)
        processing.processFile(sourceFileName, assetType, nums["XML2"], files["XML2"], paths["XML"], "for XML2 (GC)", None)
        processing.processFile(sourceFileName, assetType, nums["XML2"], files["XML2"], paths["XML"], "for XML2 (PS2)", None)
        processing.processFile(sourceFileName, assetType, nums["XML2"], files["XML2"], paths["XML"], "for XML2 (PC and Xbox)", None)
        processing.processPSPFiles(sourceFileName, assetType, nums, files, paths, prefix)
        processing.processFile(sourceFileName, assetType, nums["MUA1"], files["MUA1"], paths["MUA"], "for MUA1 (PS2)", None)
        processing.processFile(sourceFileName, assetType, nums["MUA1"], files["MUA1"], paths["MUA"], "for MUA1 (Xbox)", None)
        processing.processWiiFiles(sourceFileName, assetType, nums, files, paths["MUA"])
        processing.processFile(sourceFileName, assetType, nums["MUA1"], files["MUA1"], paths["MUA"], "for MUA1 (PC and 360)", [f"{prefix}1-1.ini"])
        processing.processFile(sourceFileName, assetType, nums["MUA1"], files["MUA1"], paths["MUA"], "for MUA1 (Steam and PS3)", [f"{prefix}1-1.ini"])
        processing.processFile(sourceFileName, assetType, nums["MUA2"], files["MUA2"], paths["MUA"], "for MUA2 (PS2)", [f"{prefix}3.ini"])
    elif folderOption == folderOptions[1]:
        # Send out like a model with a larger than 256x256 texture
        processing.processFile(sourceFileName, assetType, nums["XML1"], files["XML1"], paths["XML"], "for XML1 (GC)", None)
        processing.processFile(sourceFileName, assetType, nums["XML1"], files["XML1"], paths["XML"], "for XML1 (PS2)", None)
        processing.processFile(sourceFileName, assetType, nums["XML1"], files["XML1"], paths["XML"], "for XML1 (Xbox)", None)
        processing.processFile(sourceFileName, assetType, nums["XML2"], files["XML2"], paths["XML"], "for XML2 (GC)", None)
        processing.processFile(sourceFileName, assetType, nums["XML2"], files["XML2"], paths["XML"], "for XML2 (PS2)", None)
        processing.processFile(sourceFileName, assetType, nums["XML2"], files["XML2"], paths["XML"], "for XML2 (PC and Xbox)", None)
        processing.processPSPFiles(sourceFileName, assetType, nums, files, paths, prefix)
        processing.processFile(sourceFileName, assetType, nums["MUA1"], files["MUA1"], paths["MUA"], "for MUA1 (PS2)", None)
        processing.processFile(sourceFileName, assetType, nums["MUA1"], files["MUA1"], paths["MUA"], "for MUA1 (Xbox)", None)
        processing.processWiiFiles(sourceFileName, assetType, nums, files, paths["MUA"])
        processing.processFile(sourceFileName, assetType, nums["MUA1"], files["MUA1"], paths["MUA"], "for MUA1 (PC, Steam, PS3, and 360)", [f"{prefix}1-1.ini"])
        processing.processFile(sourceFileName, assetType, nums["MUA2"], files["MUA2"], paths["MUA"], "for MUA2 (PS2)", [f"{prefix}3.ini"])
    else:
        # Send to as few folders as possible
        processing.processFile(sourceFileName, assetType, nums["XML1"], files["XML1"], paths["XML"], "for XML1 (GC, PS2, and Xbox)", None)
        processing.processFile(sourceFileName, assetType, nums["XML2"], files["XML2"], paths["XML"], "for XML2 (PC, GC, PS2, and Xbox)", None)
        processing.processPSPFiles(sourceFileName, assetType, nums, files, paths, prefix)
        processing.processFile(sourceFileName, assetType, nums["MUA1"], files["MUA1"], paths["MUA"], "for MUA1 (PS2 and Xbox)", None)
        processing.processWiiFiles(sourceFileName, assetType, nums, files, paths["MUA"])
        processing.processFile(sourceFileName, assetType, nums["MUA1"], files["MUA1"], paths["MUA"], "for MUA1 (PC, Steam, PS3, and 360)", [f"{prefix}1-1.ini"])
        processing.processFile(sourceFileName, assetType, nums["MUA2"], files["MUA2"], paths["MUA"], "for MUA2 (PS2)", [f"{prefix}3.ini"])

# Define the function for processing assets
def process3D(assetType, sourceFileName, textureFormat, numsDict, nameDict, pathDict):
    # Determine the asset type
    if assetType == "Skin":
        # This is a skin
        # Set the ini prefix
        iniPrefix = "skin"
    else:
        # Not a skin
        # Set the ini prefix
        iniPrefix = "stat"
    # Set up the dictionary of necessary operations for each texture type
    processDict = {
        # No texture type
        "No Texture": [
            {"function": processNoTexFile, "kwargs": {"nums": numsDict, "files": nameDict, "paths": pathDict, "prefix": iniPrefix}}
        ],
        # Single texture type, PNG8 format, all consoles
        "PC, PS2, Xbox, and MUA1 360": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and 360)", "optList": [f"{iniPrefix}1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam and PS3)", "optList": [f"{iniPrefix}1-1.ini", f"{iniPrefix}1-2.ini"]}}
        ],
        "PC, Xbox, and MUA1 360": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and 360)", "optList": [f"{iniPrefix}1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam and PS3)", "optList": [f"{iniPrefix}1-1.ini", f"{iniPrefix}1-2.ini"]}}
        ],
        "PS2": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2)", "optList": None}}
        ],
        "GameCube, PSP, and MUA2 PS2": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}},
            {"function": processing.processPSPFiles, "kwargs": {"nums": numsDict, "files": nameDict, "paths": pathDict, "prefix": iniPrefix}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA2"], "file": nameDict["MUA2"], "path": pathDict["MUA"], "folder": "for MUA2 (PS2)", "optList": [f"{iniPrefix}3.ini"]}}
        ],
        # Single texture type, PNG8 format, PC only
        "PC": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC)", "optList": [f"{iniPrefix}1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam)", "optList": [f"{iniPrefix}1-1.ini", f"{iniPrefix}1-2.ini"]}}
        ],
        # Single texture type, DXT1 format, all consoles
        "MUA1 PC, Steam, 360, and PS3": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC, Steam, PS3 and 360)", "optList": [f"{iniPrefix}1-1.ini"]}}
        ],
        "XML2 PC, Xbox, and Wii": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox and Wii)", "optList": None}}
        ],
        "Wii": [
            {"function": processing.processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        # Single texture type, DXT1 format, PC only
        "MUA1 PC and Steam": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and Steam)", "optList": [f"{iniPrefix}1-1.ini"]}}
        ],
        "XML2 PC": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        # Single texture type, plain PNG format, all consoles ("PS2" and "GameCube, PSP, and MUA2 PSP" already covered earlier)
        "PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}},
            {"function": processing.processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and 360)", "optList": [f"{iniPrefix}1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam and PS3)", "optList": [f"{iniPrefix}1-1.ini"]}}
        ],
        "PC, Xbox, Wii, MUA1 Steam, PS3, and 360": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC and Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}},
            {"function": processing.processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and 360)", "optList": [f"{iniPrefix}1-1.ini"]}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Steam and PS3)", "optList": [f"{iniPrefix}1-1.ini"]}}
        ],
        # Single texture type, plain PNG format, PC only
        "PC and MUA1 Steam": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PC and Steam)", "optList": [f"{iniPrefix}1-1.ini"]}}
        ],
        # PNG8 format environment maps, all consoles
        "Environment texture: PC and MUA1 360": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        "Environment texture: Xbox": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}}
        ],
        "Environment texture: PS2": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PS2)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (PS2)", "optList": None}}
        ],
        "Environment texture: GameCube, PSP, and MUA2 PS2": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (GC)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (GC)", "optList": None}},
            {"function": processing.processPSPFiles, "kwargs": {"nums": numsDict, "files": nameDict, "paths": pathDict, "prefix": iniPrefix}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA2"], "file": nameDict["MUA2"], "path": pathDict["MUA"], "folder": "for MUA2 (PS2)", "optList": [f"{iniPrefix}3.ini"]}}
        ],
        # PNG8 format environment maps, PC only
        "Environment texture: PC": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        # DXT1 Format environment maps, all consoles
        "Environment texture: XML2 PC": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (PC)", "optList": None}}
        ],
        "Environment texture: Xbox and Wii": [
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML1"], "file": nameDict["XML1"], "path": pathDict["XML"], "folder": "for XML1 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["XML2"], "file": nameDict["XML2"], "path": pathDict["XML"], "folder": "for XML2 (Xbox)", "optList": None}},
            {"function": processing.processFile, "kwargs": {"num": numsDict["MUA1"], "file": nameDict["MUA1"], "path": pathDict["MUA"], "folder": "for MUA1 (Xbox)", "optList": None}},
            {"function": processing.processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        "Environment texture: Wii": [
            {"function": processing.processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
        ],
        "Environment texture: Xbox and Wii": [
            {"function": processing.processWiiFiles, "kwargs": {"nums": numsDict, "files": nameDict, "path": pathDict["MUA"]}}
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
    # Return whether or not the processing was successfully completed
    return complete