# ########### #
# INFORMATION #
# ########### #
# This module is used to process Xbox assets.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import optimizations
import processing
# External modules
from os import remove
from shutil import copy


# ######### #
# FUNCTIONS #
# ######### #
# This function determines if it's okay to process MUA1 Steam/PS3 assets.
def CanProcessSteamPS3(settings_dict, texture_info_dict):
    # Initialize a variable to determine if it's okay to process (assume yes).
    can_process = True
    # Initialize the output folder name (assume PS3 only).
    output_folder_list = [f'for MUA1 (PS3)']
    # Determine if there are environment maps.
    if ' Env' in texture_info_dict['texture_type']:
        # There are environment maps.
        # Don't process for either console.
        can_process = False
    else:
        # There are no environment maps.
        # Verify if the Steam version is in use.
        if settings_dict['Steam'] == True:
            # The Steam version is in use.
            # Determine if the PS3 is in use.
            if settings_dict['PS3'] == True:
                # The PS3 is in use.
                # Determine if advanced texture folders are being forced.
                if settings_dict['force_adv_tex_folders'] == True:
                    # Advanced texture folders are being forced.
                    # Set up the folder names.
                    output_folder_list = ['for MUA1 (Steam)', 'for MUA1 (PS3)']
                else:
                    # Advanced texture folders are not being forced.
                    # Update the folder name.
                    output_folder_list = ['for MUA1 (Steam and PS3)']
            else:
                # The PS3 is not in use.
                # Update the folder name.
                output_folder_list = ['for MUA1 (Steam)']
        else:
            # The Steam version is not in use.
            # Determine if the PS3 is in use.
            if settings_dict['PS3'] == False:
                # The PS3 is not in use.
                # Skip processing.
                can_process = False
    # Return whether or not it's okay to process as well as the list of output folders.
    return can_process, output_folder_list

# This function checks if PS3 assets need to be scaled.
def CheckPS3Scaling(asset_type, game, alchemy_32_optimization_list, output_folder_list, max_texture_size):
    # Set up a scale factor. Assume 1.
    scale_factor = 1.0
    # Determine if this is for MUA1 Steam only.
    if not(output_folder_list == ['for MUA1 (Steam)']):
        # This is not for MUA1 Steam only, so scaling may be needed.
        # Determine if this is an asset type that needs scaling.
        if asset_type in ['Comic Cover', 'Concept Art', 'Loading Screen']:
            # This is an asset type that needs scaling.
            # Check if the max size is exceeded.
            if max_texture_size > 2048:
                # The max texture size is exceeded.
                # Update the scale factor.
                scale_factor = 2048 / max_texture_size
                # Add the resizing optimization to the optimization list.
                alchemy_32_optimization_list.append('igResizeImage')
                # Determine if this is for MUA1 Steam and PS3.
                if output_folder_list == ['for MUA1 (Steam and PS3)']:
                    # This is for Steam and PS3.
                    # Update the list to separate them.
                    output_folder_list = ['for MUA1 (PS3)', 'for MUA1 (Steam)']
                elif output_folder_list ['for MUA1 (Steam)', 'for MUA1 (Xbox)']:
                    # Steam and PS3 are already separated.
                    # Rearrange the order.
                    output_folder_list = ['for MUA1 (PS3)', 'for MUA1 (Steam)']
    # Return the updated lists.
    return alchemy_32_optimization_list, output_folder_list, scale_factor

# This function process MUA1 Steam/PS3 assets.
def ProcessSteamPS3Asset(asset_type, temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
    # Get the processing status and list of output folders.
    can_process, output_folder_list = CanProcessSteamPS3(settings_dict, texture_info_dict)
    # Determine if it's okay to process.
    if can_process == True:
        # It's okay to process.
        # Set up an output name for the Alchemy 3.2 optimized file.
        temp_file_hexed_32_path = temp_file_hexed_path.with_name('temph2.igb')
        # Initialize a list of optimizations.
        alchemy_32_optimization_list = []
        alchemy_5_optimization_list = []
        # For other models, add the collision generation if required.
        if ((asset_type == 'Other') and (settings['generate_collision'] == True)):
            alchemy_32_optimization_list.append('igCollideHullRaven')
        # Determine if scaling is necessary.
        alchemy_32_optimization_list, output_folder_list, scale_factor = CheckPS3Scaling(asset_type, game, alchemy_32_optimization_list, output_folder_list, texture_info_dict['max_texture_size'])
        ################################################################################################### NEED TO ADD ADVANCED TEXTURE SUPPORT HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ### Advanced textures get converted to the necessary texture format, except need to make sure that normal maps are converted to DXT5 no matter what.
        # Loop through the output folders.
        for output_folder_name in output_folder_list:
            # Determine if this is for Steam after a PS3 asset that was scaled.
            if ((output_folder_list == ['for MUA1 (PS3)', 'for MUA1 (Steam)']) and (output_folder_name == 'for MUA1 (Steam)')):
                # This is for the Steam after a PS3 asset was scaled.
                # Remove the scaling optimization.
                alchemy_32_optimization_list.remove('igResizeImage')
            # Determine if there are any Alchemy 3.2 optimizations.
            if not(alchemy_32_optimization_list == []):
                # There are Alchemy 3.2 optimizations.
                # Write the Alchemy 3.2 optimization.
                optimizations.WriteOptimization(alchemy_32_optimization_list, alchemy_version = 'Alchemy 3.2')
                # Perform the Alchemy 3.2 optimizations and don't send the file.
                alchemy.CallAlchemy(temp_file_hexed_path, alchemy_version = 'Alchemy 3.2', output_path = temp_file_hexed_32_path)
            else:
                # There are no Alchemy 3.2 optimizations.
                # Create a copy of the file with the Alchemy 3.2 name.
                copy(temp_file_hexed_path, temp_file_hexed_32_path)
            # Add the conversion to DXT1.
            alchemy_5_optimization_list.append('igConvertImage (DXT1)')
            # Add the global color optimization for skins only.
            if asset_type == 'Skin':
                alchemy_5_optimization_list.append('igGenerateGlobalColor')
            # Add the mandatory Alchemy 5 optimization.
            alchemy_5_optimization_list.append('igConvertGeometryAttr')
            # Determine if the output sub-folder should be skipped.
            if settings_dict['skip_subfolder'] == False:
                # The sub-folder should not be skipped.
                # Set up the destination path.
                output_file_path = settings_dict[f'{game}_path'] / output_folder_name / output_file_name
            else:
                # The sub-folder should be skipped.
                # Set up the destination path.
                output_file_path = settings_dict[f'{game}_path'] / output_file_name
            # Write the Alchemy 5 optimization.
            optimizations.WriteOptimization(alchemy_5_optimization_list)
            # Perform the Alchemy 5 optimizations and send the file.
            alchemy.CallAlchemy(temp_file_hexed_32_path, output_path = output_file_path)
            # Delete the temp file.
            remove(temp_file_hexed_32_path)