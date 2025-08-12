# ########### #
# INFORMATION #
# ########### #
# This module is used to recognize the asset type from the file name.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import questions
import settings


# ######### #
# FUNCTIONS #
# ######### #
# This function gets the special name for a mannequin.
def GetMannequinSpecialName(input_file_path, settings_dict):
    # Verify that the file name ends with a closing parenthesis.
    if input_file_path.name.endswith(').igb'):
        # The name does end with a closing parenthesis.
        # Verify that there is a dash for the descriptor.
        if input_file_path.name.startswith('123XX (Mannequin - '):
            # The name has the dash for the descriptor.
            # Loop through the games.
            for game in settings.games_list:
                # Determine if the settings already have a special name for this game.
                if settings_dict[f'{game}_special_name'] is None:
                    # There is no special name for this game.
                    # Set the special name from the file name by splitting at the dash and removing the extension.
                    settings_dict[f'{game}_special_name'] = input_file_path.name.split(' - ')[1].replace(').igb', '')
        else:
            # The name does not have the dash for the descriptor.
            # Give an error.
            questions.PrintError(f'{input_file_path.name} was detected as a mannequin due to its file name starting with "123XX (Mannequin", and ending with ").igb", but there is no dash in the middle for the descriptor.', system_exit = True)
    else:
        # The name does not have the closing parenthesis.
        # Give an error.
        questions.PrintError(f'{input_file_path.name} was detected as a mannequin due to its file name starting with "123XX (Mannequin", but it does not have a closing parenthesis in the name.', system_exit = True)
    # Return the settings dictionary.
    return settings_dict

# This function is used to get the special name of an Other model.
def GetOtherSpecialName(input_file_path, settings_dict):
    # Loop through the games.
    for game in settings.games_list:
        # Determine if the settings already have a special name for this game.
        if settings_dict[f'{game}_special_name'] is None:
            # There is no special name for this game.
            # Set the special name using the file name.
            settings_dict[f'{game}_special_name'] = input_file_path.stem
    # Return the updated dictionary.
    return settings_dict

# This function checks if an unknown file is a mannequin.
def CheckIfMannequin(input_file_path, settings_dict):
    # Check if the file name starts with how a mannequin would start.
    if input_file_path.name.startswith('123XX (Mannequin'):
        # This is a mannequin.
        # Set the asset type as a mannequin.
        asset_type = 'Mannequin'
        # Determine if this is a mannequin with a standard name.
        if not(input_file_path.name == '123XX (Mannequin).igb'):
            # This is not a standard name.
            # Get the special name.
            settings_dict = GetMannequinSpecialName(input_file_path, settings_dict)
    else:
        # This is not a mannequin.
        # Set that the asset type is not known.
        asset_type = 'Unknown'
    # Return the asset type and the updated settings.
    return asset_type, settings_dict

# This function lets the user pick the asset type.
def UserPicksAsset(input_file_path, settings_dict, detection_failed):
    # Determine if detection failed.
    if detection_failed == True:
        # The detection failed.
        # Print a warning to the user.
        questions.PrintWarning(f'The asset type of {input_file_path.name} could not be detected from the file name.', skip_pause = True)
    # Ask the user what the asset type is.
    asset_type = questions.Select(f'What type of asset is {input_file_path.name}?', settings.asset_type_list, default_choice = 'Other')
    # Determine if this is a mannequin.
    if asset_type == 'Mannequin':
        # This is a mannequin.
        # Get the special name for the mannequin.
        settings_dict = GetMannequinSpecialName(input_file_path, settings_dict)
    elif asset_type == 'Other':
        # This is an Other asset.
        # Get the special name for the asset.
        settings_dict = GetOtherSpecialName(input_file_path, settings_dict)
    # Return the asset type and the updated settings.
    return asset_type, settings_dict

# This function is used to recognize the asset type.
def AssetRecognition(input_file_path, settings_dict):
    # Determine if the settings are forcing an asset type.
    if settings_dict['forced_asset_type'] is not None:
        # The user forced an asset type.
        # Set that asset type.
        asset_type = settings_dict['forced_asset_type']
        # Announce this.
        questions.PrintSuccess(f'{input_file_path.name} was set as a {asset_type}.')
    elif settings_dict['forced_asset_type'] == 'Ask':
        # The user wants to be asked about the asset type no matter what.
        # Get the asset type from the user.
        asset_type, settings_dict = UserPicksAsset(input_file_path, settings_dict, False)
    else:
        # The user did not force an asset type.
        # Set up the dictionary of file names and their asset types.
        asset_type_dict = {
            'igActor01_Animation01DB.igb': 'Skin',
            '123XX (3D Head).igb': '3D Head',
            'hud_head_123XX.igb': 'Conversation Portrait',
            '123XX (Character Select Portrait).igb': 'Character Select Portrait',
            'power_icons.igb': 'Power Icons',
            'comic_cov.igb': 'Comic Cover',
            'concept.igb': 'Concept Art',
            '123XX (Loading Screen).igb': 'Loading Screen'
        }
        # Try to look up the file name in the dictionary to get the type.
        try:
            asset_type = asset_type_dict[input_file_path.name]
            # If there is no error, then this line is reached. The file type is known, so say so.
            questions.PrintSuccess(f'{input_file_path.name} was automatically identified as a {asset_type}.')
        except KeyError:
            # The file name does not match with one of the listed asset types, but it may be a mannequin. Check the name.
            asset_type, settings_dict = CheckIfMannequin(input_file_path, settings_dict)
            # Determine if a valid asset type was found.
            if asset_type == 'Unknown':
                # The asset type could not be detected.
                # Get the asset type from the user.
                asset_type, settings_dict = UserPicksAsset(input_file_path, settings_dict, True)
            else:
                # This was a mannequin.
                # Announce that it was detected as such.
                questions.PrintSuccess(f'{input_file_path.name} was automatically identified as a mannequin.')
    # Update the consoles based on the asset type.
    if asset_type == 'Mannequin':
        settings_dict['XML1_num'] = None
        settings_dict['XML2_num'] = None
        settings_dict['XML1_path'] = None
        settings_dict['XML2_path'] = None
    elif asset_type in ['3D Head', 'Character Select Portrait']:
        settings_dict['MUA1_num'] = None
        settings_dict['MUA2_num'] = None
        settings_dict['MUA1_path'] = None
        settings_dict['MUA2_path'] = None
    elif asset_type in ['Comic Cover', 'Concept Art']:
        settings_dict['MUA2_num'] = None
        settings_dict['MUA2_path'] = None
    # Return the asset type and the settings.
    return asset_type, settings_dict