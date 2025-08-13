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


# ######### #
# FUNCTIONS #
# ######### #
# This function determines if it's okay to process GameCube assets.
def CanProcessGC(settings_dict, texture_info_dict):
    # Initialize a variable to determine if it's okay to process (assume yes).
    can_process = True
    # Determine if the PS2 is in use.
    if settings_dict['GameCube'] == False:
        # The GameCube is not in use.
        # Do not process.
        can_process = False
    else:
        # The GameCube is in use.
        # Determine if environment maps are in use.
        if ' Env' in texture_info_dict['texture_type']:
            # Environment maps are in use.
            # Determine if the correct environment size is in use.
            if not(texture_info_dict['texture_type'].endswith(f' Env{8}')):
                # The wrong environment map size is in use.
                # Skip processing.
                can_process = False
    # Determine if advanced textures are in use.
    if settings['advanced_texture_ini'] is not None:
        # Advanced textures are in use.
        # Skip processing.
        can_process = False
    # Return the status.
    return can_process

# This function determines how much to scale the asset.
def CheckGCScaling(settings_dict, asset_type, texture_info_dict):
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
        if asset_type in ['Conversation Portrait', 'Character Select Portrait', 'Power Icons']:
            max_size = 128
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

# This function process GameCube assets.
def ProcessGCAsset(asset_type, temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
    # Get whether or not the GC should be processed.
    can_process = CanProcessGC(settings_dict, texture_info_dict)
    # Determine if it's okay to proces.
    if can_process == True:
        # It's okay to process.
        # Initialize a list of optimizations.
        optimization_list = []
        # For other models, add the collision generation if required.
        if ((asset_type == 'Other') and (settings['generate_collision'] == True)):
            optimization_list.append('igCollideHullRaven')
        # Determine the scale factor.
        scale_factor = CheckGCScaling(settings_dict, asset_type, texture_info_dict)
        # Add the necessary optimizations.
        optimization_list.extend(['igResizeImage', 'igQuantizeRaven'])
        ################################################################################################### NEED TO ADD ENVIRONMENT MAP SUPPORT HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Write the optimization.
        optimizations.WriteOptimization(optimization_list, alchemy_version = 'Alchemy 3.2', scale_to = scale_factor)
        # Determine if the output sub-folder should be skipped.
        if settings_dict['skip_subfolder'] == False:
            # The sub-folder should not be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / f'for {game} (GC)' / output_file_name
        else:
            # The sub-folder should be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / output_file_name
        # Perform the Alchemy optimizations.
        alchemy.CallAlchemy(temp_file_hexed_path, alchemy_version = 'Alchemy 3.2', output_path = output_file_path)