# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# External modules
import os
from pathlib import Path
from shutil import copy


# ######### #
# FUNCTIONS #
# ######### #
# This function updates the hex out list and adds game-specific information.
def UpdateHexOutList(hex_out_list, asset_type, texture_info_dict, geometry_list, game, settings_dict):
    # Set the game number.
    game_num = settings_dict[f'{game}_num']
    # Determine if the character number ends in XX.
    if game_num.endswith('XX'):
        # The skin number ends in XX.
        # Update the number.
        game_num_hex = f'{game_num[0-2]}01'
    else:
        # The skin number is a standard number.
        # Update the value.
        game_num_hex = game_num
    # Start a list of in values (this will check for duplicates).
    hex_in_values = []
    # Initialize a list of byte data to hex out.
    hex_out_list_byte = []
    # Loop through the values in the hex out list.
    for hex_out_pair in hex_out_list:
        # Get the items of the pair.
        hex_in_value = hex_out_pair[0]
        hex_out_value = hex_out_pair[1]
        # Add the in value to the list of in values.
        hex_in_values.append(hex_in_value)
        # Determine if the out value has the skin number.
        if '12301' in hex_out_value:
            # There is a skin number.
            # Update the skin number.
            hex_out_value = hex_out_value.replace('12301', game_num_hex)
        # Add the converted data to the byte data list.
        hex_out_list_byte.append([bytearray(hex_in_value, 'utf-8'), bytearray(hex_out_value, 'utf-8')])
    # Loop through the textures.
    for texture_dict in texture_info_dict['textures_list']:
        # Get the input value.
        hex_in_value = str(texture_dict['Name'])
        # Determine if the input value was previously accounted for.
        if not(hex_in_value in hex_in_values):
            # This was not previously accounted for.
            # Get the hex out value.
            hex_out_value = hex_in_value.replace('12301', game_num_hex)
            # Add the converted data to the byte data list.
            hex_out_list_byte.append([bytearray(hex_in_value, 'utf-8'), bytearray(hex_out_value, 'utf-8')])
    # Loop through the geometry names.
    for geometry_name in geometry_list:
        # Determine if this is just the plain '12301' geometry.
        if not(geometry_name == '12301'):
            # This is not the plain '12301' geometry (that entry will be added at the very end).
            # Determine if the input value was previously accounted for.
            if not(geometry_name in hex_in_values):
                # This was not previously accounted for.
                # Get the hex out value.
                hex_out_value = hex_in_value.replace('12301', game_num_hex)
                # Add the converted data to the byte data list.
                hex_out_list_byte.append([bytearray(hex_in_value, 'utf-8'), bytearray(hex_out_value, 'utf-8')])
    # Determine if this is a skin.
    if asset_type == 'Skin':
        # This is a skin.
        # Add the igActor01Appearance value.
        hex_out_list_byte.append([bytearray('igActor01Appearance', 'utf-8'), bytearray(game_num_hex, 'utf-8')])
        # Add the igActor01Skeleton value.
        hex_out_list_byte.append([bytearray('igActor01Skeleton', 'utf-8'), bytearray(f'{game_num_hex}_skel', 'utf-8')])
    # Determine if the user wanted to convert igBlend transparency attributes to igAlpha transparency attributes.
    if settings_dict['igBlend_to_igAlpha_transparency'] == True:
        # The user wanted to convert these attributes.
        # Add the attributes to the list.
        hex_out_list_byte.append([bytearray('igBlendStateAttr', 'utf-8'), bytearray('igAlphaStateAttr', 'utf-8')])
        hex_out_list_byte.append([bytearray('igBlendFunctionAttr', 'utf-8'), bytearray('igAlphaFunctionAttr', 'utf-8')])
    # Add the final 12301 value, which will get anything that's left.
    hex_out_list_byte.append([bytearray('12301', 'utf-8'), bytearray(game_num_hex, 'utf-8')])
    # Return the new list with the byte format data.
    return hex_out_list_byte

# This function hex edits files.
def HexEditor(temp_file_path, temp_file_hexed_path, hex_out_list_byte):
    # Read the file in byte mode
    with open(temp_file_path, 'rb') as f:
        byte = f.read()
    # Loop through the entries in the hex out list.
    for hex_out_pair in hex_out_list_byte:
        # Get the parts of the pair.
        hex_in = hex_out_pair[0]
        hex_out = hex_out_pair[1]
        # Verify that the before value is longer.
        if len(hex_in) >= len(hex_out):
            # The before value is longer.
            # Set up the hex out value with the necessary amount of whitespace.
            hex_out_adjusted = hex_out + bytearray(([0] * (len(hex_in) - len(hex_out))))
            # Update the byte version of the file with the new hex string.
            byte = byte.replace(hex_in, hex_out_adjusted)
    # Replace the same file with the new byte data
    with open(temp_file_hexed_path, 'wb') as f:
        f.write(byte)

# This function coordinates the hex editing.
def HexEdit(temp_file_path, asset_type, hex_out_list, texture_info_dict, geometry_list, game, settings_dict):
    # Add the game-specific information to the hex out list.
    hex_out_list_byte = UpdateHexOutList(hex_out_list, asset_type, texture_info_dict, geometry_list, game, settings_dict)
    # Set up the path to the hex edited file.
    temp_file_hexed_path = Path(os.environ['TEMP']) / 'temph.igb'
    # Perform the hex editing.
    HexEditor(temp_file_path, temp_file_hexed_path, hex_out_list_byte)
    # Return the new file path.
    return temp_file_hexed_path