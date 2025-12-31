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
from datetime import datetime, timezone
from os import environ, remove, rename
from pathlib import Path


# ######### #
# FUNCTIONS #
# ######### #
# This function determines if it's okay to process Xbox/XML2 PC assets.
def CanProcessXbox(game, settings_dict, texture_info_dict):
    # Initialize a variable to determine if it's okay to process (assume yes).
    can_process = True
    # Initialize the output folder name (assume Xbox only).
    output_folder_list = [f'for {game} (Xbox)']
    # Determine which game this is for.
    if game == 'XML2':
        # This is for XML2.
        # Determine if there are environment maps.
        if ' Env' in texture_info_dict['texture_type']:
            # There are environment maps.
            # Determine what size these are.
            if texture_info_dict['texture_type'].endswith(' Env128'):
                # This is the PC size.
                # Determine if the PC is in use.
                if settings_dict['PC'] == True:
                    # The PC is in use.
                    # Set the output folder name.
                    output_folder_list = ['for XML2 (PC)']
                else:
                    # The PC is not in use.
                    # Skip processing.
                    can_process = False
            elif texture_info_dict['texture_type'].endswith(' Env32'):
                # This is the Xbox size.
                # Determine if the Xbox is in use.
                if settings_dict['Xbox'] == False:
                    # The Xbox is not in use.
                    # Processing is not needed here.
                    can_process = False
            else:
                # These are some other size.
                # Don't process for Xbox.
                can_process = False
        else:
            # There are no environment maps.
            # Verify if the PC is in use.
            if settings_dict['PC'] == True:
                # The PC is in use.
                # Determine if the Xbox is in use.
                if settings_dict['Xbox'] == True:
                    # The Xbox is in use.
                    # Determine if advanced texture folders are being forced.
                    if settings_dict['force_adv_tex_folders'] == True:
                        # Advanced texture folders are being forced.
                        # Set up the folder names.
                        output_folder_list = ['for XML2 (PC)', 'for XML2 (Xbox)']
                    else:
                        # Advanced texture folders are not being forced.
                        # Update the folder name.
                        output_folder_list = ['for XML2 (PC and Xbox)']
                else:
                    # The Xbox is not in use.
                    # Update the folder name.
                    output_folder_list = ['for XML2 (PC)']
            else:
                # The PC is not in use.
                # Determine if the Xbox is in use.
                if ((settings_dict['Xbox'] == False) or (settings_dict['Xbox'] == 'MUA1')):
                    # The xbox is not in use.
                    # Skip processing.
                    can_process = False
    else:
        # This is for XML1 or MUA1.
        # Determine if there are environment maps.
        if ' Env' in texture_info_dict['texture_type']:
            # There are environment maps.
            # Determine what size these are.
            if not(texture_info_dict['texture_type'].endswith(' Env32')):
                # This is not the Xbox size.
                # Skip processing.
                can_process = False
        # Determine if the Xbox is in use.
        if settings_dict['Xbox'] == False:
            # The Xbox is not in use.
            # Skip processing.
            can_process = False
    # Determine if advanced textures are in use.
    if settings_dict['advanced_texture_ini'] is not None:
        # Advanced textures are in use.
        # Skip processing.
        can_process = False
    # Return whether or not it's okay to process as well as the list of output folders.
    return can_process, output_folder_list

# This function checks if Xbox assets need to be scaled.
def CheckXboxScaling(asset_type, game, optimization_list, output_folder_list, max_texture_size):
    # Set up a scale factor. Assume 1.
    scale_factor = 1.0
    # Determine if this is for XML2 PC only.
    if not(output_folder_list == ['for XML2 (PC)']):
        # This is not for XML2 PC only, so scaling may be needed.
        # Determine if this is an asset type that needs scaling.
        if asset_type in ['Comic Cover', 'Concept Art', 'Loading Screen']:
            # This is an asset type that needs scaling.
            # Check if the max size is exceeded.
            if max_texture_size > 1024:
                # The max texture size is exceeded.
                # Update the scale factor.
                scale_factor = 1024 / max_texture_size
                # Add the resizing optimization to the optimization list.
                optimization_list.append('igResizeImage')
                # Determine if this is for XML2 PC and Xbox.
                if output_folder_list == ['for XML2 (PC and Xbox)']:
                    # This is for PC and Xbox.
                    # Update the list to separate them.
                    output_folder_list = ['for XML2 (Xbox)', 'for XML2 (PC)']
                elif output_folder_list ['for XML2 (PC)', 'for XML2 (Xbox)']:
                    # PC and Xbox are already separated.
                    # Rearrange the order.
                    output_folder_list = ['for XML2 (Xbox)', 'for XML2 (PC)']
    # Return the updated lists.
    return optimization_list, output_folder_list, scale_factor

# This function determines the cutoff size for PNG8 vs DXT1.
def GetXboxMaxPNG8Size(asset_type):
    # Set the max size based on the asset type.
    if asset_type in ['Conversation Portrait', 'Character Select Portrait']:
        max_png8_size = 128
    elif asset_type in ['Comic Cover', 'Concept Art', 'Loading Screen']:
        max_png8_size = 0
    else:
        max_png8_size = 256
    # Return the max size.
    return max_png8_size

# This function process Xbox and XML2 PC Assets.
def ProcessXboxAsset(asset_type, temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
    # Check if processing is allowed.
    can_process, output_folder_list = CanProcessXbox(game, settings_dict, texture_info_dict)
    # Determine if it's okay to process.
    if can_process == True:
        # It's okay to process.
        # Initialize a list of optimizations.
        optimization_list = []
        # For other models, add the collision generation if required.
        if ((asset_type == 'Other') and (settings_dict['generate_collision'] == True)):
            optimization_list.append('igCollideHullRaven')
        # Determine if scaling is necessary.
        optimization_list, output_folder_list, scale_factor = CheckXboxScaling(asset_type, game, optimization_list, output_folder_list, texture_info_dict['max_texture_size'])
        # Determine the max size for PNG8 textures.
        max_png8_size = GetXboxMaxPNG8Size(asset_type)
        # Determine the texture size.
        if texture_info_dict['max_texture_size'] > max_png8_size:
            # This is a large texture.
            # Convert to DXT1 (automatically preserves transparent textures but will convert environment maps).
            optimization_list.append('igConvertImage (DXT1)')
        else:
            # This is a small texture.
            # Determine if the texture is opaque.
            if texture_info_dict['texture_type'].startswith('Opaque'):
                # This is an opaque texture.
                # Convert to PNG8.
                optimization_list.append('igQuantizeRaven')
            else:
                # The texture is transparent.
                # Write the list of transparent textures.
                processing.TransparentTextureNames(texture_info_dict['textures_list'])
                # Convert to PNG8, skipping transparent textures.
                optimization_list.append('igQuantizeRaven (exclude)')
            # Determine if there are environment maps.
            if ' Env' in texture_info_dict['texture_type']:
                # There are environment maps.
                # Add the conversion to PNG8 the default way, which will convert the environment maps. Also preserves transparent textures.
                optimization_list.append('igConvertImage (PNG8) (exclude)')
        # Loop through the output folder list.
        for output_folder_name in output_folder_list:
            # Determine if the output sub-folder should be skipped.
            if settings_dict['skip_subfolder'] == False:
                # The sub-folder should not be skipped.
                # Set up the destination path.
                output_file_path = settings_dict[f'{game}_path'] / output_folder_name / output_file_name
            else:
                # The sub-folder should be skipped.
                # Set up the destination path.
                output_file_path = settings_dict[f'{game}_path'] / output_file_name
            # Determine if this is for PC after an Xbox asset that was scaled.
            if ((output_folder_list == ['for XML2 (Xbox)', 'for XML2 (PC)']) and (output_folder_name == 'for XML2 (PC)')):
                # This is for the PC after an Xbox asset was scaled.
                # Remove the scaling optimization.
                optimization_list.remove('igResizeImage')
            # Write the optimization.
            optimizations.WriteOptimization(optimization_list, alchemy_version = 'Alchemy 3.2', scale_to = scale_factor)
            # Perform the Alchemy optimizations.
            alchemy.CallAlchemy(temp_file_hexed_path, alchemy_version = 'Alchemy 3.2', output_path = output_file_path, debug_mode = settings_dict.get('debug_mode', False), console = output_folder_name)
        # Determine if the text file exists.
        if (Path(environ['temp']) / 'temp.txt').exists():
            # The text file exists.
            # Determine if debug mode is on.
            if settings_dict.get('debug_mode', False) == True:
                # Debug mode is on.
                # Rename the text file.
                rename((Path(environ['temp']) / 'temp.txt'), (Path(environ['temp']) / f'temp - {output_folder_name} - Alchemy 3.2 - {str(datetime.now(timezone.utc)).replace(':', '-')}.txt'))
            else:
                # Debug mode is off.
                # Remove the text file.
                remove(Path(environ['temp']) / 'temp.txt')