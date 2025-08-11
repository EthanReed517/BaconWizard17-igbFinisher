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
# This function is used to set up the skin's output file name.
def SetUpSkinName(settings_dict, game, has_cel):
    # Start with the character number.
    output_file_name = settings_dict[f'{game}_num'][0:-2]
    # Determine how the character number should end.
    if settings_dict[f'{game}_num_XX'] == True:
        # The number should end in XX.
        # Add this to the output file name.
        output_file_name += 'XX'
    else:
        # The number should end in the skin number.
        # Add this to the output file name.
        output_file_name += settings_dict[f'{game}_num'][-2:]
    # Determine if it's necessary to include anything else.
    if not(settings_dict[f'{game}_special_name'] == 'NumberOnly'):
        # There should be a descriptor.
        # Add the opening parenthesis.
        output_file_name += ' ('
        # Determine which type of descriptor is needed.
        if settings_dict[f'{game}_special_name'] is None:
            # The user wants the default descriptor.
            # Use the default descriptor.
            output_file_name += 'Skin'
        else:
            # The user wants a custom descriptor.
            # Add the custom descritpro.
            output_file_name += settings_dict[f'{game}_special_name']
        # Determine if this is an XML1/XML2 skin without cel shading.
        if ((game in ['XML1', 'XML2']) and (has_cel == False)):
            # This is an XML1/XML2 skin without cel shading.
            # Add the no cel descriptor.
            output_file_name += ' - No Cel'
        # Add the closing parenthesis.
        output_file_name += ')'
    # Add the file extension.
    output_file_name += '.igb'
    # Return the output file name.
    return output_file_name

# This function is used to get a list of transparent textures and write their names to the temp file.
def TransparentTextureNames(textures_list):
    # Set up a list of transparent textures.
    transparent_textures = []
    # Loop through the textures in the list.
    for texture_dict in textures_list:
        # Determine if this is a transparent texture.
        if texture_dict['Format'] == 'IG_GFX_TEXTURE_FORMAT_RGB_8888_32 (7)':
            # This is a transparent texture.
            # Add its file name to a list.
            transparent_textures.append(texture_dict['Name'].name)
    # Open the temp file.
    with open((Path(environ['temp']) / 'temp.txt'), 'w') as file:
        # Loop through the texture names.
        for transparent_texture_name in transparent_textures:
            # Write the name to the list.
            file.write(f'{transparent_texture_name}\n')

# This function process Xbox and XML2 PC skins.
def ProcessXboxSkin(temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
    # Initialize a variable to determine if it's okay to process (assume yes).
    can_process = True
    # Initialize the output folder name (assume Xbox only).
    output_folder_name = f'for {game} (Xbox)'
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
                    output_folder_name = 'for XML2 (PC)'
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
                    # Update the folder name.
                    output_folder_name = 'for XML2 (PC and Xbox)'
                else:
                    # The Xbox is not in use.
                    # Update the folder name.
                    output_folder_name = 'for XML2 (PC)'
            else:
                # The PC is not in use.
                # Determine if the Xbox is in use.
                if settings_dict['Xbox'] == False:
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
    # Determine if it's okay to process.
    if can_process == True:
        # It's okay to process.
        # Initialize a list of optimizations.
        optimization_list = []
        # Determine the texture size.
        if texture_info_dict['max_texture_size'] > 256:
            # This is a large texture.
            # Convert to DXT1 (automatically preserves transparent textures).
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
                TransparentTextureNames(texture_info_dict['textures_list'])
                # Convert to PNG8, skipping transparent textures.
                optimization_list.append('igQuantizeRaven (exclude)')
        ################################################################################################### NEED TO ADD ENVIRONMENT MAP SUPPORT HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Write the optimization.
        optimizations.WriteOptimization(optimization_list, alchemy_version = 'Alchemy 3.2')
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

# This function process PS2 skins.
def ProcessPS2Skin(temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
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
    # Determine if it's okay to proces.
    if can_process == True:
        # It's okay to process.
        # Initialize a list of optimizations.
        optimization_list = []
        # Determine if the scale factor.
        if settings_dict['big_texture'] == True:
            # This is a big texture, which can keep its original size.
            # Set the scale factor.
            scale_factor = 1.0
        else:
            # This is not a big texture, so the max is 256.
            # Determine if this is already under or at 256.
            if texture_info_dict['max_texture_size'] <= 256:
                # This is already under or at 256.
                # Set the scale factor to 1.
                scale_factor = 1.0
            else:
                # This is over 256.
                # Set the scale factor to scale to 256.
                scale_factor = 256 / texture_info_dict['max_texture_size']
        # Determine if this is a secondary skin.
        if settings_dict['secondary_skin'] == True:
            # This is a secondary skin.
            # Cut the scale factor in half.
            scale_factor *= 0.5
        # Determine if this is for MUA2.
        if game == 'MUA2':
            # This is for MUA2.
            # Cut the scale factor in half.
            scale_factor *= 0.5
        # Add the scaling optimization.
        optimization_list.append('igResizeImage')
        # Add the conversion to PNG8.
        optimization_list.append('igQuantizeRaven')
        ################################################################################################### NEED TO ADD ENVIRONMENT MAP SUPPORT HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
            # Perform the Alchemy 3.2 optimizations without sending the file.
            alchemy.CallAlchemy(temp_file_hexed_path, alchemy_version = 'Alchemy 3.2')
            # Write a new optimization file for Alchemy 5.
            optimizations.WriteOptimization(['igConvertGeometryAttr'])
            # Perform the Alchemy 5 optimization.
            alchemy.CallAlchemy(temp_file_hexed_path, output_path = output_file_path)
        else:
            # This is for the other games.
            # Perform the Alchemy optimizations.
            alchemy.CallAlchemy(temp_file_hexed_path, alchemy_version = 'Alchemy 3.2', output_path = output_file_path)

# This function process GameCube skins.
def ProcessGCSkin(temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
    # Initialize a variable to determine if it's okay to process (assume yes).
    can_process = True
    # Determine if the GameCube is in use.
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
            if not(texture_info_dict['texture_type'].endswith(' Env8')):
                # The wrong environment map size is in use.
                # Skip processing.
                can_process = False
    # Determine if it's okay to proces.
    if can_process == True:
        # It's okay to process.
        # Initialize a list of optimizations.
        optimization_list = []
        # Determine the scale factor.
        if settings_dict['big_texture'] == True:
            # This is a big texture, which can be half the original size regardless.
            # Set the scale factor.
            scale_factor = 0.5
        else:
            # This is not a big texture, so the max is 128.
            # Determine if this is already under or at 128.
            if texture_info_dict['max_texture_size'] <= 128:
                # This is already under or at 128.
                # Set the scale factor to 1.0.
                scale_factor = 1.0
            else:
                # This is over 256.
                # Set the scale factor to scale to 128.
                scale_factor = 128 / texture_info_dict['max_texture_size']
        # Determine if this is a secondary skin.
        if settings_dict['secondary_skin'] == True:
            # This is a secondary skin.
            # Cut the scale factor in half.
            scale_factor *= 0.5
        # Add the scaling optimization.
        optimization_list.append('igResizeImage')
        # Add the conversion to PNG8.
        optimization_list.append('igQuantizeRaven')
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

# This function process XML2 PSP skins.
def ProcessXML2PSPSkin(temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
    # Initialize a variable to determine if it's okay to process (assume yes).
    can_process = True
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
    # Determine if it's okay to proces.
    if can_process == True:
        # It's okay to process.
        # Initialize a list of Alchemy 3.2 optimizations.
        alchemy_32_optimization_list = []
        # Initialize a list of Alchemy 5 optimizations.
        alchemy_5_optimizations_list = []
        # Determine the scale factor.
        if settings_dict['big_texture'] == True:
            # This is a big texture, which can be half the original size regardless.
            # Set the scale factor.
            scale_factor = 0.5
        else:
            # This is not a big texture, so the max is 128.
            # Determine if this is already under or at 128.
            if texture_info_dict['max_texture_size'] <= 128:
                # This is already under or at 128.
                # Set the scale factor to 1.0.
                scale_factor = 1.0
            else:
                # This is over 256.
                # Set the scale factor to scale to 128.
                scale_factor = 128 / texture_info_dict['max_texture_size']
        # Determine if this is a secondary skin.
        if settings_dict['secondary_skin'] == True:
            # This is a secondary skin.
            # Cut the scale factor in half.
            scale_factor *= 0.5
        # Add the scaling optimization.
        alchemy_32_optimization_list.append('igResizeImage')
        # Add the conversion to PNG8.
        alchemy_32_optimization_list.append('igQuantizeRaven')
        # Add the optimization that references the other optimization.
        alchemy_5_optimizations_list.append('igOptimizeActorSkinsInScenes')
        # Set up the list of secondary optimizations that are called.
        secondary_optimization_list = ['igConvertGeometryAttr (PSP)', 'igConvertTransform', 'igCollapseAllHierarchies', 'igPromoteAllAttrs', 'igCollapseAllHierarchies', 'igPromoteAllAttrs', 'igCollapseAllHierarchies', 'igCollapseGeometry', 'igCollapseHierarchy (igGeometry)', 'igLimitActorBlendPalettes', 'igCollapseHierarchy (igBlendMatrixSelect)', 'igMSStripTriangles', 'igSetVertexStreamAccessMode', 'igBuildNativeGeometry']
        # Determine if the output sub-folder should be skipped.
        if settings_dict['skip_subfolder'] == False:
            # The sub-folder should not be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / f'for {game} (PSP)' / output_file_name
        else:
            # The sub-folder should be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / output_file_name
        # Write the Alchemy 3.2 optimization.
        optimizations.WriteOptimization(alchemy_32_optimization_list, alchemy_version = 'Alchemy 3.2', scale_to = scale_factor)
        # Set up an output name for the Alchemy 3.2 optimized file.
        temp_file_hexed_32_path = temp_file_hexed_path.with_name('temph2.igb')
        # Call the Alchemy 3.2 optimization without sending out the final file.
        alchemy.CallAlchemy(temp_file_hexed_path, alchemy_version = 'Alchemy 3.2', output_path = temp_file_hexed_32_path)
        # Write the Alchemy 5 optimizations.
        optimizations.WriteOptimization(alchemy_5_optimizations_list)
        optimizations.WriteOptimization(secondary_optimization_list, optimization_path = (Path(environ['temp']) / 'opt2.ini'))
        # Perform the optimizations
        alchemy.CallAlchemy(temp_file_hexed_32_path, output_path = output_file_path)
        # Delete the temp file.
        remove(temp_file_hexed_32_path)
        # Delete the secondary optimization.
        remove(Path(environ['temp']) / 'opt2.ini')

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

# This function process MUA1/MUA2 PSP skins.
def ProcessPSPSkin(temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel):
    # Initialize a variable to determine if it's okay to process (assume yes).
    can_process = True
    # Initialize the output folder name (assume one game only).
    output_folder_name = f'for {game} (PSP)'
    # Determine if the PSP is in use.
    if settings_dict['PSP'] == False:
        # The PSP is not in use.
        # Skip processing.
        can_process = False
    else:
        # The PSP is in use.
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
                output_folder_name = 'for MUA1 (PSP) and MUA2 (PSP)'
            else:
                # This is for MUA2.
                # Skip processing, as processing was already handled for MUA1.
                can_process = False
    # Determine if it's okay to process.
    if can_process == True:
        # It's okay to process.
        # Determine the scale factor.
        if settings_dict['big_texture'] == True:
            # This is a big texture, which can be half the original size regardless.
            # Set the scale factor.
            scale_factor = 0.5
        else:
            # This is not a big texture, so the max is 128.
            # Determine if this is already under or at 128.
            if texture_info_dict['max_texture_size'] <= 128:
                # This is already under or at 128.
                # Set the scale factor to 1.0.
                scale_factor = 1.0
            else:
                # This is over 256.
                # Set the scale factor to scale to 128.
                scale_factor = 128 / texture_info_dict['max_texture_size']
        # Determine if this is a secondary skin.
        if settings_dict['secondary_skin'] == True:
            # This is a secondary skin.
            # Cut the scale factor in half.
            scale_factor *= 0.5
        # Determine if the output sub-folder should be skipped.
        if settings_dict['skip_subfolder'] == False:
            # The sub-folder should not be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / output_folder_name / output_file_name
        else:
            # The sub-folder should be skipped.
            # Set up the destination path.
            output_file_path = settings_dict[f'{game}_path'] / output_file_name
        # Write the Alchemy 3.2 optimization.
        optimizations.WriteOptimization(['igResizeImage', 'igQuantizeRaven'], alchemy_version = 'Alchemy 3.2', scale_to = scale_factor)
        # Set up an output name for the Alchemy 3.2 optimized file.
        temp_file_hexed_32_path = temp_file_hexed_path.with_name('temph2.igb')
        # Call the Alchemy 3.2 optimization without sending out the final file.
        alchemy.CallAlchemy(temp_file_hexed_path, alchemy_version = 'Alchemy 3.2', output_path = temp_file_hexed_32_path)
        # Write the Alchemy 5 optimizations.
        optimizations.WriteOptimization(['igConvertGeometryAttr'])
        # Perform the optimizations
        alchemy.CallAlchemy(temp_file_hexed_32_path, output_path = output_file_path)
        # Delete the temp file.
        remove(temp_file_hexed_32_path)

# This function is the main function used to process skins.
def ProcessSkin(input_file_path, settings_dict, texture_info_dict, hex_out_list, geometry_list, has_cel):
    # This is the dictionary of processes by game.
    game_console_process_dict = {
        'XML1': [ProcessXboxSkin, ProcessPS2Skin, ProcessGCSkin],
        'XML2': [ProcessXboxSkin, ProcessPS2Skin, ProcessGCSkin, ProcessXML2PSPSkin],
        'MUA1': [ProcessPC360Skin, ProcessPS3SteamSkin, ProcessWiiSkin, ProcessXboxSkin, ProcessPS2Skin, ProcessPSPSkin],
        'MUA2': [ProcessWiiSkin, ProcessPS2Skin, ProcessPSPSkin]
    }
    # Set up the temp file for processing.
    temp_file_path = alchemy.CreateAnimDB(input_file_path)
    # Loop through the games.
    for game in settings.games_list:
        # Determine if the game is in use.
        if ((settings_dict[f'{game}_num'] is not None) and (settings_dict[f'{game}_path'] is not None)):
            # The game is in use.
            # Set up the output file name.
            output_file_name = SetUpSkinName(settings_dict, game, has_cel)
            # Hex edit the file.
            temp_file_hexed_path = hex.HexEdit(temp_file_path, 'Skin', hex_out_list, texture_info_dict, geometry_list, settings_dict[f'{game}_num'])
            # Loop through the possible functions for the game.
            for console_process in game_console_process_dict[game]:
                # Perform the processing.
                console_process(temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel)
            # Delete the hex edited file.
            remove(temp_file_hexed_path)
    # Delete the temp file.
    remove(temp_file_path)