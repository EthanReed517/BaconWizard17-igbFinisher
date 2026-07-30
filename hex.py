# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Python modules
import os
from pathlib import Path


# ######### #
# FUNCTIONS #
# ######### #
def CreateHexEditPair(bytes_in: bytes, bytes_out: bytes) -> tuple[bytes]:
    '''
    Checks if bytes_out is short enough to fit in bytes_in and, if necessary, pads it to match the length of bytes_in.
    
    returns a pair tuple with the bytes_in and the padded bytes_out values.
    '''
    padding = len(bytes_in) - len(bytes_out)
    # Only skip if that's acceptable:
    #if padding < 0:
    #    return None # or something similar
    # Otherwise, report that hex-editing is impossible
    assert padding > -1, f'Cannot hex edit from {bytes_in} to {bytes_out}, the string is too long.'
    return bytes_in, bytes_out if padding == 0 else bytes_out.ljust(padding, b'\0')

def CreateHexEditPairs(replace_values: list[tuple[bytes]], textures: list[dict], geometries: list[str],
                       is_skin: bool, skin_number: str, igBlend_to_igAlpha_transparency: bool) -> list[tuple[bytes]]:
    '''
    Write the values in the three lists to a list with pairs, where the first item is the input value,
    and the second item is the input value where '12301' is replaced with the skin_number.
    replace_values should contain pairs where the first item is the input value and the second item
    will have '12301' replaced instead of the input value (may contain simple replace strings without '12301' as well).
    If is_skin, replaces igActor01Appearance and igActor01Skeleton,
    and igBlend_to_igAlpha_transparency, replaces the blend attribute strings with the alpha equivalents.
    
    returns the list with the final replace pairs.
    '''
    # If necessary, replace the XX suffix with the number 01.
    if skin_number.endswith('XX'):
        skin_number = f'{game_num[:-2]}01'

    # Initialize a set to check for duplicates. '12301' will be added last.
    in_values = {'12301'}
    # Initialize the final hex edit pair list and a method that only adds unique in values and replaces the placeholder '12301' with the skin_number.
    hex_out_list = []
    def add_pair(in_value: str, out_value: str):
        out_value = out_value.replace('12301', skin_number)
        if in_value not in in_values and in_value != out_value:
            in_values.add(in_value)
            hex_out_list.append(CreateHexEditPair(in_value.encode('ansi'), out_value.encode('ansi')))

    for pair in replace_values:
        # Add the adjusted pair as bytes
        add_pair(*pair)

    for texture_dict in textures:
        texture_name = str(texture_dict['Name']) # note: what other types can this be than str?
        # Add the texture_name and adjusted texture_name as bytes
        add_pair(texture_name, texture_name)

    for geometry_name in geometries:
        # Add the geometry_name and adjusted geometry_name as bytes
        add_pair(geometry_name, geometry_name)

    if is_skin:
        # Add the igActor01Appearance and igActor01Skeleton values.
        hex_out_list.append(CreateHexEditPair(b'igActor01Appearance', skin_number.encode('ansi')))
        hex_out_list.append(CreateHexEditPair(b'igActor01Skeleton', f'{skin_number}_skel'.encode('ansi')))

    if igBlend_to_igAlpha_transparency:
        # The user wants to convert blend to alpha attributes, so add them to the hex edit list.
        hex_out_list.append(CreateHexEditPair(b'igBlendStateAttr', b'igAlphaStateAttr'))
        hex_out_list.append(CreateHexEditPair(b'igBlendFunctionAttr', b'igAlphaFunctionAttr'))

    # Add '12301', which will cover any remaining occurrences.
    hex_out_list.append(CreateHexEditPair(b'12301', skin_number.encode('ansi')))

    return hex_out_list

def HexEdit(file_path: Path, replace_values: list[tuple[bytes]]) -> Path:
    '''
    In temp_file_path, replaces all occurrence of each input value with each output value from replace_values.
    replace_values must contain at least one valid replace pair.
    
    returns the pathlib.Path of the hex-edited file.
    '''
    # If the list can be empty, you might have to check for that, and either silently return the original path or throw an exception.
    data = file_path.read_bytes()
    for bytes_in, bytes_out in replace_values:
        data.replace(hex_in, hex_out_adjusted)
    temp_file_hexed_path = Path(os.environ['TEMP']) / 'temph.igb'
    temp_file_hexed_path.write_bytes(data)
    return temp_file_hexed_path