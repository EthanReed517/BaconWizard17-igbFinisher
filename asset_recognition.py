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
    # The file should always end in a closing parenthesis.
    if input_file_path.name.endswith(').igb'):
        # The name should have a dash if there is a descriptor.
        if input_file_path.name.startswith('123XX (Mannequin - '):
            # Set the descriptor only if there is not already a special name.
            for game in settings.games_list:
                if settings_dict[f'{game}_special_name'] is None:
                    settings_dict[f'{game}_special_name'] = input_file_path.name.split(' - ')[1].replace(').igb', '')
        else:
            # If there is no dash, give an error.
            questions.PrintError(f'{input_file_path.name} was detected as a mannequin due to its file name starting with "123XX (Mannequin", and ending with ").igb", but there is no dash in the middle for the descriptor.', system_exit = True)
    else:
        # If there is no closing parenthesis, give an error.
        questions.PrintError(f'{input_file_path.name} was detected as a mannequin due to its file name starting with "123XX (Mannequin", but it does not have a closing parenthesis in the name.', system_exit = True)
    return settings_dict

# This function is used to get the special name of an Other model.
def GetOtherSpecialName(input_file_path, settings_dict):
    # The special name is set as the setting or as the file name if no setting is given.
    for game in settings.games_list:
        if settings_dict[f'{game}_special_name'] is None:
            settings_dict[f'{game}_special_name'] = input_file_path.stem
    return settings_dict

# This function checks if an unknown file is a mannequin.
def CheckIfMannequin(input_file_path, settings_dict):
    # Mannequins all start the same way but may have a special descriptor.
    if input_file_path.name.startswith('123XX (Mannequin'):
        asset_type = 'Mannequin'
        if not(input_file_path.name == '123XX (Mannequin).igb'):
            settings_dict = GetMannequinSpecialName(input_file_path, settings_dict)
    else:
        asset_type = 'Unknown'
    return asset_type, settings_dict

# This function lets the user pick the asset type.
def UserPicksAsset(input_file_path, settings_dict, detection_failed):
    # Warn the user if detection failed.
    if detection_failed == True:
        questions.PrintWarning(f'The asset type of {input_file_path.name} could not be detected from the file name.', skip_pause = True)
    # Ask the user what the asset type is.
    asset_type = questions.Select(f'What type of asset is {input_file_path.name}?', settings.asset_type_list, default_choice = 'Other')
    # Get the special name for mannequins and other models.
    if asset_type == 'Mannequin':
        settings_dict = GetMannequinSpecialName(input_file_path, settings_dict)
    elif asset_type == 'Other':
        settings_dict = GetOtherSpecialName(input_file_path, settings_dict)
    return asset_type, settings_dict

# This function is used to recognize the asset type.
def AssetRecognition(input_file_path, settings_dict):
    # Determine if the settings are forcing an asset type.
    if settings_dict['forced_asset_type'] is not None:
        asset_type = settings_dict['forced_asset_type']
        questions.PrintSuccess(f'{input_file_path.name} was set as a {asset_type}.')
    elif settings_dict['forced_asset_type'] == 'Ask':
        # The user wants to be asked about the asset type no matter what.
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
            # If there is no error, then this line is reached. The file type is known.
            questions.PrintSuccess(f'{input_file_path.name} was automatically identified as a {asset_type}.')
        except KeyError:
            # The file name does not match with one of the listed asset types, but it may be a mannequin. Check the name.
            asset_type, settings_dict = CheckIfMannequin(input_file_path, settings_dict)
            if asset_type == 'Unknown':
                # The asset type could not be detected. The user should pick.
                asset_type, settings_dict = UserPicksAsset(input_file_path, settings_dict, True)
            else:
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