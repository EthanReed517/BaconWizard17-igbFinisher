# ########### #
# INFORMATION #
# ########### #
# This module is used to determine the texture formats for loading screens


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import questions
# External modules
import os.path


# ######### #
# FUNCTIONS #
# ######### #
# Define the function to recognize the texture format.
def recognizeLoadTextureFormat(texPathList, texFormatList):
    # Initialize the counters for the acceptable texture formats. These will keep track of how many textures of each format are found.
    png8Counter = 0
    dxt1Counter = 0
    # Get the name of the folder that the texture is stored in. This is the second to last element in the path.
    texFolder = texPathList[0].split("\\")[-2]
    # Get the name of the texture file. This is the last element in the path.
    texFile = texPathList[0].split("\\")[-1]
    # The texture format list should only have one element, so set the format to be the first item in the list.
    texFormat = texFormatList[0]
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
        # Increment the counter for plain png textures.
        questions.PrintError("This model uses a png texture that's uncompressed with an alpha channel (plain png texture). This texture format is not supported by igbFinisher. Please choose a different texture.")
    elif texFormat == "IG_GFX_TEXTURE_FORMAT_X_4 (65537)":
        # This format is a png file with PNG4 compression, which is not supported. 
        # Give an error to let the user know that this format isn't allowed. It's not supported because PNG4 is only used on the PSP and only for some assets; taking out PNG4 compatibility reduces the number of texture options and makes processing easier.
        questions.PrintError("This model uses a png texture that's in PNG4 format. This texture format is not supported by igbFinisher. Please choose a different texture.")
    elif texFormat == "IG_GFX_TEXTURE_FORMAT_RGB_888_24 (5)":
        # This format is a png file with no compression but no alpha channel, which is not supported.
        # Give an error to let the user know that this format isn't allowed. It's not supported because uncompressed png files bring up file sizes significantly with no benefits to the texture (since there's no alpha channel, they can't even have transparency).
        questions.PrintError("This model uses a png texture that's uncompressed without an alpha channel (no transparency). This texture format is not supported by igbFinisher. Please choose a different texture.")
    elif texFormat == "IG_GFX_TEXTURE_FORMAT_RGBA_DXT3 (15)":
        # This format is a dds file with DXT3 compression, which is not supported.
        # Give an error to let the user know that this format isn't allowed. It's not supported because DXT3 is compatible with fewer consoles; the Marvel Mods GIMP scripts don't even export with it for that reason, so there's no reason that it would show up here.
        questions.PrintError("This model uses a dds texture that's in DXT3 format. This texture format is not supported by igbFinisher. Please choose a different texture.")
    elif texFormat == "IG_GFX_TEXTURE_FORMAT_RGBA_DXT5 (16)":
        # This format is a dds file with DXT5 compression, which is not supported.
        # Give an error to let the user know that this format isn't allowed. It's not supported because DXT5 is compatible with fewer consoles; the Marvel Mods GIMP scripts don't even export with it for that reason, so there's no reason that it would show up here.
        questions.PrintError("This model uses a dds texture that's in DXT5 format. This texture format is not supported by igbFinisher. Please choose a different texture.")
    else:
        # The format was not recognized at all.
        # Give an error to let the user know. This technically shouldn't happen because the previous options cover all the common formats, but there are some fringe formats that can be exported if you know how to do it.
        questions.PrintError(f"A texture format used by this model is not recognized. Please choose a different texture.\nTexture format \"{texFormat}\".")
    # Return the collected variables: the number of PNG8 textures found in the model, the number of DXT1 textures found in the model, the number of plain png textures found in the model, and the texture folder and file name.
    return png8Counter, dxt1Counter, texFolder, texFile

# Define the function for finding the texture folder in the list of texture folders.
def findFolder(texFolder, textureFolderList):
    # Determine if the texture folder can be found in the list of texture folders that was created earlier. Since all folders are the same, the first item from the list is taken.
    if texFolder in textureFolderList:
        # The texture folder used by the model can be found in the list of texture folders that was created earlier.
        # Set the format to be this folder.
        textureFormat = texFolder
        # Print a success message to inform the user that there is a match.
        questions.PrintSuccess(f"The texture folder was automatically identified as {textureFormat}.")
    else:
        # The texture folder used by the model can't be found in the list of texture folders that was created earlier.
        # Print the error to inform the user that the texture folder couldn't be matched to an acceptable format. This can happen if they exported without using the Marvel Mods GIMP Scripts or if they dropped the textures from outside of the VM.
        questions.PrintError(f"The texture folder, {texFolder}, could not be recognized. Make sure that you're exporting your textures with the Marvel Mods GIMP Scripts and adding the textures from within the VM. Please try again.")
        # In order to have a return variable for this case, set the texture format to "None" again.
        textureFormat = None
    # Return the collected texture format for further processing.
    return textureFormat

# Define the function to get texture formats for 3D assets
def getLoadTextureFormat(settings, fullFileName):
    # Call the function to get the texture information from Alchemy for this file. Return a list of the texture paths and another of the texture formats.
    (texPathList, texFormatList) = alchemy.GetTexPath(fullFileName)
    # Initialize the texture format as a None variable. This way, if a format is not detected, it doesn't have to be set as anything. But if one is detected, it can be overwritten.
    textureFormat = None
    # Initialize the file name as a None variable. This way, if an incorrect format is detected, it doesn't have to be set as anything. But if one is detected, it can be overwritten.
    fileName = None
    # Determine the number of textures to ensure that the model was set up correctly.
    if len(texPathList) == 0:
        # No textures were found.
        # Give an error to let the user know. Textures are required for igbFinisher to work, so no other operations are performed.
        questions.PrintError("No textures were found in the model. Please try again.")
    elif len(texPathList) == 1:
        # One texture was found. This is the correct number of textures.
        # Determine which texture format is being used.
        (png8Counter, dxt1Counter, texFolder, texFile) = recognizeLoadTextureFormat(texPathList, texFormatList)
        # Get the file name
        fileName = os.path.splitext(texFile)[0]
        # Determine the texture format
        if png8Counter == 1:
            # This is an indexed texture
            # Determine if this is for PC or consoles, which will determine which texture list to use.
            if settings["pcOnly"] == False:
                # The model is being processed for all consoles.
                # Set up the texture folder list with png8 texture options that are compatible with all consoles.
                textureFolderList = ["XML1 and XML2 PS2", "XML2 PSP", "MUA1 and MUA2 PS2 and PSP"]
            else:
                # The model is being process for PC only.
                # Set up the texture folder list with png8 texture options that are compatible with PC only.
                textureFolderList = []
            # Determine the format that's in use.
            textureFormat = findFolder(texFolder, textureFolderList)
        elif dxt1Counter == 1:
            # This is a dxt1 texture
            # Determine if this is for PC or consoles, which will determine which texture list to use.
            if settings["pcOnly"] == False:
                # The model is being processed for all consoles.
                # Set up the texture folder list with DXT1 texture options that are compatible with all consoles.
                textureFolderList = ["XML2 PC", "XML1 and XML2 Xbox", "XML1 Xbox, XML2 PC and Xbox", "XML1 and XML2 GameCube", "MUA1 PC and Steam", "MUA1 PS3 and 360", "MUA1 Next-Gen", "MUA1 Wii and Xbox, MUA2 Wii"]
            else:
                # The model is being process for PC only.
                # Set up the texture folder list with DXT1 texture options that are compatible with PC only.
                textureFolderList = ["XML2 PC", "MUA1 PC and Steam"]
            # Determine the format that's in use.
            textureFormat = findFolder(texFolder, textureFolderList)
        else:
            # No recognized format was found.
            # Do nothing here, just needed to catch this case and make sure it's not processed.
            pass
    else:
        # Two or more textures were found, which means that the model was set up incorrectly.
        # Give an error to let the user know.
        questions.PrintError("Two or more textures were found in the model. Loading screens should only have one texture applied. Please try again.")
    # Return the collected value
    return textureFormat