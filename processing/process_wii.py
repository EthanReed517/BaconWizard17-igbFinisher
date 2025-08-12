# ########### #
# INFORMATION #
# ########### #
# This module is used to process GameCube assets.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import optimizations
# External modules
from os import environ, remove
from pathlib import Path


# ######### #
# FUNCTIONS #
# ######### #
# This function determines if it's okay to process Wii assets.
def CanProcessWii(settings_dict, texture_info_dict, game, output_file_name):
    # Initialize a variable to determine if it's okay to process (assume yes).
    can_process = True
    # Initialize the output folder name (assume one game only).
    output_folder_name = f'for {game} (Wii)'
    # Determine if the Wii is in use.
    if settings_dict['Wii'] == False:
        # The Wii is not in use.
        # Do not process.
        can_process = False
    else:
        # The Wii is in use.
        # Determine if environment maps are in use.
        if ' Env' in texture_info_dict['texture_type']:
            # Environment maps are in use.
            # Determine if the correct environment size is in use.
            if not(texture_info_dict['texture_type'].endswith(' Env32')):
                # The wrong environment map size is in use.
                # Skip processing.
                can_process = False
        # This is for MUA1 or MUA2.
        # Determine if the MUA1 and MUA2 information is the same.
        if ((settings_dict['MUA1_num'] == settings_dict['MUA2_num']) and (settings_dict['MUA1_path'] == settings_dict['MUA2_path'])):
            # The MUA1 and MUA2 information is the same.
            # Determine which game this is for.
            if game == 'MUA1':
                # This is for MUA1.
                # Update the output folder name.
                output_folder_name = 'for MUA1 (Wii) and MUA2 (Wii)'
            else:
                # This is for MUA2.
                # Skip processing, as processing was already handled for MUA1.
                can_process = False
    # Return if this can be processed as well as the output folder.
    return can_process, output_folder_name

# This function determines how much to scale the asset.
def CheckWiiScaling(settings_dict, asset_type, texture_info_dict, optimizations_list):
    # Initialize the scale_factor as 1.0.
    scale_factor = 1.0
    # Determine if this is a big texture.
    if settings_dict['big_texture'] == False:
        # This is not a big texture.
        # Determine if this is an asset type that has a max size.
        if asset_type in ['Comic Cover', 'Concept Art', 'Loading Screen']:
            # This is an asset that has a max size.
            # Determine if the texture is less than the max size.
            if texture_info_dict['max_texture_size'] > 1024:
                # The texture is bigger than the max size.
                # Update the scale factor.
                scale_factor = 1024 / texture_info_dict['max_texture_size']
                # Add the scaling optimization.
                optimizations_list.append('igResizeImage')
    # Return the scale factor.
    return scale_factor, optimizations_list

# This function process Wii assets.
def ProcessWiiAsset(asset_type, temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
    # Get the processing status.
    can_process, output_folder_name = CanProcessWii(settings_dict, texture_info_dict, game, output_file_name)
    # Determine if it's okay to process.
    if can_process == True:
        # It's okay to process.
        # Initialize a list of optimizations.
        optimizations_list = []
        # For other models, add the collision generation if required.
        if ((asset_type == 'Other') and (settings['generate_collision'] == True)):
            optimization_list.append('igCollideHullRaven')
        # Check if the asset needs to be scaled.
        scale_factor, optimizations_list = CheckWiiScaling(settings_dict, asset_type, texture_info_dict, optimizations_list)
        # Add the conversion to DXT1.
        optimizations_list.append('igConvertImage (DXT1)')
        # Write the optimization.
        optimizations.WriteOptimization(optimizations_list, alchemy_version = 'Alchemy 3.2', scale_to = scale_factor)
        # Determine if the output sub-folder should be skipped.
        if settings_dict['skip_subfolder'] == False:
            # The sub-folder should not be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / output_folder_name / output_file_name
        else:
            # The sub-folder should be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / output_file_name
        # Perform the Alchemy optimizations.
        alchemy.CallAlchemy(temp_file_hexed_path, alchemy_version = 'Alchemy 3.2', output_path = output_file_path)