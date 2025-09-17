# ########### #
# INFORMATION #
# ########### #
# This module is used to process PS2 assets.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import optimizations
# External modules
from os import remove


# ######### #
# FUNCTIONS #
# ######### #
# This function determines if it's okay to process PS2 assets.
def CanProcessPS2(settings_dict, texture_info_dict, game):
    # Initialize a variable to determine if it's okay to process (assume yes).
    can_process = True
    # Determine if the PS2 is in use.
    if settings_dict['PS2'] == False:
        # The PS2 is not in use.
        # Do not process.
        can_process = False
    else:
        # The PS2 is in use.
        # Determine if environment maps are in use.
        if ' Env' in texture_info_dict['texture_type']:
            # Environment maps are in use.
            # Set the environment map size.
            if game == 'MUA2':
                environment_size = 8
            else:
                environment_size = 16
            # Determine if the correct environment size is in use.
            if not(texture_info_dict['texture_type'].endswith(f' Env{environment_size}')):
                # The wrong environment map size is in use.
                # Skip processing.
                can_process = False
    # Determine if advanced textures are in use.
    if settings_dict['advanced_texture_ini'] is not None:
        # Advanced textures are in use.
        # Skip processing.
        can_process = False
    # Determine if this is MUA only.
    if ((settings_dict['PS2'] == 'MUA') and (game == 'XML2')):
        # This is for MUA only, but the game is XML2.
        # Skip processing.
        can_process = False
    # Return the status.
    return can_process

# This function determines how much to scale the asset.
def CheckPS2Scaling(settings_dict, asset_type, texture_info_dict, game):
    # Initialize the scale_factor as 1.0.
    scale_factor = 1.0
    # Determine if this is a big texture.
    if settings_dict['big_texture'] == False:
        # This is not a big texture.
        # Determine the max texture size.
        if asset_type in ['Conversation Portrait', 'Character Select Portrait', 'Power Icons']:
            max_size = 128
        elif asset_type in ['Comic Cover', 'Concept Art', 'Loading Screen']:
            max_size = 512
        else:
            max_size = 256
        # Determine if the texture is less than the max size.
        if texture_info_dict['max_texture_size'] > max_size:
            # The texture is bigger than the max size.
            # Update the scale factor.
            scale_factor = max_size / texture_info_dict['max_texture_size']
    # Determine if this is an asset that will be resized by being a secondary skin.
    if asset_type in ['Skin', 'Other']:
        # This is an asset that can be impacted by the secondary skin setting.
        # Check if this is a secondary skin.
        if settings_dict['secondary_skin'] == True:
            # This is a secondary skin.
            # Resize it.
            scale_factor *= 0.5
    # Determine if this is for MUA2.
    if game == 'MUA2':
        # This is for MUA2.
        # Determine if this is an asset that needs to be smaller in MUA2.
        if not(asset_type in ['Conversation Portrait', 'Character Select Portrait', 'Other']):
            # This is an asset that needs to be smaller in MUA2.
            # Update the scale factor.
            scale_factor *= 0.5
    # Return the scale factor.
    return scale_factor

# This function processes PS2 assets.
def ProcessPS2Asset(asset_type, temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
    # Get whether or not it's okay to process.
    can_process = CanProcessPS2(settings_dict, texture_info_dict, game)
    # Determine if it's okay to proces.
    if can_process == True:
        # It's okay to process.
        # Initialize a list of optimizations.
        optimization_list = []
        # For other models, add the collision generation if required.
        if ((asset_type == 'Other') and (settings_dict['generate_collision'] == True)):
            optimization_list.append('igCollideHullRaven')
        # Determine if the scale factor.
        scale_factor = CheckPS2Scaling(settings_dict, asset_type, texture_info_dict, game)
        # Add the necessary optimizations.
        optimization_list.extend(['igResizeImage', 'igQuantizeRaven'])
        # Add the conversion to PNG8 the default way, which will convert the environment maps.
        optimization_list.append('igConvertImage (PNG8)')
        # Write the optimization.
        optimizations.WriteOptimization(optimization_list, alchemy_version = 'Alchemy 3.2', scale_to = scale_factor)
        # Determine if the output sub-folder should be skipped.
        if settings_dict['skip_subfolder'] == False:
            # The sub-folder should not be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / f'for {game} (PS2)' / output_file_name
        else:
            # The sub-folder should be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / output_file_name
        # Determine if this is for MUA2.
        if game == 'MUA2':
            # This is for MUA2.
            # Set up a temp path for the Alchemy 3.2 optimized file.
            temp_file_hexed_32_path = temp_file_hexed_path.with_name('temph2.igb')
            # Perform the Alchemy 3.2 optimizations without sending the file.
            alchemy.CallAlchemy(temp_file_hexed_path, alchemy_version = 'Alchemy 3.2', output_path = temp_file_hexed_32_path)
            # Write a new optimization file for Alchemy 5.
            optimizations.WriteOptimization(['igConvertGeometryAttr'])
            # Perform the Alchemy 5 optimization.
            alchemy.CallAlchemy(temp_file_hexed_32_path, output_path = output_file_path)
            # Delete the other temp file.
            remove(temp_file_hexed_32_path)
        else:
            # This is for the other games.
            # Perform the Alchemy optimizations.
            alchemy.CallAlchemy(temp_file_hexed_path, alchemy_version = 'Alchemy 3.2', output_path = output_file_path)