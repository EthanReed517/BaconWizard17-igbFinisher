# ########### #
# INFORMATION #
# ########### #
# This module is used for common operations in processing as well as to set up file names.


# ####### #
# IMPORTS #
# ####### #
# External modules
from os import environ
from pathlib import Path


# ######### #
# FUNCTIONS #
# ######### #
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