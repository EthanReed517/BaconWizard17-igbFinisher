# ########### #
# INFORMATION #
# ########### #
# This module is used to recognize information about the model's textures.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import basic_xml_ops
import questions
import settings
# External modules
from natsort import os_sorted
from pathlib import Path


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
            elif texture_dict['Format'] == 'IG_GFX_TEXTURE_FORMAT_RGBA_8888_32 (7)':
                # This is a transparent texture.
                # Set the type to transparent.
                texture_type = 'Transparent'
            else:
                # This is some other texture type, which is not supported.
                # Print an error.
                questions.PrintError(f'Texture {texture_dict['Name']} uses format {texture_dict['Format']}, which is not supported. The supported texture formats are IG_GFX_TEXTURE_FORMAT_RGB_888_24 (5) (for opaque textures) or IG_GFX_TEXTURE_FORMAT_RGBA_8888_32 (7) (for textures with transparency).', system_exit = True)
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
                questions.PrintError(f'The output path for {game} is set up for folder detection in the settings, but the model has no textures available for detection.', system_exit = True)
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
                questions.PrintWarning(f'The output path for {game} is set up for folder detection in the settings, but the model uses multiple texture folders.', skip_pause = True)
                # Can't use windows path types for this; start a list that will hold them as strings.
                texture_folders_list_str = []
                # Loop through the texture folders.
                for texture_folder in texture_folders_list:
                    # Add the folder as a string.
                    texture_folders_list_str.append(str(texture_folder))
                # Give the option to pick a folder for selection.
                texture_folder_choice = Path(questions.Select('Select which texture folder to use for detection.', os_sorted(texture_folders_list_str)))
            else:
                # Only 1 folder was found.
                # Default to this folder.
                texture_folder_choice = texture_folders_list[0]
            # Get the character and sub-folder from the texture folder.
            character = texture_folder_choice.parts[-3]
            asset_type_folder = texture_folder_choice.parts[-2]
            sub_folder = texture_folder_choice.parts[-1]
            # Determine if detection is needed for this game.
            if settings_dict[f'{game}_path'] == 'Detect':
                # It's necessary to detect for this game.
                # Get the path.
                settings_dict[f'{game}_path'] = basic_xml_ops.GetOutputPath(game, application_path, character, asset_type_folder, sub_folder, asset_type, settings_dict)
    # Return the updated settings file.
    return settings_dict

# This function is used to set the list of hex editing values and also get the output file names for 2D assets.
def GetHexOutList(settings_dict, asset_type, textures_list):
    # Initialize a list of things to hex out.
    hex_out_list = []
    # Verify that this is a 2D asset that gets its file name from the texture name.
    if asset_type in ['Conversation Portrait', 'Character Select Portrait', 'Power Icons', 'Comic Cover', 'Concept Art', 'Loading Screen']:
        # This is a 2D asset that gets its file name from the texture name.
        # Get the texture name.
        texture_name = textures_list[0].stem
        # Filter by asset type.
        if asset_type in ['Conversation Portrait', 'Character Select Portrait']:
            # This is a portrait.
            # Set up a dictionary to match the prefixes to descriptors.
            descriptor_dict = {'b': 'Hero', 'g': 'Villain - Green Outline', 'r': 'Villain', 'ng': 'Next-Gen Style', 'x1c': 'XML1', 'x2c': 'XML2'}
            # Loop through the possible prefixes.
            for prefix in descriptor_dict.keys():
                # Determine if the texture starts with one of these prefixes.
                if texture_name.startswith(f'{prefix}_'):
                    # The texture starts with this prefix.
                    # Update the hex editing list to remove this.
                    hex_out_list.append([texture_name, texture_name[(len(prefix) + 1):]])
                    # Loop through the games.
                    for game in settings.games_list:
                        # Make sure that the special name should be set.
                        if settings_dict[f'{game}_special_name'] is None:
                            # The special name should be set.
                            # Update the name for that game.
                            settings_dict[f'{game}_special_name'] = descriptor_dict[prefix]
                    # Determine if this is a CSP.
                    if asset_type == 'Character Select Portrait':
                        # This is a CSP.
                        # Set up a dictionary of games to skip.
                        game_to_skip_dict = {'x1c': 'XML2', 'x2c': 'XML1'}
                        # Skip the necessary game.
                        settings_dict[f'{game_to_skip_dict[prefix]}_num'] = None
                        settings_dict[f'{game_to_skip_dict[prefix]}_path'] = None
        elif asset_type == 'Power Icons':
            # This is power icons.
            # Determine what game this is for.
            texture_prefix = texture_name.split('_')[0]
            # Loop through the games.
            for game in settings.games_list:
                # Determine if this matches the game.
                if game == texture_prefix:
                    # The games match.
                    # Make sure that the special name should be set.
                    if settings_dict[f'{game}_special_name'] is None:
                        # The special name should be set.
                        # Update the settings accordingly.
                        settings_dict[f'{game}_special_name'] = texture_name
                        hex_out_list.append([texture_name, texture_name[5:]])
                        # Determine if this is an icons file.
                        if asset_type == 'Power Icons':
                            # This is an icons file.
                            # Determine if this is an icons2 file.
                            if 'icons2' in texture_name:
                                # This is an icons2 file.
                                # Skip the consoles that don't use icons2.
                                settings_dict['GameCube'] = False
                                settings_dict['PS2'] = False
                                settings_dict['PSP'] = False
                else:
                    # This is another game.
                    # Update the settings accordingly.
                    settings_dict[f'{game}_num'] = None
                    settings_dict[f'{game}_path'] = None
        elif asset_type == 'Comic Cover':
            # This is a comic cover.
            # Determine which game this is for.
            texture_prefix = texture_name.split('_')[0]
            # Determine the game.
            if texture_prefix == 'XML1':
                # This is for XML1.
                # Disable the other games.
                settings_dict['XML2_num'] = None
                settings_dict['XML2_path'] = None
                settings_dict['MUA1_num'] = None
                settings_dict['MUA1_path'] = None
            elif texture_prefix == 'XML2':
                # This is for XML2 (except for PSP).
                # Disable the other games and the PSP.
                settings_dict['XML1_num'] = None
                settings_dict['XML1_path'] = None
                settings_dict['MUA1_num'] = None
                settings_dict['MUA1_path'] = None
                settings_dict['PSP'] = False
            elif texture_prefix == 'XML2-PSP':
                # This is for XML2 PSP.
                # Disable the other games and consoles.
                settings_dict['XML1_num'] = None
                settings_dict['XML1_path'] = None
                settings_dict['MUA1_num'] = None
                settings_dict['MUA1_path'] = None
                settings_dict['GameCube'] = False
                settings_dict['PS2'] = False
                settings_dict['PC'] = False
                settings_dict['Xbox'] = False
            elif texture_prefix == 'MUA1-LG':
                # This is for last-gen MUA1.
                # Disable the other games and consoles.
                settings_dict['XML1_num'] = None
                settings_dict['XML1_path'] = None
                settings_dict['XML2_num'] = None
                settings_dict['XML2_path'] = None
                settings_dict['PC'] = False
                settings_dict['Steam'] = False
                settings_dict['PS3'] = False
                settings_dict['Xbox_360'] = False
            else:
                # This is for next-gen MUA1.
                # Disable the other games and consoles.
                settings_dict['XML1_num'] = None
                settings_dict['XML1_path'] = None
                settings_dict['XML2_num'] = None
                settings_dict['XML2_path'] = None
                settings_dict['PS2'] = False
                settings_dict['PSP'] = False
                settings_dict['Wii'] = False
                settings_dict['Xbox'] = False
            # Always disable MUA2 because it doesn't use comic covers.
            settings_dict['MUA2_num'] = None
            settings_dict['MUA2_path'] = None
        else:
            # This is an asset that has game-specific aspect ratios.
            # Get the suffix from the file name.
            suffix = texture_name.split('_')[-1]
            # Check what the suffix is.
            if suffix == '4-3':
                # This is a 4:3 texture.
                # Skip processing for PSP, MUA1, and MUA2.
                settings_dict['PSP'] = False
                settings_dict['MUA1_num'] = None
                settings_dict['MUA2_num'] = None
                settings_dict['MUA1_path'] = None
                settings_dict['MUA2_path'] = None
            elif suffix == '16-9-P':
                # This is a 16:9 XML2 PSP loading screen texture.
                # Skip processing for all games except for XML2.
                settings_dict['XML1_num'] = None
                settings_dict['XML1_path'] = None
                settings_dict['MUA1_num'] = None
                settings_dict['MUA1_path'] = None
                settings_dict['MUA2_num'] = None
                settings_dict['MUA2_path'] = None
                # Skip processing for non-PSP consoles.
                settings_dict['GameCube'] = False
                settings_dict['PS2'] = False
                settings_dict['PC'] = False
                settings_dict['Xbox'] = False
            elif suffix == '16-9-N':
                # This is a 16-9 next-gen texture.
                # Skip processing for all games except for MUA1.
                settings_dict['XML1_num'] = None
                settings_dict['XML1_path'] = None
                settings_dict['XML2_num'] = None
                settings_dict['XML2_path'] = None
                settings_dict['MUA2_num'] = None
                settings_dict['MUA2_path'] = None
                # Skip processing for last-gen consoles.
                settings_dict['PS2'] = False
                settings_dict['PSP'] = False
                settings_dict['Wii'] = False
                settings_dict['Xbox'] = False
            elif suffix == '16-9-L':
                # This is a last-gen texture.
                # Skip processing for XML1.
                settings_dict['XML1_num'] = None
                settings_dict['XML1_path'] = None
                # Determine the asset type.
                if asset_type == 'Loading Screen':
                    # This is a loading screen.
                    # Skip processing for all of XML2.
                    settings_dict['XML2_num'] = None
                    settings_dict['XML2_path'] = None
                else:
                    # This is concept art.
                    # Skip processing for non-PSP XML2 consoles.
                    settings_dict['GameCube'] = False
                    settings_dict['PS2'] = 'MUA'
                    settings_dict['PC'] = False
                    settings_dict['Xbox'] = 'MUA1'
                # Skip processing for next-gen consoles.
                settings_dict['PC'] = False
                settings_dict['Steam'] = False
                settings_dict['PS3'] = False
                settings_dict['Xbox_360'] = False
            # Determine if this is concept art.
            if asset_type == 'Concept Art':
                # This is concept art.
                # Skip processing for MUA2.
                settings_dict['MUA2_num'] = None
                settings_dict['MUA2_path'] = None
                # Loop through the games.
                for game in settings.games_list:
                    # Make sure that the special name should be set.
                    if settings_dict[f'{game}_special_name'] is None:
                        # The special name should be set.
                        # Update the settings accordingly.
                        settings_dict[f'{game}_special_name'] = texture_name
                # Add the hex editing information.
                hex_out_list.append([texture_name, ('_').join(texture_name.split('_')[1:])])
            else:
                # This is a loading screen.
                # Determine if this is a villain loading screen.
                if texture_name.split('_')[1] == 'v':
                    # This is a villain loading screen.
                    # Loop through the games.
                    for game in settings.games_list:
                        # Make sure that the special name should be set.
                        if settings_dict[f'{game}_special_name'] is None:
                            # The special name should be set.
                            # Update the settings accordingly.
                            settings_dict[f'{game}_special_name'] = 'Villain'
                    # Add the hex editing information
                    hex_out_list.append([texture_name, ('_').join(texture_name.split('_')[2:])])
                else:
                    # This is a standard loading screen.
                    # Add the hex editing information
                    hex_out_list.append([texture_name, ('_').join(texture_name.split('_')[1:])])
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
    settings_dict, hex_out_list = GetHexOutList(settings_dict, asset_type, textures_list)
    # Determine the environment map type from the texture information.
    settings_dict, hex_out_list, texture_type = GetEnvironmentType(textures_list, settings_dict, asset_type, hex_out_list, input_file_path, texture_type)
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