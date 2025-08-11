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
def FolderDetection(textures_list, settings_dict, application_path, asset_type):
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
        # Start a list of texture folders.
        texture_folders_list = []
        # Loop through the detectable textures.
        for texture_dict in detectable_textures_list:
            # Determine if the texture folder is already in the list.
            if not(texture_dict['Name'].parent in texture_folders_list):
                # The folder is not in the list.
                # Add it to the list.
                texture_folders_list.append(texture_dict['Name'].parent)
        # Determine how many folders were found.
        if len(texture_folders_list) > 1:
            # Multiple folders were found.
            # Give an error.
            questions.PrintError('At least one output path is set up for folder detection in the settings, but the model uses multiple texture folders.', system_exit = True)
        # Get the character and sub-folder from the texture folder.
        character = texture_folders_list[0].parts[-3]
        asset_type_folder = texture_folders_list[0].parts[-2]
        sub_folder = texture_folders_list[0].parts[-1]
        # Loop through the games in the series.
        for game in settings.games_list:
            # Determine if detection is needed for this game.
            if settings_dict[f'{game}_path'] == 'Detect':
                # It's necessary to detect for this game.
                # Get the path.
                settings_dict[f'{game}_path'] = basic_xml_ops.GetOutputPath(game, application_path, character, asset_type_folder, sub_folder, asset_type)
    # Return the updated settings file.
    return settings_dict

# This function is used to get the list of texture values that need to be hexed out.
def GetHexOutList(textures_list, asset_type):
    # Initialize a list of things to hex out.
    hex_out_list = []
    # Determine if this is a portrait.
    if asset_type in ['Conversation Portrait', 'Character Select Portrait']:
        # This is a portrait.
        # Get the texture name.
        texture_name = textures_list[0].stem
        # Set up the dictionary of prefixes.
        prefix_dict = {'Conversation Portrait': ['b', 'g', 'r', 'ng'], 'Character Select Portrait': ['x1c', 'x2c']}
        # Loop through the possible prefixes.
        for prefix in prefix_dict[asset_type]:
            # Determine if the texture starts with one of these prefixes.
            if texture_name.startswith(f'{prefix}_'):
                # The texture starts with this prefix.
                # Update the hex editing list to remove this.
                hex_out_list.append([texture_name, texture_name[(len(prefix) + 1):]])
    # Return the collected list.
    return hex_out_list

# This function is used to set the output file names for 2D assets.
def Get2DAssetFileNames(settings_dict, asset_type, hex_out_list, textures_list):
    # Verify that this is a 2D asset that gets its file name from the texture name.
    if asset_type in ['Power Icons', 'Comic Cover', 'Concept Art']:
        # This is a 2D asset that gets its file name from the texture name.
        # Get the texture name.
        texture_name = textures_list[0].stem
        # Filter by asset type.
        if asset_type == 'Power Icons':
            # These are power icons.
            # Determine what game the icons are for.
            icons_game = texture_name.split('_')[0]
            # Loop through the games.
            for game in settings.games_list:
                # Determine if this matches the game.
                if game == icons_game:
                    # The games match.
                    # Update the settings accordingly.
                    settings_dict[f'{game}_special_name'] = texture_name
                    hex_out_list.append([texture_name, texture_name[5:]])
                    # Determine if this is an icons2 file.
                    if texture_name.endswith('icons2'):
                        # This is an icons2 file.
                        # Skip the consoles that don't use icons2.
                        settings_dict['GameCube'] = None
                        settings_dict['PS2'] = None
                        settings_dict['PSP'] = None
                else:
                    # This is another game.
                    # Update the settings accordingly.
                    settings_dict[f'{game}_num'] = None
                    settings_dict[f'{game}_path'] = None
        else:
            # This is a comic cover or concept art.
            # Loop through the games.
            for game in settings.games_list:
                # Update the name for that game.
                settings_dict[f'{game}_special_name'] = texture_name
    # Return the updated values.
    return settings_dict, hex_out_list

# This function is used to determine the environment map type.
def GetEnvironmentType(textures_list, settings_dict, asset_type, hex_out_list, input_file_path, texture_type):
    # Set an initial environment map size of 0.
    env_size = 0
    # Loop through the textures.
    for texture_dict in textures_list:
        # Determine if this is a sphereImage
        if str(texture_dict['Name']) == 'sphereImage':
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
        # If this is a PC size, set the size to 128 (standard size for PC).
        if env_size > 32:
            env_size = 128
        # Update the texture format.
        texture_type += f' Env{str(env_size)}'
        # Let the user know.
        questions.PrintSuccess('Detected environment maps.')
        # Match the size to the elements to remove in the replace list.
        size_match_dict = {'8': 'XS', '16': 'S', '32': 'M', '128': 'L'}
        size_suffix = size_match_dict[str(env_size)]
        # Add the textures to the hex out list.
        hex_out_list.extend([[f'_{size_suffix}_LF.png.cube', '_LF.png.cube'], [f'_{size_suffix}_RT.png.cube', '_RT.png.cube'], [f'_{size_suffix}_FR.png.cube', '_FR.png.cube'], [f'_{size_suffix}_BK.png.cube', '_BK.png.cube'], [f'_{size_suffix}_DN.png.cube', '_DN.png.cube'], [f'_{size_suffix}_UP.png.cube', '_UP.png.cube']])
    # Return the updated settings dictionary and hex out list.
    return settings_dict, hex_out_list, texture_type

# This function is used to get the game that the character select portrait is for.
def GetCSPGame(settings_dict, textures_list):
    # Determine what the texture name starts with.
    if textures_list['Name'].name.startswith('x1c'):
        # This is for XML1.
        # Skip processing for XML2.
        settings_dict['XML2_num'] = None
        settings_dict['XML2_path'] = None
    else:
        # This is for XML2.
        # Skip processing for XML1.
        settings_dict['XML1_num'] = None
        settings_dict['XML1_path'] = None
    # Return the updated settings.
    return settings_dict

# This function is used to get the texture information from the model.
def GetTextureInfo(application_path, input_file_path, settings_dict, asset_type):
    # Get the texture information from Alchemy.
    textures_list = alchemy.GetTextureInfo(input_file_path)
    # Determine the texture type from the texture information.
    texture_type = GetTextureType(textures_list, settings_dict, asset_type, input_file_path)
    # Determine the max texture size for the model.
    max_texture_size = GetMaxTextureSize(textures_list)
    # Update the paths with folder detection.
    settings_dict = FolderDetection(textures_list, settings_dict, application_path, asset_type)
    # Determine if any texture values need to be hexed out.
    hex_out_list = GetHexOutList(textures_list, asset_type)
    # Update file names for 2D assets.
    settings_dict, hex_out_list = Get2DAssetFileNames(settings_dict, asset_type, hex_out_list, textures_list)
    # Determine the environment map type from the texture information.
    settings_dict, hex_out_list, texture_type = GetEnvironmentType(textures_list, settings_dict, asset_type, hex_out_list, input_file_path, texture_type)
    # Determine if this is a CSP.
    if asset_type == 'Character Select Portrait':
        # This is a CSP.
        # Update processing based on the game.
        settings_dict = GetCSPGame(settings_dict, textures_list)
    # Build a dictionary of texture info.
    texture_info_dict = {'texture_type': texture_type, 'max_texture_size': max_texture_size, 'textures_list': textures_list}
    # Determine if it's necessary to print the debug information.
    if settings_dict.get('debug_mode', False) == True:
        # It's necessary to print the debug information.
        questions.PrintPlain('\n\nDebug information from textures.py:')
        questions.PrintDebug('texture_type', texture_type)
        questions.PrintDebug('max_texture_size', max_texture_size)
        questions.PrintDebug('textures_list', textures_list)
        questions.PrintDebug('settings_dict', settings_dict)
        questions.PrintPlain('\n\n')
    # Return the necessary information.
    return settings_dict, hex_out_list, texture_info_dict