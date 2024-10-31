# ########### #
# INFORMATION #
# ########### #
# This module is used to determine the texture formats for 3D assets: skins, 3D heads, mannequins, and other models.


# ####### #
# IMPORTS #
# ####### #
# Modules from this program
import alchemy
import questions


# ######### #
# FUNCTIONS #
# ######### #
# Define the function to recognize the texture format.
def recognize3DTextureFormat(texPathList, texFormatList):
    # Initialize the counters for the acceptable texture formats. These will keep track of how many textures of each format are found.
    png8Counter = 0
    dxt1Counter = 0
    plainPngCounter = 0
    # Initialize a list to keep track of the folders. The folders will be picked out in the following loop and appended to this list.
    texFolderList = []
    # Loop through the lists of texture paths and texture formats.
    for path, format in zip(texPathList, texFormatList):
        # Determine if this is an environment map, which will show as a texture path that just says "sphereImage."
        if "sphereImage" in path:
            # This is a path for an environment map.
            # Since "sphereImage" paths don't have folders, there's nothing to split, so the folder can just be set to "sphereImage."
            texFolder = "sphereImage"
        else:
            # This is not a path for an environment map.
            # Get the name of the folder that the texture is stored in. This is the second to last element in the path.
            texFolder = path.split("\\")[-2]
        # When there are multiple formats of different lengths, there will be spaces added after them to keep them the same length for Alchemy's list. This removes the spaces to make sure that the same information is always presented.
        texFormat = format.rstrip()
        # Begin checking if the current format matches with any of the allowed format.
        if texFormat == "IG_GFX_TEXTURE_FORMAT_X_8 (65536)":
            # This format is a png file with PNG8 compression.
            # Increment the counter for PNG8 formats.
            png8Counter += 1
        elif texFormat == "IG_GFX_TEXTURE_FORMAT_RGBA_DXT1 (14)":
            # This format is a dds file with DXT1 compression.
            # Increment the counter for DXT1 formats.
            dxt1Counter += 1
        elif texFormat == "IG_GFX_TEXTURE_FORMAT_RGBA_8888_32 (7)":
            # This format is a png file with no compression.
            # Display a warning. igbFinisher doesn't perform operations for transparency because there's no way to know if it's necessary or not (only certain types of transparency need it). This warning lets the user know that.
            questions.printWarning("This model uses a plain png texture with transparency. If the texture has full transparency, you will need to convert igBlend to igAlpha prior to running the model through igbFinisher.")
            # Increment the counter for plain png textures.
            plainPngCounter += 1
        elif texFormat == "IG_GFX_TEXTURE_FORMAT_X_4 (65537)":
            # This format is a png file with PNG4 compression, which is not supported. 
            # Give an error to let the user know that this format isn't allowed. It's not supported because PNG4 is only used on the PSP and only for some assets; taking out PNG4 compatibility reduces the number of texture options and makes processing easier.
            questions.printError("This model uses a png texture that's in PNG4 format. This texture format is not supported by igbFinisher. Please choose a different texture.", False)
        elif texFormat == "IG_GFX_TEXTURE_FORMAT_RGB_888_24 (5)":
            # This format is a png file with no compression but no alpha channel, which is not supported.
            # Give an error to let the user know that this format isn't allowed. It's not supported because uncompressed png files bring up file sizes significantly with no benefits to the texture (since there's no alpha channel, they can't even have transparency).
            questions.printError("This model uses a png texture that's uncompressed without an alpha channel (no transparency). This texture format is not supported by igbFinisher. Please choose a different texture.", False)
        elif texFormat == "IG_GFX_TEXTURE_FORMAT_RGBA_DXT3 (15)":
            # This format is a dds file with DXT3 compression, which is not supported.
            # Give an error to let the user know that this format isn't allowed. It's not supported because DXT3 is compatible with fewer consoles; the Marvel Mods GIMP scripts don't even export with it for that reason, so there's no reason that it would show up here.
            questions.printError("This model uses a dds texture that's in DXT3 format. This texture format is not supported by igbFinisher. Please choose a different texture.", False)
        elif texFormat == "IG_GFX_TEXTURE_FORMAT_RGBA_DXT5 (16)":
            # This format is a dds file with DXT5 compression, which is not supported.
            # Give an error to let the user know that this format isn't allowed. It's not supported because DXT5 is compatible with fewer consoles; the Marvel Mods GIMP scripts don't even export with it for that reason, so there's no reason that it would show up here.
            questions.printError("This model uses a dds texture that's in DXT5 format. This texture format is not supported by igbFinisher. Please choose a different texture.", False)
        else:
            # The format was not recognized at all.
            # Give an error to let the user know. This technically shouldn't happen because the previous options cover all the common formats, but there are some fringe formats that can be exported if you know how to do it.
            questions.printError(f"A texture format used by this model is not recognized. Please choose a different texture.\nTexture format \"{texFormat}\".", False)
        # Add the texture folder to the list of texture formats.
        texFolderList.append(texFolder)
    # Return the collected variables: the number of PNG8 textures found in the model, the number of DXT1 textures found in the model, the number of plain png textures found in the model, and the list of texture formats.
    return png8Counter, dxt1Counter, plainPngCounter, texFolderList

# Define the function for identifying the number of unique texture folders in the model's list of texture folders
def getUniqueFolders(texFolderList):
    # Start a list of unique folders to ensure that each folder is only listed once.
    uniqueFolders = []
    # Loop through all the folders in list of the model's texture folders.
    for folder in texFolderList:
        # Determine if the folder has not yet been added to the list of unique folders, meaning that it is truly unique.
        if folder not in uniqueFolders:
            # Determine if the current folder is not the "sphereImage" folder, since that folder isn't a real folder and doesn't need to be counted as a unique folder.
            if not(folder == "sphereImage"):
                # This is not a "sphereImage" folder, so it can be added to the list if it's unique.
                # The folder has not been added yet, so it is unique.
                # Add the folder to the list of unique folders.
                uniqueFolders.append(folder)
    # Return the list of of unique folders
    return uniqueFolders

# Define the function for getting the texture folder in the case where there's only one texture format and the same folder is used for all textures.
def oneFormatOneFolder(png8Counter, dxt1Counter, plainPngCounter, texFolderList, settings):
    # Compare the counters of different folders to determine which folder is being used.
    if png8Counter == len(texFolderList):
        # This is PNG8 format.
        # Determine if this is for PC or consoles, which will determine which texture list to use.
        if settings["pcOnly"] == False:
            # The model is being processed for all consoles.
            # Set up the texture folder list with PNG8 texture options that are compatible with all consoles.
            textureFolderList = ["PC, PS2, Xbox, and MUA1 360", "PC, Xbox, and MUA1 360", "PS2", "GameCube, PSP, and MUA2 PS2"]
        else:
            # The model is being process for PC only.
            # Set up the texture folder list with PNG8 texture options that are compatible with PC only.
            textureFolderList = ["PC"]
    elif dxt1Counter == len(texFolderList):
        # This is DXT1 format.
        # Determine if this is for PC or consoles, which will determine which texture list to use.
        if settings["pcOnly"] == False:
            # The model is being processed for all consoles.
            # Set up the texture folder list with DXT1 texture options that are compatible with all consoles.
            textureFolderList = ["MUA1 PC, Steam, 360, and PS3", "XML2 PC, Xbox, and Wii", "Wii"]
        else:
            # The model is being process for PC only.
            # Set up the texture folder list with DXT1 texture options that are compatible with PC only.
            textureFolderList = ["MUA1 PC and Steam", "XML2 PC"]
    elif plainPngCounter == len(texFolderList):
        # This is plain png format.
        # Determine if this is for PC or consoles, which will determine which texture list to use.
        if settings["pcOnly"] == False:
            # The model is being processed for all consoles.
            # Set up the texture folder list with plain png texture options that are compatible with all consoles.
            textureFolderList = ["PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360", "PC, Wii, Xbox, MUA1 Steam, PS3, and 360", "PS2", "GameCube, PSP, and MUA2 PS2"]
        else:
            # The model is being process for PC only.
            # Set up the texture folder list with plain png texture options that are compatible with PC only.
            textureFolderList = ["PC and MUA1 Steam"]
    else:
        # No format counter is the same as the length of the texture format list.
        # Notify the user of the error. There's really no way this should happen unless there's something super weird going on, but I'm adding it for extra error security.
        questions.printError("igbFinisher determined that the model only uses one texture format and one texture folder, but no texture format counter is the same as the length of the texture format list.", True)
    # Determine if the texture folder can be found in the list of texture folders that was created earlier. Since all folders are the same, the first item from the list is taken.
    if texFolderList[0] in textureFolderList:
        # The texture folder used by the model can be found in the list of texture folders that was created earlier.
        # Set the format to be this folder.
        textureFormat = texFolderList[0]
        # Print a success message to inform the user that there is a match.
        questions.printSuccess(f"The texture folder was automatically identified as {textureFormat}.")
    else:
        # The texture folder used by the model can't be found in the list of texture folders that was created earlier.
        # Print the error to inform the user that the texture folder couldn't be matched to an acceptable format. This can happen if they exported without using the Marvel Mods GIMP Scripts or if they dropped the textures from outside of the VM.
        questions.printError(f"The texture folder, {texFolderList[0]}, could not be recognized. Make sure that you're exporting your textures with the Marvel Mods GIMP Scripts and adding the textures from within the VM. Please try again.", False)
        # In order to have a return variable for this case, set the texture format to "None" again.
        textureFormat = None
    # Return the collected texture format for further processing.
    return textureFormat

# Define the function for getting the texture folder in the case where there's only one texture format and environment maps were used.
def oneFormatEnvironmentMaps(png8Counter, dxt1Counter, plainPngCounter, texFolderList, settings):
    # Compare the counters of different folders to determine which folder is being used.
    if png8Counter == len(texFolderList):
        # This is PNG8 format.
        # Determine if this is for PC or consoles, which will determine which texture list to use.
        if settings["pcOnly"] == False:
            # The model is being processed for all consoles.
            # Set up the texture folder list with PNG8 texture options that are compatible with all consoles.
            textureFolderList = [("PC, PS2, Xbox, and MUA1 360", "PC and MUA1 360"), ("PC, PS2, Xbox, and MUA1 360", "Xbox"), ("PC, PS2, Xbox, and MUA1 360", "PS2"), ("PC, Xbox, and MUA1 360", "PC and MUA1 360"), ("PC, Xbox, and MUA1 360", "Xbox"), ("PS2", "PS2"), ("GameCube, PSP, and MUA2 PS2", "GameCube, PSP, and MUA2 PS2"), ("PC and MUA1 360", "PC and MUA1 360"), ("Xbox", "Xbox")]
        else:
            # The model is being process for PC only.
            # Set up the texture folder list with PNG8 texture options that are compatible with PC only.
            textureFolderList = [("PC", "PC")]
    elif dxt1Counter == len(texFolderList):
        # This is DXT1 format.
        # Determine if this is for PC or consoles, which will determine which texture list to use.
        if settings["pcOnly"] == False:
            # The model is being processed for all consoles.
            # Set up the texture folder list with DXT1 texture options that are compatible with all consoles.
            textureFolderList = [("XML2 PC, Xbox, and Wii", "XML2 PC"), ("XML2 PC, Xbox, and Wii", "Xbox and Wii"), ("Wii", "Wii"), ("Wii", "Xbox and Wii")]
        else:
            # The model is being process for PC only.
            # Set up the texture folder list with DXT1 texture options that are compatible with PC only.
            textureFolderList = [("XML2 PC", "XML2 PC")]
    elif plainPngCounter == len(texFolderList):
        # This is plain png format, which isn't allowed. Environment maps can't be in plain png format.
        # Print an error to let the user know.
        questions.printError("igbFinisher determined that a plain png diffuse texture is being used with plain png environment maps. Plain png environment maps are not supported.", False)
        # Create a blank list to avoid any errors.
        textureFolderList = []
    else:
        # No format counter is the same as the length of the texture format list.
        # Notify the user of the error. There's really no way this should happen unless there's something super weird going on, but I'm adding it for extra error security.
        questions.printError("igbFinisher determined that the model only uses one texture format and uses environment maps, but no texture format counter is the same as the length of the texture format list.", True)
        # Create a blank list to avoid any errors.
        textureFolderList = []
    # Initiate a counter to keep track of whether or not a folder option is found in the model's list of folders
    folderFound = 0
    # Loop through the available folder options that were generated earlier.
    for folderPair in textureFolderList:
        # Determine if the folders can be found in the list of folders for the model.
        if ((folderPair[0] in texFolderList) and (folderPair[1] in texFolderList)):
            # Both folders can be found in the folder list, meaning that an acceptable folder was found.
            # Set up the variables for the two folders.
            diffuseFolder = folderPair[0]
            envFolder = folderPair[1]
            # Increment the counter to indicate that a folder has been detected.
            folderFound += 1
    # Determine if a folder has been found, which will happen when the counter is 1.
    if folderFound == 1:
        # A texture folder was found, meaning that the folder was recognized.
        # Set up the texture format using the folders found earlier.
        textureFormat = f"Main texture: {diffuseFolder} / Environment texture: {envFolder}"
        # Print a success message to let the user know that the folder was identified.
        questions.printSuccess(f"The diffuse texture folder was automatically identified as {diffuseFolder}. The environment map folder was automatically identified as {envFolder}.")
    elif folderFound == 0:
        # No folder was found, so an acceptable folder is not in use.
        # Initialize a string to let the user know about the error.
        errorString = "The texture folders could not be recognized.\nDetected texture folders: "
        # Get a list of the unique folders in the model's list of texture folders. This is to ensure that no folders repeat in the error string.
        uniqueFolders = getUniqueFolders(texFolderList)
        # Loop through the list of unique folders to report which were identified.
        for folder in uniqueFolders:
            # Add the folder to the error string.
            errorString += (f"{folder} / ")
        # Print the error so that the user can see which folders the model has.
        questions.printError(errorString, False)
        # In order to have a return variable for this case, set the texture format to "None" again.
        textureFormat = None
    else:
        # More than 1 folder was found, which shouldn't be possible. This is being added for extra error security.
        questions.printError("igbFinisher determined the texture folders used by the model match more than one texture folder option for this format.", True)
        # In order to have a return variable for this case, set the texture format to "None" again.
        textureFormat = None
    # Return the collected texture format for further processing.
    return textureFormat

# Define the function for getting the texture folder in the case where plain png textures are used with environment maps
def transparentEnvironmentMaps(png8Counter, dxt1Counter, plainPngCounter, texFolderList, settings):
    # Compare the texture format counters to determine which environment map format is being used. This could lead to false positives if the format was botched somehow, but it's unlikely.
    if png8Counter > 1:
        # The environment maps use PNG8 textures. 
        # Determine if this is for PC or consoles, which will determine which texture list to use.
        if settings["pcOnly"] == False:
            # The model is being processed for all consoles.
            # Set up the texture folder list with plain png texture options that are compatible with all consoles.
            textureFolderList = [("PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360", "PC and MUA1 360"), ("PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360", "Xbox"), ("PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360", "PS2"), ("PC, Wii, Xbox, MUA1 Steam, PS3, and 360", "PC and MUA1 360"), ("PC, Wii, Xbox, MUA1 Steam, PS3, and 360", "Xbox"), ("PS2", "PS2"), ("GameCube, PSP, and MUA2 PS2", "GameCube, PSP, and MUA2 PS2")]
        else:
            # The model is being process for PC only.
            # Set up the texture folder list with plain png texture options that are compatible with PC only.
            textureFolderList = [("PC and MUA1 Steam", "PC")]
    elif dxt1Counter > 1:
        # The environment maps use DXT1 textures.
        # Determine if this is for PC or consoles, which will determine which texture list to use.
        if settings["pcOnly"] == False:
            # The model is being processed for all consoles.
            # Set up the texture folder list with plain png texture options that are compatible with all consoles.
            textureFolderList = [("PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360", "XML2 PC"), ("PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360", "Xbox and Wii"), ("PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360", "Wii"), ("PC, Xbox, Wii, MUA1 Steam, PS3, and 360", "XML2 PC"), ("PC, Xbox, Wii, MUA1 Steam, PS3, and 360", "Xbox and Wii"), ("PC, Xbox, Wii, MUA1 Steam, PS3, and 360", "Wii")]
        else:
            # The model is being process for PC only.
            # Set up the texture folder list with plain png texture options that are compatible with PC only.
            textureFolderList = [("PC and MUA1 Steam", "XML2 PC")]
    else:
        # The environment maps use neither DXT1 nor PNG8 format, which shouldn't be possible.
        # Let the user know that this shouldn't be possible.
        questions.printError("igbFinisher determined that the model has a transparent diffuse texture with environment maps, but neither PNG8 nor DXT1 counters were more than 1.", True)
        # Create a blank list to avoid any errors.
        textureFolderList = []
    # Initiate a counter to keep track of whether or not a folder option is found in the model's list of folders
    folderFound = 0
    # Loop through the available folder options that were generated earlier.
    for folderPair in textureFolderList:
        # Determine if the folders can be found in the list of folders for the model.
        if ((folderPair[0] in texFolderList) and (folderPair[1] in texFolderList)):
            # Both folders can be found in the folder list, meaning that an acceptable folder was found.
            # Set up the variables for the two folders.
            diffuseFolder = folderPair[0]
            envFolder = folderPair[1]
            # Increment the counter to indicate that a folder has been detected.
            folderFound += 1
    # Determine if a folder has been found, which will happen when the counter is 1.
    if folderFound == 1:
        # A texture folder was found, meaning that the folder was recognized.
        # Set up the texture format using the folders found earlier.
        textureFormat = f"Main texture: {diffuseFolder} / Environment Texture: {envFolder}"
        # Print a success message to let the user know that the folder was identified.
        questions.printSuccess(f"The diffuse texture folder was automatically identified as {diffuseFolder}. The environment map folder was automatically identified as {envFolder}.")
    elif folderFound == 0:
        # No folder was found, so an acceptable folder is not in use.
        # Initialize a string to let the user know about the error.
        errorString = "The texture folders could not be recognized.\nDetected texture folders: "
        # Get a list of the unique folders in the model's list of texture folders. This is to ensure that no folders repeat in the error string.
        uniqueFolders = getUniqueFolders(texFolderList)
        # Loop through the list of unique folders to report which were identified.
        for folder in uniqueFolders:
            # Add the folder to the error string.
            errorString += (f"{folder} / ")
        # Print the error so that the user can see which folders the model has.
        questions.printError(errorString, False)
        # In order to have a return variable for this case, set the texture format to "None" again.
        textureFormat = None
    else:
        # More than 1 folder was found, which shouldn't be possible. This is being added for extra error security.
        questions.printError("igbFinisher determined the texture folders used by the model match more than one texture folder option for this format.", True)
        # In order to have a return variable for this case, set the texture format to "None" again.
        textureFormat = None
    # Return the collected texture format for further processing.
    return textureFormat

# Define the function for getting the texture folder in the case where plain png textures are used with opaque textures
def transparentAndOpaque(png8Counter, dxt1Counter, plainPngCounter, texFolderList, settings):
    # Compare the texture format counters to determine which environment map format is being used. This could lead to false positives if the format was botched somehow, but it's unlikely.
    if png8Counter > 1:
        # The environment maps use PNG8 textures. 
        # Determine if this is for PC or consoles, which will determine which texture list to use.
        if settings["pcOnly"] == False:
            # The model is being processed for all consoles.
            # Set up the texture folder list with plain png texture options that are compatible with all consoles.
            textureFolderList = [("PC, PS2, Xbox, and MUA1 360", "PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360"), ("PC, Xbox, and MUA1 360", "PC, Wii, Xbox, MUA1 Steam, PS3, and 360"), ("PS2", "PS2"), ("GameCube, PSP, and MUA2 PS2", "GameCube, PSP, and MUA2 PS2")]
        else:
            # The model is being process for PC only.
            # Set up the texture folder list with plain png texture options that are compatible with PC only.
            textureFolderList = [("PC", "PC and MUA1 Steam")]
    elif dxt1Counter > 1:
        # The environment maps use DXT1 textures.
        # Determine if this is for PC or consoles, which will determine which texture list to use.
        if settings["pcOnly"] == False:
            # The model is being processed for all consoles.
            # Set up the texture folder list with plain png texture options that are compatible with all consoles.
            textureFolderList = [("MUA1 PC, Steam, 360, and PS3", "PC, Wii, Xbox, MUA1 Steam, PS3, and 360"), ("XML2 PC, Xbox, and Wii", "PC, Wii, Xbox, MUA1 Steam, PS3, and 360"), ("Wii", "PC, Wii, Xbox, MUA1 Steam, PS3, and 360")]
        else:
            # The model is being process for PC only.
            # Set up the texture folder list with plain png texture options that are compatible with PC only.
            textureFolderList = [("MUA1 PC and Steam", "PC and MUA1 Steam"), ("XML2 PC", "PC and MUA1 Steam")]
    else:
        # The environment maps use neither DXT1 nor PNG8 format, which shouldn't be possible.
        # Let the user know that this shouldn't be possible.
        questions.printError("igbFinisher determined that the model has transparent and opaque diffuse textures with environment maps, but neither PNG8 nor DXT1 counters were more than 1.", True)
        # Create a blank list to avoid any errors.
        textureFolderList = []
    # Initiate a counter to keep track of whether or not a folder option is found in the model's list of folders
    folderFound = 0
    # Loop through the available folder options that were generated earlier.
    for folderPair in textureFolderList:
        # Determine if the folders can be found in the list of folders for the model.
        if ((folderPair[0] in texFolderList) and (folderPair[1] in texFolderList)):
            # Both folders can be found in the folder list, meaning that an acceptable folder was found.
            # Set up the variables for the two folders.
            diffuseOFolder = folderPair[0]
            diffuseTFolder = folderPair[1]
            # Increment the counter to indicate that a folder has been detected.
            folderFound += 1
    # Determine if a folder has been found, which will happen when the counter is 1.
    if folderFound == 1:
        # A texture folder was found, meaning that the folder was recognized.
        # Set up the texture format using the folders found earlier.
        textureFormat = diffuseFolder
        # Print a success message to let the user know that the folder was identified.
        questions.printSuccess(f"The opaque diffuse texture folder was automatically identified as {diffuseOFolder}. The transparent diffuse texture folder was automatically identified as {diffuseTFolder}.")
    elif folderFound == 0:
        # No folder was found, so an acceptable folder is not in use.
        # Initialize a string to let the user know about the error.
        errorString = "The texture folders could not be recognized.\nDetected texture folders: "
        # Get a list of the unique folders in the model's list of texture folders. This is to ensure that no folders repeat in the error string.
        uniqueFolders = getUniqueFolders(texFolderList)
        # Loop through the list of unique folders to report which were identified.
        for folder in uniqueFolders:
            # Add the folder to the error string.
            errorString += (f"{folder} / ")
        # Print the error so that the user can see which folders the model has.
        questions.printError(errorString, False)
        # In order to have a return variable for this case, set the texture format to "None" again.
        textureFormat = None
    else:
        # More than 1 folder was found, which shouldn't be possible. This is being added for extra error security.
        questions.printError("igbFinisher determined the texture folders used by the model match more than one texture folder option for this format.", True)
        # In order to have a return variable for this case, set the texture format to "None" again.
        textureFormat = None
    # Return the collected texture format for further processing.
    return textureFormat

# Define the function for getting the texture folder in the case where there are transparent textures, opaque textures, and environment maps
def tripleFormat(png8Counter, dxt1Counter, plainPngCounter, texFolderList, settings):
    # Compare the texture format counters to determine which environment map format is being used. This could lead to false positives if the format was botched somehow, but it's unlikely.
    if png8Counter > 1:
        # The environment maps use PNG8 textures. 
        # Determine if this is for PC or consoles, which will determine which texture list to use.
        if settings["pcOnly"] == False:
            # The model is being processed for all consoles.
            # Set up the texture folder list with plain png texture options that are compatible with all consoles.
            textureFolderList = [("PC, PS2, Xbox, and MUA1 360", "PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360", "PC and MUA1 360"), ("PC, PS2, Xbox, and MUA1 360", "PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360", "Xbox"), ("PC, PS2, Xbox, and MUA1 360", "PC, PS2, Xbox, Wii, MUA1 Steam, PS3, and 360", "PS2"), ("PC, Xbox, and MUA1 360", "PC, Wii, Xbox, MUA1 Steam, PS3, and 360", "PC and MUA1 360"), ("PC, Xbox, and MUA1 360", "PC, Wii, Xbox, MUA1 Steam, PS3, and 360", "Xbox"), ("PS2", "PS2", "PS2"), ("GameCube, PSP, and MUA2 PS2", "GameCube, PSP, and MUA2 PS2", "GameCube, PSP, and MUA2 PS2")]
        else:
            # The model is being process for PC only.
            # Set up the texture folder list with plain png texture options that are compatible with PC only.
            textureFolderList = [("PC", "PC and MUA1 Steam", "PC")]
    elif dxt1Counter > 1:
        # The environment maps use DXT1 textures.
        # Determine if this is for PC or consoles, which will determine which texture list to use.
        if settings["pcOnly"] == False:
            # The model is being processed for all consoles.
            # Set up the texture folder list with plain png texture options that are compatible with all consoles.
            textureFolderList = [("MUA1 PC, Steam, 360, and PS3", "PC, PS2, Wii, Xbox, MUA1 Steam, PS3, and 360", "MUA1 PC, Steam, 360, and PS3"), ("XML2 PC, Xbox, and Wii", "PC, PS2, Wii, Xbox, MUA1 Steam, PS3, and 360", "XML2 PC"), ("XML2 PC, Xbox, and Wii", "PC, PS2, Wii, Xbox, MUA1 Steam, PS3, and 360", "Xbox and Wii"), ("Wii", "PC, PS2, Wii, Xbox, MUA1 Steam, PS3, and 360", "Wii"), ("Wii", "PC, PS2, Wii, Xbox, MUA1 Steam, PS3, and 360", "Xbox and Wii"), ("MUA1 PC, Steam, 360, and PS3", "PC, Wii, Xbox, MUA1 Steam, PS3, and 360", "MUA1 PC, Steam, 360, and PS3"), ("XML2 PC, Xbox, and Wii", "PC, Wii, Xbox, MUA1 Steam, PS3, and 360", "XML2 PC"), ("XML2 PC, Xbox, and Wii", "PC, Wii, Xbox, MUA1 Steam, PS3, and 360", "Xbox and Wii"), ("Wii", "PC, Wii, Xbox, MUA1 Steam, PS3, and 360", "Wii"), ("Wii", "PC, Wii, Xbox, MUA1 Steam, PS3, and 360", "Xbox and Wii")]
        else:
            # The model is being process for PC only.
            # Set up the texture folder list with plain png texture options that are compatible with PC only.
            textureFolderList = [("MUA1 PC and Steam", "PC and MUA1 Steam", "MUA1 PC and Steam"), ("XML2 PC", "PC and MUA1 Steam", "XML2 PC")]
    else:
        # The environment maps use neither DXT1 nor PNG8 format, which shouldn't be possible.
        # Let the user know that this shouldn't be possible.
        questions.printError("igbFinisher determined that the model has transparent and opaque diffuse textures with environment maps, but neither PNG8 nor DXT1 counters were more than 1.", True)
        # Create a blank list to avoid any errors.
        textureFolderList = []
    # Initiate a counter to keep track of whether or not a folder option is found in the model's list of folders
    folderFound = 0
    # Loop through the available folder options that were generated earlier.
    for folderTriple in textureFolderList:
        # Determine if the folders can be found in the list of folders for the model.
        if ((folderTriple[0] in texFolderList) and (folderTriple[1] in texFolderList) and (folderTriple[2] in texFolderList)):
            # All three folders can be found in the folder list, meaning that an acceptable folder was found.
            # Set up the variables for the two folders.
            diffuseOFolder = folderPair[0]
            diffuseTFolder = folderPair[1]
            envFolder = folderPair[2]
            # Increment the counter to indicate that a folder has been detected.
            folderFound += 1
    # Determine if a folder has been found, which will happen when the counter is 1.
    if folderFound == 1:
        # A texture folder was found, meaning that the folder was recognized.
        # Set up the texture format using the folders found earlier.
        textureFormat = f"Main texture: {diffuseOFolder} / Environment Texture: {envFolder}"
        # Print a success message to let the user know that the folder was identified.
        questions.printSuccess(f"The opaque diffuse texture folder was automatically identified as {diffuseOFolder}. The transparent diffuse texture folder was automatically identified as {diffuseTFolder}. The environment map folder was automatically identified as {envFolder}.")
    elif folderFound == 0:
        # No folder was found, so an acceptable folder is not in use.
        # Initialize a string to let the user know about the error.
        errorString = "The texture folders could not be recognized.\nDetected texture folders: "
        # Get a list of the unique folders in the model's list of texture folders. This is to ensure that no folders repeat in the error string.
        uniqueFolders = getUniqueFolders(texFolderList)
        # Loop through the list of unique folders to report which were identified.
        for folder in uniqueFolders:
            # Add the folder to the error string.
            errorString += (f"{folder} / ")
        # Print the error so that the user can see which folders the model has.
        questions.printError(errorString, False)
        # In order to have a return variable for this case, set the texture format to "None" again.
        textureFormat = None
    else:
        # More than 1 folder was found, which shouldn't be possible. This is being added for extra error security.
        questions.printError("igbFinisher determined the texture folders used by the model match more than one texture folder option for this format.", True)
        # In order to have a return variable for this case, set the texture format to "None" again.
        textureFormat = None
    # Return the collected texture format for further processing.
    return textureFormat

# Define the function to get texture formats for 3D assets
def get3DTextureFormat(assetType, settings, fullFileName):
    # Call the function to get the texture information from Alchemy for this file. Return a list of the texture paths and another of the texture formats.
    (texPathList, texFormatList) = alchemy.GetTexPath(fullFileName)
    # Initialize the texture format as a None variable. This way, if a format is not detected, it doesn't have to be set as anything. But if one is detected, it can be overwritten.
    textureFormat = None
    # Determine the number of textures to ensure that there actually are textures.
    if len(texPathList) == 0:
        # No textures were found.
        # Give a warning to let the user know. Textures are generally required for the program to work correctly.
        questions.printWarning("No textures were found in the model.")
        # Ask the user if the model is supposed to have textures.
        needsTex = questions.confirm("Is this model supposed to have textures?", True)
        # Determine what the user answered.
        if needsTex == True:
            # The model is supposed to have textures.
            # Print an error to let the user know that they must try again with a texture applied.
            questions.printError("The model is supposed to have textures, but none were detected. Please apply textures, re-export the model, and try again.", False)
        else:
            # The model is not supposed to have textures.
            # Warn the user that this will go to every console.
            questions.printWarning("If the model does not use textures and only uses plain colors, it will be exported for every console available.")
            # Set the texture format
            textureFormat = "No Texture"
    else:
        # There are one or more textures.
        # Determine which texture formats are being used.
        (png8Counter, dxt1Counter, plainPngCounter, texFolderList) = recognize3DTextureFormat(texPathList, texFormatList)
        # Determine if all formats are acceptable. The number of formats detected should be equal to the length of the list of texture formats.
        if (png8Counter + dxt1Counter + plainPngCounter) == len(texFormatList):
            # The number of detected formats is equal to the length of the format list, so all formats were detected.
            # Determine if there is a mix of formats, which will happen if no texture format counter is the same as the length of the texture format list.
            if ((png8Counter < len(texFormatList)) and (dxt1Counter < len(texFormatList)) and (plainPngCounter < len(texFormatList))):
                # Because each format counter is smaller than the length of the list of texture formats, there is a mix of formats.
                # Determine if there are both PNG8 and DXT1 textures
                if ((png8Counter > 0) and (dxt1Counter > 0)):
                    # There are both PNG8 and DXT1 textures. 
                    # Print an error to let the user know that this isn't allowed, because it makes optimization difficult and restricts compatibility. Using proper export settings with the GIMP scripts shouldn't allow this to happen.
                    questions.printError("This model uses both PNG8 and DXT1 textures. This isn't allowed because it limits compatibility. Please try again.", True)
                else:
                    # The model has at least one plain png texture, and the other texture(s) are PNG8 or DXT1, but not both.
                    # Determine if there is a "sphereImage" in the list of texture folders, which would indicate that there are environment maps in use.
                    if "sphereImage" in texFolderList:
                        # There is a sphereImage, so environment maps are in use.
                        # Get the list of unique texture folders from the model's list of texture folders. The 6 components of the environment map will all be listed as separate textures but with the same folder, so repeats need to be removed.
                        uniqueFolders = getUniqueFolders(texFolderList)
                        # Determine the number of unique folders.
                        if len(uniqueFolders) == 2:
                            # There are two folders, meaning that there's a transparent diffuse texture with environment maps (theoretically, it would be possible to get here with transparent environment maps and an opaque diffuse texture, but that would take some real skill, and it wouldn't produce an accepted format anyways).
                            # Determine which format is actually in use.
                            textureFormat = transparentEnvironmentMaps(png8Counter, dxt1Counter, plainPngCounter, texFolderList, settings)
                        elif len(uniqueFolders) == 3:
                            # There are three folders, meaning that there's a transparent diffuse texture, an opaque diffuse texture, and environment maps (theoretically, it would also be possible to get here with some botched combination of 3 folders, but once again, that would take some real skill, and it wouldn't produce an accepted format anyways).
                            # Determine which format is actually in use.
                            textureFormat = tripleFormat(png8Counter, dxt1Counter, plainPngCounter, texFolderList, settings)
                        elif len(uniqueFolders) > 3:
                            # More than 3 unique folders were found, which means that the user set up the model incorrectly.
                            # Inform the user of this error so that they can reduce the number of different texture folders.
                            questions.printError("More than 3 texture folders were found. When using environment maps and transparent textures, a maximum of 3 folders is allowed: 1 for the transparent diffuse texture(s), 1 for the opaque diffuse texture(s) (if applicable), and 1 for the environment map(s).", False)
                        else:
                            # 1 or fewer unique folders were found somehow. This shouldn't happen, and the user could only get here through some critical programming flaw.
                            # Print an error so that the user knows that this shouldn't happen and to report the issue.
                            questions.printError("igbFinisher determined that the model is using textures of different formats, and that it is using environment maps, but the number of unique formats was determined to be less than 2.", True)
                    else:
                        # There is no sphereImage, so environment maps are not in use. This means that there is an opaque texture (PNG8 or DXT1) is being used with a transparent texture (plain png).
                        # Get the list of unique texture folders from the model's list of texture folders.
                        uniqueFolders = getUniqueFolders(texFolderList)
                        # Determine the number of unique folders.
                        if len(uniqueFolders) == 2:
                            # There are two folders, meaning that there's one opaque folder and one transparent folder, which is the only allowed mix format without environment maps.
                            # Determine which format is actually in use.
                            textureFormat = transparentAndOpaque(png8Counter, dxt1Counter, plainPngCounter, texFolderList, settings)
                        elif len(uniqueFolders) > 2:
                            # More than 2 unique folders were found, which means that the user set up the model incorrectly.
                            # Inform the user of this error so that they can reduce the number of different texture folders.
                            questions.printError("More than 2 texture folders were found. When using opaque and transparent textures, a maximum of 2 folders is allowed: 1 for the transparent diffuse texture(s) and 1 for the opaque diffuse texture(s).", False)
                        else:
                            # 1 or fewer unique folders were found somehow. This shouldn't happen, and the user could only get here through some critical programming flaw.
                            # Print an error so that the user knows that this shouldn't happen and to report the issue.
                            questions.printError("igbFinisher determined that the model is using textures of different formats without environment maps, but the number of unique formats was determined to be less than 2.", True)                       
            else:
                # All textures are the same texture format, which is preferred.
                # Determine if all elements of the texture folder list are the same, which would indicate that only one texture folder was used.
                if len(list(set(texFolderList))) == 1:
                    # All texture folders are the same, so all textures use the same texture folder.
                    # Determine which texture folder was used. This is the easiest, since everything is the same.
                    textureFormat = oneFormatOneFolder(png8Counter, dxt1Counter, plainPngCounter, texFolderList, settings)
                else:
                    # All texture formats are the same, but the textures come from different texture folders. This is only allowed if there are environment maps.
                    # Determine if there is a "sphereImage" in the list of texture folders, which would indicate that there are environment maps in use.
                    if "sphereImage" in texFolderList:
                        # There is a sphereImage, so environment maps are in use.
                        # Get the list of unique texture folders from the model's list of texture folders. The 6 components of the environment map will all be listed as separate textures but with the same folder, so repeats need to be removed.
                        uniqueFolders = getUniqueFolders(texFolderList)
                        # Determine if there is the right number of folders. If environment maps are used, only two folders can be used: one for the diffuse texture and one for the environment maps. There are some cases (like PS2 textures when the diffuse texture is separate, all Wii textures, or the GameCube, PSP, and MUA2 PS2 textures) where the folders will be the same, so that's why 1 or 2 folders is allowed.
                        if ((len(uniqueFolders) == 1) or (len(uniqueFolders) == 2)):
                            # The number of unique texture folders is acceptable, so the determination can now happen.
                            # Determine which format is actually in use.
                            textureFormat = oneFormatEnvironmentMaps(png8Counter, dxt1Counter, plainPngCounter, texFolderList, settings)
                        else:
                            # The number of folders was incorrect, meaning that the model can't be processed.
                            # Determine if there were more than 2 folders found. That could happen through user error. If there are less than 1, then there's a problem.
                            if len(uniqueFolders) > 2:
                                # There are more than 2 folders, which can happen through user error (the user not picking the right folders)
                                # Print an error to let the user know that this isn't allowed.
                                questions.printError("More than 2 texture folders were found. When using environment maps, only 2 texture folders can be used: 1 for the diffuse texture(s), and 1 for the environment map(s).", False)
                            else:
                                # 0 (or even worse, negative) unique folders were found somehow. This shouldn't happen, and the user could only get here through some critical programming flaw.
                                # Print an error so that the user knows that this shouldn't happen and to report the issue.
                                questions.printError("igbFinisher determined that the model is using all textures of the same format, and that it is using environment maps, but the number of unique formats was determined to be less than 1.", True)
                    else:
                        # There is no sphereImage, so environment maps are not in use. As such, multiple folders are not allowed.
                        # Let the user know that they can't do this.
                        questions.printError("Textures from multiple folders were used. This is only allowed if environment maps are in use, and no environment maps were detected.", False)
        else:
            # Not all formats are acceptable
            questions.printError("One or more texture formats is not accepted. Please try again.", False)
    # Return the collected value
    return textureFormat