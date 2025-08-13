# ########### #
# INFORMATION #
# ########### #
# This module is used to get the settings from the settings.ini file.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import questions
# External modules
import argparse
from configparser import ConfigParser
import os.path
from pathlib import Path
import sys


# ################ #
# GLOBAL VARIABLES #
# ################ #
# The list of games in the series.
games_list = ['XML1', 'XML2', 'MUA1', 'MUA2']
# The list of possible consoles.
consoles_list = ['PC', 'Steam', 'GameCube', 'PS2', 'PS3', 'PSP', 'Wii', 'Xbox', 'Xbox 360']
# A dictionary of Boolean strings to their Boolean values.
bool_dict = {'True': True, 'False': False}
# The list of possible asset types.
asset_type_list = ['Skin', 'Mannequin', '3D Head', 'Conversation Portrait', 'Character Select Portrait', 'Power Icons', 'Comic Cover', 'Concept Art', 'Loading Screen', 'Other']


# ######### #
# FUNCTIONS #
# ######### #
# This function processes the arguments.
def ProcessArguments(application_path):
    # Create an argument parser.
    parser = argparse.ArgumentParser()
    # Add an argument for the input file's path.
    parser.add_argument('input_file_path')
    # Add an argument for the settings file path.
    parser.add_argument('-s', '--settings')
    # Parse the arguments.
    args = parser.parse_args()
    # Check if the input file path can be converted to a path.
    try:
        input_file_path = Path(args.input_file_path)
        # Check if the input file exists.
        if not(input_file_path.exists()):
            # The input path does not exist.
            # Print the error.
            questions.PrintError(f'The input file ({args.input_file_path}) does not exist.', system_exit = True)
        elif not(input_file_path.suffix == '.igb'):
            # This is not an igb file.
            # Print the error.
            questions.PrintError(f'The input file ({args.input_file_path}) is not a .igb file.', system_exit = True)
    except Exception as e:
        # The file path couldn't be converted for some reason.
        questions.PrintError(f'The input file ({args.input_file_path}) could not be processed as a path.', error_text = e, system_exit = True)
    # Check if a settings path was entered.
    try:
        args.settings_file_path
        # A path was entered. Attempt to convert the path to a path.
        try:
            settings_file_path = Path(args.settings_file_path)
            # Check if the settings file exists.
            if not(settings_file_path.exists()):
                # The settings file doesn't exist.
                # Print the error.
                questions.PrintError(f'The input settings file ({args.settings_file_path}) does not exist.', system_exit = True)
        except Exception as e:
            # The file path couldn't be converted for some reason.
            questions.PrintError(f'The input settings file ({args.settings_file_path}) could not be processed as a path.', error_text = e, system_exit = True)
    except AttributeError:
        # There was an attribute error, which means that a settings path was not entered. This is okay, and it just means the default path should be used.
        settings_file_path = application_path / 'settings.ini'
    except Exception as e:
        # There was some other error. Print an error message.
        questions.PrintError(f'An unexpected error occurred when attempting to parse the argument for the settings file path.', error_text = e, contact_creator = True, system_exit = True)
    # Return the collected arguments.
    return input_file_path, settings_file_path

# This function determines if the settings.ini file exists.
def VerifySettingsExistence(settings_file_path):
    # Check if the file exists.
    if not(settings_file_path.exists()):
        # The path doesn't exist.
        # Give an error.
        questions.PrintError(f'{settings_file_path} does not exist. Restore the file and try again.', system_exit = True)

# This function reads the settings file and verifies its integrity. It does not pull or verify values.
def ReadAndConfirmSettingsStructure(settings_file_path):
    # Set up the config parser class.
    config = ConfigParser()
    # Read the settings file.
    try:
        config.read(settings_file_path)
    except Exception as e:
        # The file could not be read.
        # Print the error message.
        questions.PrintError(f'Failed to open settings.ini. Address the error and try again.', error_text = e, system_exit = True)
    # Create another while loop that won't end until it's broken.
    # Set up the disctionary of sections and keys.
    section_key_dict = {
        'CHARACTER': ['XML1_num', 'XML2_num', 'MUA1_num', 'MUA2_num', 'XML1_path', 'XML2_path', 'MUA1_path', 'MUA2_path'],
        'ASSET': ['XML1_num_xx', 'XML2_num_XX', 'MUA1_num_XX', 'MUA2_num_XX', 'XML1_special_name', 'XML2_special_name', 'MUA1_special_name', 'MUA2_special_name'],
        'CONSOLES': consoles_list,
        'SETTINGS': ['big_texture', 'secondary_skin', 'untextured_okay', 'generate_collision', 'igBlend_to_igAlpha_transparency', 'skip_subfolder', 'force_adv_tex_folders', 'advanced_texture_ini', 'forced_asset_type']
    }
    # Loop through the sections (the sections of the ini file are the keys of the dictionary, and the keys of the ini file make up a list that's the value of the dictionary).
    for section, key_list in section_key_dict.items():
        try:
            # Attempt to access the section.
            config[section]
            try:
                # Loop through the key list.
                for key in key_list:
                    # Attempt to access the value.
                    config[section][key.replace(' ', '_')]
            except Exception as e:
                # The key could not be accessed.
                questions.PrintError(f'Error when accessing key {e} in section \'{section}\' of settings.ini.', system_exit = True)
        except Exception as e:
            # The section could not be accessed.
            # Print the error message.
            questions.PrintError(f'Error when accessing section {e} in settings.ini.', system_exit = True)
    # Return the read settings file
    return config

# This function gets all of the settings from the config file or user.
def GetSettings(settings_file_path, config):
    # Initialize a dictionary to store the settings.
    settings_dict = {}
    # Get the game-specific settings.
    settings_dict = GetGameSpecificSettings(settings_dict, config)
    # Get the console-specific settings.
    settings_dict = GetConsoleSpecificSettings(settings_dict, config)
    # Get the remaining settings.
    settings_dict = GetRemainingSettings(settings_dict, config)
    # Set a temporary variable for the debug mode.
    settings_dict = GetDebugStatus(settings_dict, config)
    # Return the dictionary of settings.
    return settings_dict

# This function gets the game-specific settings.
def GetGameSpecificSettings(settings_dict, config):
    # Loop through the games in the series.
    for game in games_list:
        # Get the skin number for that game.
        game_number = SkinNumberGetter(config, game)
        # Check if a number was set for this game.
        if game_number is None:
            # There is no number for this game.
            # No path is needed for the game.
            game_path = None
            # The numbering convention can be set to the default (True)
            game_num_XX = True
            # No special name is needed for this game.
            game_special_name = None
        else:
            # There is a number for this game.
            # Get the path for this game.
            game_path = GamePathGetter(config, game)
            # Determine if any path was given.
            if game_path is None:
                # No path was given.
                # The numbering convention can be set to the default (True).
                game_num_XX = True
                # No special name is needed for this game.
                game_special_name = None
            else:
                # A path was given.
                # Get the numbering convention fot this game.
                game_num_XX = GetTrueFalseAskSetting(config, 'ASSET', f'{game}_num_XX', f'the numbering convention for {game}', 'Should the number in the file name end in XX?', True)
                # Get the special name for this game.
                game_special_name = GetGameSpecialName(config, game)
        # Write the game-specific settings.
        settings_dict[f'{game}_num'] = game_number
        settings_dict[f'{game}_path'] = game_path
        settings_dict[f'{game}_num_XX'] = game_num_XX
        settings_dict[f'{game}_special_name'] = game_special_name
    # Return the dictionary of settings.
    return settings_dict

# This function gets the console-specific settings.
def GetConsoleSpecificSettings(settings_dict, config):
    # Loop through the possible consoles.
    for console in consoles_list:
        # Get the status of that console.
        console_status = GetTrueFalseAskSetting(config, 'CONSOLES', console.replace(' ', '_'), f'if assets should be exported for {console}', f'Should assets be exported for {console}?', True)
        # Write the console's status to the settings.
        settings_dict[console.replace(' ', '_')] = console_status
    # Return the dictionary of settings.
    return settings_dict

# This function gets the remaining settings.
def GetRemainingSettings(settings_dict, config):
    # Get the settings that can be True, False, or Ask
    settings_dict['big_texture'] = GetTrueFalseAskSetting(config, 'SETTINGS', 'big_texture', 'if assets with textures over 256x256 should retain the default size for weaker consoles', 'Should assets with textures over 256x256 be kept at their original size on weaker consoles?', False)
    settings_dict['secondary_skin'] = GetTrueFalseAskSetting(config, 'SETTINGS', 'secondary_skin', 'if this is a secondary skin', 'Is this a secondary skin?', False)
    settings_dict['untextured_okay'] = GetTrueFalseAskSetting(config, 'SETTINGS', 'untextured_okay', 'if it\'s okay for 3D assets to lack textures', 'Is it okay if 3D assets lack textures?', False)
    settings_dict['generate_collision'] = GetTrueFalseAskSetting(config, 'SETTINGS', 'generate_collision', 'if collision should be generated for Other models', 'Should collision be generated for Other models?', False)
    settings_dict['igBlend_to_igAlpha_transparency'] = GetTrueFalseAskSetting(config, 'SETTINGS', 'igBlend_to_igAlpha_transparency', 'if igBlendStateAttr/igBlendFunctionAttr attributes should be converted to igAlphaStateAttr/igAlphaFunctionAttr attributes in transparent models', 'Should igBlendStateAttr/igBlendFunctionAttr attributes be converted to igAlphaStateAttr/igAlphaFunctionAttr attributes in transparent models?', False)
    settings_dict['skip_subfolder'] = GetTrueFalseAskSetting(config, 'SETTINGS', 'skip_subfolder', 'if subfolders should be skipped for the resulting model', 'Should subfolders be skipped for the resulting model?', False)
    settings_dict['force_adv_tex_folders'] = GetTrueFalseAskSetting(config, 'SETTINGS', 'force_adv_tex_folders', 'if the advanced texture folder structure should be forced', 'For the advanced texture folder structure?', False)
    settings_dict['advanced_texture_ini'] = GetAdvancedTextureINIPath(config)
    settings_dict['forced_asset_type'] = GetForcedAssetType(config)
    # Return the dictionary of settings.
    return settings_dict

# This function is used to get skin numbers from the settings.
def SkinNumberGetter(config, game):
    # Get the number from the settings.
    game_number = config['CHARACTER'][f'{game}_num']
    # Determine what the value is.
    if game_number == 'Ask':
        # The user wants to be asked about the number.
        # Ask about the number.
        game_number = questions.TextInput(f'What is the skin number for {game}?', validator = questions.SkinNumberValidator)
    elif game_number == 'None':
        # There shouldn't be any number for this game.
        # Update the number to the None value.
        game_number = None
    else:
        # A number was entered.
        # Check if the number is the correct length.
        if ((len(game_number) == 4) or (len(game_number) == 5)):
            # The length of the number is correct.
            # Check if the number is numeric.
            if game_number.isnumeric():
                # The number is numeric.
                # Check if the character number is between 00 and 255.
                if not((int(game_number[0:-2]) >= 0) and (int(game_number[0:-2]) <= 255)):
                    # The number is not between 00 and 255.
                    # Get the correct number from the user.
                    questions.PrintError(f'The first {len(game_number) - 2} digits of the skin number for {game} ("{game}_num" in settings.ini) are not between 00 and 255.', system_exit = True)
            else:
                # The number is not numeric.
                # Get the correct number from the user.
                questions.PrintError(f'The skin number for {game} ("{game}_num" in settings.ini) is not a number.', system_exit = True)
        else:
            # The number is not the correct length.
            # Get the correct number from the user.
            questions.PrintError(f'The skin number for {game} ("{game}_num" in settings.ini) is not the correct length (4 or 5 digits).', system_exit = True)
    # Return the skin number.
    return game_number

# This function is used to get game paths from the settings.
def GamePathGetter(config, game):
    # Get the number from the settings.
    game_path = config['CHARACTER'][f'{game}_path']
    # Check the path value.
    if game_path == 'Ask':
        # The user wants to be asked about the path.
        # Ask about the path.
        game_path = questions.PathInput(f'What path should be used for {game}?', validator = questions.PathValidator)
    elif game_path == 'Detect':
        # This is one of the allowed strings that can stay as a string.
        # Nothing needs to be done here.
        pass
    elif game_path == 'None':
        # This is the None value.
        # Convert it to a None value.
        game_path = None
    else:
        # This is not one of the available strings.
        try:
            # Check if the string is a path
            game_path = Path(game_path)
            # If there are no issues in the previous step, then this can be converted to a path. Check if the path exists.
            if not(game_path.exists()):
                # The path does not exist.
                # Give an error.
                questions.PrintError(f'The path entered for {game}, {game_path}, ("{game}_path" in settings.ini) does not exist.', system_exit = True)
        except Exception as e:
            # The path could not be made a path.
            questions.PrintError(f'The path entered for {game}, {game_path}, ("{game}_path" in settings.ini) is not a recognized value.', error_text = e, system_exit = True)
    # Return the skin number.
    return game_path

# This function is used to get the value from a settings whose options are True, False, and Ask.
def GetTrueFalseAskSetting(config, section, key, setting_name, question_string, default_setting):
    # Get the numbering convention from the settings.
    setting_value = config[section][key]
    # Check the possible values.
    if setting_value in ['True', 'False']:
        # The value is a boolean.
        # Convert it to a boolean.
        setting_value = bool_dict[setting_value]
    elif ask_about_value == 'Ask':
        # The user wants to be asked about the value.
        # Ask about the value.
        setting_value = questions.Confirm(question_string, default_choice = default_setting)
    else:
        # The value is something else.
        # Give an error.
        questions.PrintError(f'The value for {setting_name} ("{key}" in settings.ini) is not a recognized value.', system_exit = True)
    # Return the collected setting.
    return setting_value

# This function is used to get a game's special asset name from the settings.
def GetGameSpecialName(config, game):
    # Get the special name from the settings.
    game_special_name = config['ASSET'][f'{game}_special_name']
    # Check what was found.
    if game_special_name == "None":
        # No special name is needed.
        # Update this to a None type.
        game_special_name = None
    elif game_special_name == "Ask":
        # The user wants to be asked.
        # Ask about the value.
        game_special_name = questions.TextInput(f'What is the name of the special name for {game}?', validator = questions.ValidateFileNameNoExt)
    elif game_special_name == "NumberOnly":
        # The user only wants a number.
        # Do nothing here, since this is an allowed string.
        pass
    else:
        # Some other value is present. Assume that this is the file name.
        # Check if any slashes are present.
        if (('/' in game_special_name) or ('\\' in game_special_name)):
            # There are slashes in the name.
            # Print the error.
            questions.PrintError(f'The value for the special name for {game} ("{game}_special_name" in settings.ini) includes a slash. The value should be a name, not a path.', system_exit = True)
        elif game_special_name.endswith('.igb'):
            # There is a file extension in the name.
            # Print the error.
            questions.PrintError(f'The value for the special name for {game} ("{game}_special_name" in settings.ini) includes a file extension. The value should not have a file extension.', system_exit = True)
        else:
            # The value has no issues.
            # Proceed
            pass
    # Return the skin number.
    return game_special_name

# This function is used to get the Advanced Texture ini setting.
def GetAdvancedTextureINIPath(config):
    # Get the setting value.
    setting_value = config['SETTINGS']['advanced_texture_ini']
    # Check the value.
    if setting_value == 'None':
        # Nothing is needed.
        # Update the value to a None string.
        setting_value = None
    elif setting_value == 'Ask':
        # It's necessary to ask about the value.
        # Ask about the value.
        setting_value = questions.PathInput('What is the path to the ini file for advanced textures?', validator = questions.PathValidator)
    else:
        # The setting is either a path or not an allowed value.
        try:
            # Check if the string can be made a path.
            setting_value = Path(setting_value)
            # Check if the path exists.
            if not(setting_value.exists()):
                # The value doesn't exist.
                # Show the error to the user.
                questions.PrintError('The value for the advanced texture ini path ("advanced_texture_ini" in settings.ini) does not exist.', system_exit = True)
        except:
            # The string cannot be made a path.
            questions.PrintError('The value for the advanced texture ini path ("advanced_texture_ini" in settings.ini) is not a recognized value.', system_exit = True)
    # Return the collected value.
    return setting_value

# This function is used to get a forced asset type.
def GetForcedAssetType(config):
    # Get the setting value.
    setting_value = config['SETTINGS']['forced_asset_type']
    # Check the value.
    if setting_value == 'None':
        # Nothing is needed.
        # Update the value to a None string.
        setting_value = None
    elif setting_value == 'Ask':
        # It's necessary to ask about the value.
        # Ask about the value.
        setting_value = questions.select(f'What asset type should the file be forced to?', asset_type_list)
    else:
        # The setting is either an asset type or not an allowed value.
        if not(setting_value in asset_type_list):
            # This is not an allowed value.
            questions.PrintError('The value for the forced asset type ("forced_asset_type" in settings.ini) is not a recognized value.', system_exit = True)
    # Return the collected value.
    return setting_value

# This function is used to get the debug status.
def GetDebugStatus(settings_dict, config):
    # Try to get the debug status.
    try:
        setting_value = config['SETTINGS']['debug_mode']
        # Set this as the value in the settings dictionary.
        settings_dict['debug_mode'] = bool_dict[setting_value]
    except:
        # The debug status was not set, so nothing is needed.
        pass
    # Return the updated settings dictionary.
    return settings_dict

# This function gets the settings for the program.
def ParseSettings(settings_file_path):
    # Check if the settings file exists.
    VerifySettingsExistence(settings_file_path)
    # Open the settings file to be able to parse its contents
    config = ReadAndConfirmSettingsStructure(settings_file_path)
    # Collect the relevant settings.
    settings_dict = GetSettings(settings_file_path, config)
    # Determine if it's necessary to print the debug information.
    if settings_dict.get('debug_mode', False) == True:
        # It's necessary to print the debug information.
        # Print the title.
        questions.PrintPlain('\n\nDebug information from settings.py:')
        questions.PrintDebug('settings_dict', settings_dict)
        questions.PrintPlain('\n\n')
    # Return the dictionary of collected settings.
    return settings_dict