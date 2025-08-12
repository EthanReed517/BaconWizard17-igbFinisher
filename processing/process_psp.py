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
# This function determines if it's okay to process PSP assets.
def CanProcessPSP(settings_dict, texture_info_dict, game, has_cel, output_file_name):
    # Initialize a variable to determine if it's okay to process (assume yes).
    can_process = True
    # Initialize the output folder name (assume one game only).
    output_folder_name = f'for {game} (PSP)'
    # Determine if the PSP is in use.
    if settings_dict['PSP'] == False:
        # The PSP is not in use.
        # Do not process.
        can_process = False
    else:
        # The PSP is in use.
        # Determine if environment maps are in use.
        if ' Env' in texture_info_dict['texture_type']:
            # Environment maps are in use.
            # Determine if the correct environment size is in use.
            if not(texture_info_dict['texture_type'].endswith(' Env8')):
                # The wrong environment map size is in use.
                # Skip processing.
                can_process = False
        # Determine if this is for XML2.
        if game == 'XML2':
            # This is for XML2.
            # Determine if the skin has cel shading.
            if has_cel == True:
                # The skin has cel shading.
                # Can't proces it.
                can_process = False
            else:
                # The skin doesn't have cel shading.
                # Determine if there's a no cel descriptor in the file name.
                if ' - No Cel' in output_file_name:
                    # There's a no cel descriptor.
                    # Remove it.
                    output_file_name = output_file_name.replace(' - No Cel', '')
        else:
            # This is for MUA1 or MUA2.
            # Determine if the MUA1 and MUA2 information is the same.
            if ((settings_dict['MUA1_num'] == settings_dict['MUA2_num']) and (settings_dict['MUA1_path'] == settings_dict['MUA2_path'])):
                # The MUA1 and MUA2 information is the same.
                # Determine which game this is for.
                if game == 'MUA1':
                    # This is for MUA1.
                    # Update the output folder name.
                    output_folder_name = 'for MUA1 (PSP) and MUA2 (PSP)'
                else:
                    # This is for MUA2.
                    # Skip processing, as processing was already handled for MUA1.
                    can_process = False
    # Return if this can be processed as well as the output folder.
    return can_process, output_folder_name

# This function determines how much to scale the asset.
def CheckPSPScaling(settings_dict, asset_type, texture_info_dict):
    # Initialize the scale_factor as 1.0.
    scale_factor = 1.0
    # Determine if this is a big texture.
    if settings_dict['big_texture'] == True:
        # This is a big texture.
        # Update the scale_factor.
        scale_factor = 0.5
    else:
        # This is not a big texture.
        # Determine the max texture size.
        if asset_type in ['Conversation Portrait', 'Character Select Portrait']:
            max_size = 64
        elif asset_type in ['Comic Cover', 'Concept Art', 'Loading Screen']:
            max_size = 512
        else:
            max_size = 128
        # Determine if the texture is less than the max size.
        if texture_info_dict['max_texture_size'] > max_size:
            # The texture is bigger than the max size.
            # Update the scale factor.
            scale_factor = max_size / texture_info_dict['max_texture_size']
    # Determine if this is an asset that will be resized by being a secondary skin.
    if asset_type == 'Skin':
        # This is an asset that can be impacted by the secondary skin setting.
        # Check if this is a secondary skin.
        if settings_dict['secondary_skin'] == True:
            # This is a secondary skin.
            # Resize it.
            scale_factor *= 0.5
    # Return the scale factor.
    return scale_factor

# This function process PSP Assets.
def ProcessPSPAsset(asset_type, temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
    # Get the processing status.
    can_process, output_folder_name = CanProcessPSP(settings_dict, texture_info_dict, game, has_cel, output_file_name)
    # Determine if it's okay to proces.
    if can_process == True:
        # It's okay to process.
        # Initialize a list of Alchemy 3.2 optimizations.
        alchemy_32_optimization_list = []
        # Initialize a list of Alchemy 5 optimizations.
        alchemy_5_optimizations_list = []
        # For other models, add the collision generation if required.
        if ((asset_type == 'Other') and (settings['generate_collision'] == True)):
            alchemy_32_optimization_list.append('igCollideHullRaven')
        # Determine the scale factor.
        scale_factor = CheckPSPScaling(settings_dict, asset_type, texture_info_dict)
        # Add the necessary optimizations.
        alchemy_32_optimization_list.extend(['igResizeImage', 'igQuantizeRaven'])
        # Write the Alchemy 3.2 optimization.
        optimizations.WriteOptimization(alchemy_32_optimization_list, alchemy_version = 'Alchemy 3.2', scale_to = scale_factor)
        # Set up an output name for the Alchemy 3.2 optimized file.
        temp_file_hexed_32_path = temp_file_hexed_path.with_name('temph2.igb')
        # Call the Alchemy 3.2 optimization without sending out the final file.
        alchemy.CallAlchemy(temp_file_hexed_path, alchemy_version = 'Alchemy 3.2', output_path = temp_file_hexed_32_path)
        # Determine if the output sub-folder should be skipped.
        if settings_dict['skip_subfolder'] == False:
            # The sub-folder should not be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / output_folder_name / output_file_name
        else:
            # The sub-folder should be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / output_file_name
        # Determine which game and asset this is for.
        if ((game == 'XML2') and (asset_type == 'Skin')):
            # This is for an XML2 skin.
            # Add the optimization that references the other optimization.
            alchemy_5_optimizations_list.append('igOptimizeActorSkinsInScenes')
            # Set up the list of secondary optimizations that are called.
            secondary_optimization_list = ['igConvertGeometryAttr (PSP)', 'igConvertTransform', 'igCollapseAllHierarchies', 'igPromoteAllAttrs', 'igCollapseAllHierarchies', 'igPromoteAllAttrs', 'igCollapseAllHierarchies', 'igCollapseGeometry', 'igCollapseHierarchy (igGeometry)', 'igLimitActorBlendPalettes', 'igCollapseHierarchy (igBlendMatrixSelect)', 'igMSStripTriangles', 'igSetVertexStreamAccessMode', 'igBuildNativeGeometry']
            # Write the secondary Alchemy 5 optimization.
            optimizations.WriteOptimization(secondary_optimization_list, optimization_path = (Path(environ['temp']) / 'opt2.ini'))
        else:
            # This is any asset for MUA1/MUA2 or a static asset for XML2.
            # Add the single necessary optimization.
            alchemy_5_optimizations_list.append('igConvertGeometryAttr')
        # Write the Alchemy 5 optimizations.
        optimizations.WriteOptimization(alchemy_5_optimizations_list)
        # Perform the optimizations.
        alchemy.CallAlchemy(temp_file_hexed_32_path, output_path = output_file_path)
        # Delete the temp file.
        remove(temp_file_hexed_32_path)
        # For XML2, delete the secondary optimization file.
        if game == 'XML2':
            remove(Path(environ['temp']) / 'opt2.ini')