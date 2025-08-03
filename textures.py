# ########### #
# INFORMATION #
# ########### #
# This module is used to recognize information about the model's textures.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import questions


# ######### #
# FUNCTIONS #
# ######### #
# This function is used to get the texture information from the model.
def GetTextureInfo(input_file_path, settings_dict):
    # Get the texture information from Alchemy.
    textures_list = alchemy.GetTexPath(input_file_path)
    
    # Fake values to prevent anything breaking, will be updated later.
    hex_out_list = []
    texture_type = 0
    max_texture_size = 0
    # Return the necessary information.
    return settings_dict, hex_out_list, texture_type, max_texture_size