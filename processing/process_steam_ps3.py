# ########### #
# INFORMATION #
# ########### #
# This module is used to process Xbox assets.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import hex
import optimizations
import processing
# External modules
from os import makedirs, remove
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
                # Determine if advanced texture folders are being forced or if advanced textures are being used.
                if ((settings_dict['force_adv_tex_folders'] == True) or (settings_dict['advanced_texture_ini'] is not None)):
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
        if ((asset_type == 'Other') and (settings_dict['generate_collision'] == True)):
            alchemy_32_optimization_list.append('igCollideHullRaven')
        # Determine if scaling is necessary.
        alchemy_32_optimization_list, output_folder_list, scale_factor = CheckPS3Scaling(asset_type, game, alchemy_32_optimization_list, output_folder_list, texture_info_dict['max_texture_size'])
        # Determine if an advanced texture is necessary.
        if settings_dict['advanced_texture_ini'] is not None:
            # Advanced textures are necessary.
            # Add the optimizations.
            alchemy_5_optimization_list.extend(['igRavenSetupMUAMaterial', 'igConvertImage (DXT1)', 'igConvertImage (DXT5)'])
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
                optimizations.WriteOptimization(alchemy_32_optimization_list, alchemy_version = 'Alchemy 3.2', scale_to = scale_factor)
                # Perform the Alchemy 3.2 optimizations and don't send the file.
                alchemy.CallAlchemy(temp_file_hexed_path, alchemy_version = 'Alchemy 3.2', output_path = temp_file_hexed_32_path)
            else:
                # There are no Alchemy 3.2 optimizations.
                # Create a copy of the file with the Alchemy 3.2 name.
                copy(temp_file_hexed_path, temp_file_hexed_32_path)
            # Add the conversion to DXT1.
            alchemy_5_optimization_list.append('igConvertImage (DXT1)')
            # Add the global color optimization for skins only.
            if ((asset_type == 'Skin') and not('igGenerateGlobalColor' in alchemy_5_optimization_list)):
                alchemy_5_optimization_list.append('igGenerateGlobalColor')
            # Add the mandatory Alchemy 5 optimization.
            if not('igConvertGeometryAttr' in alchemy_5_optimization_list):
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
            # Determine if there are advanced textures.
            if settings_dict['advanced_texture_ini'] is not None:
                # There are advanced textures.
                # Check which console this is for.
                if output_folder_name == 'for MUA1 (PS3)':
                    # This is for PS3.
                    # Write the optimization with green normal maps.
                    optimizations.WriteOptimization(alchemy_5_optimization_list, advanced_texture_ini = settings_dict['advanced_texture_ini'], normal_map_type = 'green')
                    normal_map_suffix = '_n_g.png'
                else:
                    # This is for the Steam version.
                    # Write the optimization with blue normal maps.
                    optimizations.WriteOptimization(alchemy_5_optimization_list, advanced_texture_ini = settings_dict['advanced_texture_ini'], normal_map_type = 'blue')
                    normal_map_suffix = '_n_b.png'
                # Perform the Alchemy 5 optimizations but don't send the file.
                alchemy.CallAlchemy(temp_file_hexed_32_path)
                # Make the destination folder.
                makedirs(output_file_path.parent, exist_ok = True)
                # Hex edit the extension of the normal map and send it out.
                hex.HexEditor(temp_file_hexed_32_path, output_file_path, [[bytearray(normal_map_suffix, 'utf-8'), bytearray('_n.png', 'utf-8')]])
            else:
                # There are no advanced textures.
                # Write the Alchemy 5 optimization normally.
                optimizations.WriteOptimization(alchemy_5_optimization_list)
                # Perform the Alchemy 5 optimizations and send the file.
                alchemy.CallAlchemy(temp_file_hexed_32_path, output_path = output_file_path)
            # Delete the temp file.
            remove(temp_file_hexed_32_path)