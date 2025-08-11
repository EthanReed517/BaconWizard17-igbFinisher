# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import hex
import optimizations
import questions
import settings
# External modules
from os import environ, remove
from pathlib import Path
from shutil import copy


# ######### #
# FUNCTIONS #
# ######### #
# This function process MUA1 PC/Xbox 360 skins.
def ProcessPC360Skin(temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
    # Initialize a variable to determine if it's okay to process (assume yes).
    can_process = True
    # Initialize the output folder name (assume PC only).
    output_folder_name = f'for MUA1 (PC)'
    # Determine if there are environment maps.
    if ' Env' in texture_info_dict['texture_type']:
        # There are environment maps.
        # Don't process for either console.
        can_process = False
    else:
        # There are no environment maps.
        # Verify if the PC is in use.
        if settings_dict['PC'] == True:
            # The PC is in use.
            # Determine if the 360 is in use.
            if settings_dict['Xbox_360'] == True:
                # The 360 is in use.
                # Update the folder name.
                output_folder_name = 'for MUA1 (PC and 360)'
        else:
            # The PC is not in use.
            # Determine if the 360 is in use.
            if settings_dict['Xbox_360'] == True:
                # The 360 is in use.
                # Update the folder name.
                output_folder_name = 'for MUA1 (360)'
            else:
                # The 360 is not in use.
                # Skip processing.
                can_process = False
    # Determine if it's okay to process.
    if can_process == True:
        # It's okay to process.
        # Set up an output name for the Alchemy 3.2 optimized file.
        temp_file_hexed_32_path = temp_file_hexed_path.with_name('temph2.igb')
        # Initialize a list of optimizations.
        optimization_list = []
        ################################################################################################### NEED TO ADD ADVANCED TEXTURE SUPPORT HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Determine the texture size.
        if texture_info_dict['max_texture_size'] <= 256:
            # This is a small texture.
            # Initialize a list of Alchemy 3.2 optimizations.
            alchemy_32_optimization_list = []
            # Determine if the texture is opaque.
            if texture_info_dict['texture_type'].startswith('Opaque'):
                # This is an opaque texture.
                # Convert to PNG8.
                alchemy_32_optimization_list.append('igQuantizeRaven')
            else:
                # The texture is transparent.
                # Write the list of transparent textures.
                TransparentTextureNames(texture_info_dict['textures_list'])
                # Convert to PNG8, skipping transparent textures.
                alchemy_32_optimization_list.append('igQuantizeRaven (exclude)')
            # Write the Alchemy 3.2 optimization.
            optimizations.WriteOptimization(alchemy_32_optimization_list, alchemy_version = 'Alchemy 3.2')
            # Perform the Alchemy 3.2 optimizations and don't send the file.
            alchemy.CallAlchemy(temp_file_hexed_path, alchemy_version = 'Alchemy 3.2', output_path = temp_file_hexed_32_path)
        else:
            # This is a large texture.
            optimization_list.append('igConvertImage (DXT1)')
            copy(temp_file_hexed_path, temp_file_hexed_32_path)
        # Add the Alchemy 5 optimizations.
        optimization_list.extend(['igGenerateGlobalColor', 'igConvertGeometryAttr'])
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
        optimizations.WriteOptimization(optimization_list)
        # Perform the Alchemy 5 optimizations and send the file.
        alchemy.CallAlchemy(temp_file_hexed_32_path, output_path = output_file_path)
        # Delete the temp file.
        remove(temp_file_hexed_32_path)

# This function process MUA1 Steam/PS3 skins.
def ProcessPS3SteamSkin(temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
    # Initialize a variable to determine if it's okay to process (assume yes).
    can_process = True
    # Initialize the output folder name (assume Steam only).
    output_folder_name = f'for MUA1 (Steam)'
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
                # Update the folder name.
                output_folder_name = 'for MUA1 (Steam and PS3)'
        else:
            # The Steam version is not in use.
            # Determine if the PS3 is in use.
            if settings_dict['PS3'] == True:
                # The PS3 is in use.
                # Update the folder name.
                output_folder_name = 'for MUA1 (PS3)'
            else:
                # The PS3 is not in use.
                # Skip processing.
                can_process = False
    # Determine if it's okay to process.
    if can_process == True:
        # It's okay to process.
        # Initialize a list of optimizations.
        optimization_list = []
        ################################################################################################### NEED TO ADD ADVANCED TEXTURE SUPPORT HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Add the necessary optimizations.
        optimization_list.extend(['igConvertImage (DXT1)', 'igGenerateGlobalColor', 'igConvertGeometryAttr'])
        # Determine if the output sub-folder should be skipped.
        if settings_dict['skip_subfolder'] == False:
            # The sub-folder should not be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / output_folder_name / output_file_name
        else:
            # The sub-folder should be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / output_file_name
        # Write the Alchemy optimization.
        optimizations.WriteOptimization(optimization_list)
        # Perform the Alchemy 5 optimizations and send the file.
        alchemy.CallAlchemy(temp_file_hexed_path, output_path = output_file_path)

# This function process Wii skins.
def ProcessWiiSkin(temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
    # Initialize a variable to determine if it's okay to process (assume yes).
    can_process = True
    # Initialize the output folder name (assume one game only).
    output_folder_name = f'for {game} (Wii)'
    # Determine if the Wii is in use.
    if settings_dict['Wii'] == False:
        # The Wii is not in use.
        # Skip processing.
        can_process = False
    else:
        # The Wii is in use.
        # Determine if there are environment maps.
        if ' Env' in texture_info_dict['texture_type']:
            # Environment maps are in use.
            # Determine if the correct environment size is in use.
            if not(texture_info_dict['texture_type'].endswith(' Env32')):
                # The wrong environment map size is in use.
                # Skip processing.
                can_process = False
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
    # Determine if it's okay to process.
    if can_process == True:
        # It's okay to process.
        # Write the optimization.
        optimizations.WriteOptimization(['igConvertImage (DXT1)'], alchemy_version = 'Alchemy 3.2')
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