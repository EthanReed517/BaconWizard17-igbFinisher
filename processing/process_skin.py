# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import optimizations
import questions
import settings
# External modules
import os
from pathlib import Path
from shutil import copy


# ######### #
# FUNCTIONS #
# ######### #
# This function is used to set up the skin's output file name.
def SetUpSkinName(settings_dict, game, **kwargs):
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
        if ((game in ['XML1', 'XML2']) and (kwargs.get('skin_has_cel', False) == False)):
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
    with open((Path(os.environ['temp']) / 'temp.txt'), 'w') as file:
        # Loop through the texture names.
        for transparent_texture_name in transparent_textures:
            # Write the name to the list.
            file.write(f'{transparent_texture_name}\n')

# This function processes XML1 skins.
def ProcessXML1Skin(input_file_path, settings_dict, texture_info_dict, hex_out_list, geometry_list, has_cel):
    # Set up the output file name.
    output_file_name = SetUpSkinName(settings_dict, 'XML1', skin_has_cel = has_cel)
    # Determine if the Xbox is in use.
    if settings_dict['Xbox'] == True:
        # Set the Xbox status (assume can be processed)
        process_status = True
        # Determine if there are environment maps.
        if ' Env' in texture_info_dict['texture_type']:
            # There are environment maps.
            # Determine if they're the right size.
            if not(texture_info_dict['texture_type'].endswith(' Env32')):
                # This is the wrong size.
                # The file should not be processed.
                process_status = False
        # Determine if processing is correct.
        if process_status == True:
            # It's correct to process.
            # Copy the input file to a temp file.
            temp_file_path = Path(os.environ['temp']) / 'temp.igb'
            copy(input_file_path, temp_file_path)
            # Initialize a list of optimizations.
            optimization_list = []
            # Determine if the texture is transparent.
            if 'Opaque' in texture_info_dict['texture_type']:
                # The texture is opaque.
                # Add the necessary optimization.
                optimization_list.append('igQuantizeRaven')
            else:
                # The texture is transparent.
                # Write the list of transparent textures.
                TransparentTextureNames(texture_info_dict['textures_list'])
                # Add the necessary optimization.
                optimization_list.append('igQuantizeRaven (skip)')
            # Determine if there are environment maps.
            #if ' Env' in texture_info_dict['texture_type']:
                # There are environment maps.
                # Write the list of non-environment textures.
                #NonEnvironmentTextureNames(texture_info_dict['textures_list'])
                # Add the necessary optimization.
                #optimization_list.append('igConvertImage (PNG8)')
            # Write the optimization.
            optimizations.WriteOptimization(optimization_list, alchemy_version = 'Alchemy 3.2')
            # Perform the Alchemy optimizations.
            alchemy.CallAlchemy(temp_file_path, alchemy_version = 'Alchemy 3.2')
            # Create the destination folder.
            os.makedirs(settings_dict['XML1_path'] / 'Xbox', exist_ok = True)
            # Copy the file to the destination.
            copy(temp_file_path, settings_dict['XML1_path'] / 'Xbox' / output_file_name)

# This function is the main function used to process skins.
def ProcessSkin(input_file_path, settings_dict, texture_info_dict, hex_out_list, geometry_list, has_cel):
    # Determine if XML1 is in use.
    if ((settings_dict['XML1_num'] is not None) and (settings_dict['XML1_path'] is not None)):
        # XML1 is in use.
        # Process for XML1
        ProcessXML1Skin(input_file_path, settings_dict, texture_info_dict, hex_out_list, geometry_list, has_cel)