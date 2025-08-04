# ########### #
# INFORMATION #
# ########### #
# This module is used to recognize information about the model's textures.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import questions
import settings


# ######### #
# FUNCTIONS #
# ######### #
# This function is used to get the texture type.
def GetTextureType(textures_list, settings_dict, asset_type, input_file_path):
    # Check if there are any textures.
    if len(textures_list) == 0:
        # There are no textures.
        # Determine if this is an asset that requires textures.
        if asset_type in ['Skin', 'Mannequin', '3D Head', 'Other']:
            # This is an asset type that can be without textures.
            # Check if the user allowed these model types through.
            if settings_dict['untextured_okay'] == True:
                # It's okay for there to be no textures.
                # Set the texture type as None.
                texture_type = None
            else:
                # It's not okay for there to be no textures.
                # Give an error.
                questions.PrintError(f'{input_file_path.name} model has no textures. The settings have been configured to not allow models without textures.', system_exit = True)
        else:
            # This is an asset that can't be without textures.
            # Give an error.
            questions.PrintError(f'{input_file_path.name} model has no textures. Models of asset type {asset_type} must always have textures.', system_exit = True)
    else:
        # The model has textures.
        # Check if the count is greater than 1.
        if len(textures_list) > 1:
            # There is more than one texture.
            # Check if this is an asset that allows more than 1 texture.
            if not(asset_type in ['Skin', 'Mannequin', '3D Head', 'Other']):
                # This is not an asset type that allows more than 1 texture.
                # Give an error.
                questions.PrintError(f'{input_file_path.name} model has more than 1 texture. Models of type {asset_type} must always have 1 texture.', system_exit = True)
        # Assume that the texture type will be opaque.
        texture_type = 'Opaque'
        # Loop through the textures.
        for texture_dict in textures_list:
            # Get the texture format.
            if texture_dict['Format'] == 'IG_GFX_TEXTURE_FORMAT_RGB_888_24 (5)':
                # This is an opaque texture.
                # Do nothing.
                pass
            elif texture_dict['Format'] == 'IG_GFX_TEXTURE_FORMAT_RGB_8888_32 (7)':
                # This is a transparent texture.
                # Set the type to transparent.
                texture_type = 'Transparent'
            else:
                # This is some other texture type, which is not supported.
                # Print an error.
                questions.PrintError(f'Texture {texture_dict['Name']} uses format {texture_dict['Format']}, which is not supported. The supported texture formats are IG_GFX_TEXTURE_FORMAT_RGB_888_24 (5) (for opaque textures) or IG_GFX_TEXTURE_FORMAT_RGB_8888_32 (7) (for textures with transparency).', system_exit = True)
    # Determine what texture type was found and announce it.
    if texture_type == None:
        questions.PrintSuccess(f'{input_file_path.name} has no textures.')
    elif texture_type == 'Opaque':
        questions.PrintSuccess(f'{input_file_path.name} has only opaque textures.')
    else:
        questions.PrintSuccess(f'{input_file_path.name} has at least one transparent texture.')
    # Return the collected texture type.
    return texture_type

# This function is used to get the max texture size.
def GetMaxTextureSize(textures_list):
    # Start with the max size at 0.
    max_texture_size = 0
    # Loop through the textures.
    for texture_dict in textures_list:
        # Check if the width is bigger than the max size.
        if texture_dict['Width'] > max_texture_size:
            # The width is bigger than the max texture size.
            # Increase the max texture size to the width.
            max_texture_size = texture_dict['Width']
        # Check if the height is bigger than the max size.
        if texture_dict['Height'] > max_texture_size:
            # The height is bigger than the max texture size.
            # Increase the max texture size to the height.
            max_texture_size = texture_dict['Height']
    # Return the max size.
    return max_texture_size

# This function is used to check the texture path for folder detection.
def FolderDetection(textures_list, settings_dict, application_path):
    # Assume that detection is not needed.
    need_to_detect = False
    # Loop through the games.
    for game in settings.games_list:
        # Check if the path setting for this game is 'Detect'.
        if settings_dict[f'{game}_path'] == 'Detect':
            # Folder detection is in use for this game.
            # Set that it's necessary to detect.
            need_to_detect = True
    # Determine if it's necessary to detect.
    if need_to_detect == True:
        # It's necessary to detect.
        # Start a list of detectable textures.
        detectable_textures_list = []
        # Loop through the textures.
        for texture_dict in textures_list:
            # Check if this is a sphereImage
            if not(texture_dict['Name'] == 'sphereImage'):
                # This is not a sphereImage.
                # Check if this is a cubemap component.
                if not(texture_dict['Type'] in ['CubeNEG_X', 'CubePOS_X', 'CubeNEG_Y', 'CubePOS_Y', 'CubeNEG_Z', 'CubePOS_Z']):
                    # This is not a cubemap component.
                    # The texture can be used for detection.
                    detectable_textures_list.append(texture_dict)
        # Check if any textures were found.
        if detectable_textures_list == []:
            # No textures were found.
            # Give an error.
            questions.PrintError('At least one output path is set up for folder detection in the settings, but the model has no textures available for detection.', system_exit = True)
        # Set the initial texture folder path to the folder of the first available texture.
        texture_detection_path = detectable_textures_list[0]['Name'].parent

# This function is used to get the list of texture values that need to be hexed out.
def GetHexOutList(textures_list, asset_type):
    # Initialize a list of things to hex out.
    hex_out_list = []
    # Return the collected list.
    return hex_out_list

# This function is used to determine the environment map type.
def GetEnvironmentType(textures_list, settings_dict, asset_type, hex_out_list, input_file_path, texture_format):
    # Set an initial environment map size of 0.
    env_size = 0
    # Loop through the textures.
    for texture_dict in textures_list:
        # Determine if this is a sphereImage
        if texture_dict['Name'] == 'sphereImage':
            # There is an environment map.
            # Update the max size.
            if max(texture_dict['Width'], texture_dict['Height']) > env_size:
                env_size = max(texture_dict['Width'], texture_dict['Height'])
    # Determine if environment maps were found.
    if env_size > 0:
        # Environment maps were found.
        # Check if this is an asset that allows environment maps.
        if not(asset_type in ['Skin', 'Mannequin', '3D Head', 'Other']):
            # This asset does not allow environment maps.
            # Give an error.
            questions.PrintError(f'Environment maps were found in {input_file_path.name}, but assets of type {asset_type} cannot have environment maps.', system_exit = True)
        # Update the texture format.
        texture_format += " Env"
        # Set up the dictionary of consoles to allow for each size.
        console_allow_dict = {
            '32': 
    # Return the updated settings dictionary and hex out list.
    return settings_dict, hex_out_list

# This function is used to get the texture information from the model.
def GetTextureInfo(application_path, input_file_path, settings_dict, asset_type):
    # Get the texture information from Alchemy.
    textures_list = alchemy.GetTextureInfo(input_file_path)
    # Determine the texture type from the texture information.
    texture_type = GetTextureType(textures_list, settings_dict, asset_type, input_file_path)
    # Determine the max texture size for the model.
    max_texture_size = GetMaxTextureSize(textures_list)
    # Update the paths with folder detection.
    settings_dict = FolderDetection(textures_list, settings_dict, application_path)
    # Determine if any texture values need to be hexed out.
    hex_out_list = GetHexOutList(textures_list, asset_type)
    # Determine the environment map type from the texture information.
    settings_dict, hex_out_list = GetEnvironmentType(textures_list, settings_dict, asset_type, hex_out_list, input_file_path, texture_format)
    # Return the necessary information.
    return settings_dict, hex_out_list, texture_type, max_texture_size