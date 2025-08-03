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
    # Start a loop that won't end until it's broken.
    while True:
        try:
            # Check if the settings file exists.
            assert settings_file_path.exists()
            # If there are no errors in the previous line, this line will be reached, breaking out of the loop.
            break
        except AssertionError:
            # The assertion failed (the file does not exist).
            # Print the error message.
            questions.PrintError('settings.ini does not exist. Restore the file and try again.')

# This function reads the settings file and verifies its integrity. It does not pull or verify values.
def ReadAndConfirmSettingsStructure(settings_file_path):
    # Set up the config parser class.
    config = ConfigParser()
    # Create a while loop that won't end until it's broken.
    while True:
        try:
            # Read the settings file.
            config.read(settings_file_path)
            # If there are no errors in the previous line, this line will be reached, breaking out of the loop.
            break
        except Exception as e:
            # The file could not be read.
            # Print the error message.
            questions.PrintError(f'Failed to open settings.ini. Address the error and try again.', error_text = e)
    # Create another while loop that won't end until it's broken.
    # Set up the disctionary of sections and keys.
    section_key_dict = {
        'CHARACTER': ['XML1_num', 'XML2_num', 'MUA1_num', 'MUA2_num', 'XML1_path', 'XML2_path', 'MUA1_path', 'MUA2_path'],
        'ASSET': ['XML1_num_xx', 'XML2_num_XX', 'MUA1_num_XX', 'MUA2_num_XX', 'XML1_special_name', 'XML2_special_name', 'MUA1_special_name', 'MUA2_special_name'],
        'CONSOLES': consoles_list,
        'SETTINGS': ['big_texture', 'secondary_skin', 'cel_other_model', 'PSP_PNG4', 'untextured_okay', 'generate_collision', 'igBlend_to_igAlpha_transparency', 'skip_subfolder', 'advanced_texture_ini']
    }
    # Set up a variable to track error status. Assume there's an error to start to be able to get into the loop.
    is_error = True
    # Start a while loop that will go until there are no errors.
    while is_error == True:
        # Read the settings file again just to account for any changes.
        config.read(settings_file_path)
        # Set that there are no errors so that any true errors can be captured.
        is_error = False
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
                    questions.PrintError(f'Error when accessing key {e} in section \'{section}\' of settings.ini. Address the error and try again.')
            except Exception as e:
                # The section could not be accessed.
                # Print the error message.
                questions.PrintError(f'Error when accessing section {e} in settings.ini. Address the error and try again.')
                # Set the error state.
                is_error = True
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
    settings_dict['cel_other_model'] = GetTrueFalseAskSetting(config, 'SETTINGS', 'cel_other_model', 'if this is an Other model that can have cel shading', 'If this is an Other model, can it have cel shading?', True)
    settings_dict['PSP_PNG4'] = GetTrueFalseAskSetting(config, 'SETTINGS', 'PSP_PNG4', 'if PSP 3D assets should use PNG4 textures', 'Should PSP 3D assets use PNG4 textures?', False)
    settings_dict['untextured_okay'] = GetTrueFalseAskSetting(config, 'SETTINGS', 'untextured_okay', 'if it\'s okay for 3D assets to lack textures', 'Is it okay if 3D assets lack textures?', False)
    settings_dict['generate_collision'] = GetTrueFalseAskSetting(config, 'SETTINGS', 'generate_collision', 'if collision should be generated for Other models', 'Should collision be generated for Other models?', False)
    settings_dict['igBlend_to_igAlpha_transparency'] = GetTrueFalseAskSetting(config, 'SETTINGS', 'igBlend_to_igAlpha_transparency', 'if igBlendStateAttr/igBlendFunctionAttr attributes should be converted to igAlphaStateAttr/igAlphaFunctionAttr attributes in transparent models', 'Should igBlendStateAttr/igBlendFunctionAttr attributes be converted to igAlphaStateAttr/igAlphaFunctionAttr attributes in transparent models?', False)
    settings_dict['skip_subfolder'] = GetTrueFalseAskSetting(config, 'SETTINGS', 'skip_subfolder', 'if subfolders should be skipped for the resulting model', 'Should subfolders be skipped for the resulting model?', False)
    settings_dict['advanced_texture_ini'] = GetAdvancedTextureINIPath(config)
    # Return the dictionary of settings.
    return settings_dict

# This function is used to get skin numbers from the settings.
def SkinNumberGetter(config, game):
    # Get the number from the settings.
    game_number = config['CHARACTER'][f'{game}_num']
    # Set a variable to track if the number is valid and begin by assuming that it's not.
    is_valid = False
    # Start a while loop to get the number.
    while is_valid == False:
        # Check if the number is the correct length.
        if ((len(game_number) == 4) or (len(game_number) == 5)):
            # The length of the number is correct.
            # Check if the number is numeric.
            if game_number.isnumeric():
                # The number is numeric.
                # Check if the character number is between 00 and 255.
                if ((int(game_number[0:-2]) >= 0) and (int(game_number[0:-2]) <= 255)):
                    # The number is between 00 and 255.
                    # The number is correct. Set that it is valid.
                    is_valid = True
                else:
                    # The number is not between 00 and 255.
                    # Get the correct number from the user.
                    game_number = questions.TextInput(f'The first {len(game_number) - 2} digits of the skin number for {game} ("{game}_num" in settings.ini) are not between 00 and 255. Please enter the skin number. settings.ini will not be updated.', validator = questions.SkinNumberValidator)
            else:
                # The number is not numeric.
                # Get the correct number from the user.
                game_number = questions.TextInput(f'The skin number for {game} ("{game}_num" in settings.ini) is not a number. Please enter the skin number. settings.ini will not be updated.', validator = questions.SkinNumberValidator)
        else:
            # The number is not the correct length.
            # Get the correct number from the user.
            game_number = questions.TextInput(f'The skin number for {game} ("{game}_num" in settings.ini) is not the correct length (4 or 5 digits). Please enter the skin number. settings.ini will not be updated.', validator = questions.SkinNumberValidator)
    # Return the skin number.
    return game_number

# This function is used to get game paths from the settings.
def GamePathGetter(config, game):
    # Get the number from the settings.
    game_path = config['CHARACTER'][f'{game}_path']
    # Set a variable to track if the number is valid and begin by assuming that it's not.
    is_valid = False
    # Start a while loop to get the number.
    while is_valid == False:
        # Set that it's not necessary to ask about the path.
        ask_about_path = False
        # Check the path value.
        if game_path == 'Ask':
            # The user wants to be asked about the path.
            # Set that it's necessary to ask about the path.
            ask_about_path = True
        elif game_path == 'Detect':
            # This is one of the allowed strings that can stay as a string.
            # Set that the value is valid.
            is_valid = True
        elif game_path == 'None':
            # This is the None value.
            # Convert it to a None value.
            game_path = None
            # Set that the value is valid.
            is_valid = True
        else:
            # This is not one of the available strings.
            # Set a variable that assumes that the path is not okay.
            path_okay = False
            try:
                # Check if the string is a path
                game_path = Path(game_path)
                # If there are no issues in the previous step, then this can be converted to a path. Check if the path exists.
                if game_path.exists():
                    # The path exists.
                    # Say that the path is okay.
                    path_okay = True
                    # Set that the value is valid
                    is_valid = True
                else:
                    # The path does not exist.
                    # Give an error.
                    questions.PrintError(f'The path entered for {game} ("{game}_path" in settings.ini) does not exist.', skip_pause = True)
            except:
                # The path could not be made a path.
                questions.PrintError(f'The path entered for {game} ("{game}_path" in settings.ini) is not a recognized value.', skip_pause = True)
            # Check if the path was okay.
            if path_okay == False:
                # The path was not okay.
                # Ask the user what they want to do.
                do_with_path = questions.Select(f'What would you like to do for the path for {game}? This will not update settings.ini', ['Enter a new path', 'Skip exporting for this game', 'Use folder detection'])
                # Check what the user selected.
                if do_with_path == 'Skip exporting for this game':
                    # The user wanted to skip.
                    # Set no path.
                    game_path = None
                    # Set that the value is valid.
                    is_valid = True
                elif do_with_path == 'Use folder detection':
                    # The user wants to use folder detection.
                    # Set the value.
                    game_path = 'Detect'
                    # Set that the value is valid.
                    is_valid = True
                else:
                    # The user wanted to enter a new path.
                    # Set that the path should be asked about.
                    ask_about_path = True
        # Check if it's necessary to ask about the path.
        if ask_about_path == True:
            # It's necessary to ask about the path.
            # Get the path from the user.
            game_path = questions.PathInput(f'What path should be used for {game}?', validator = questions.PathValidator)
            # The path is being validated by the validator, so it will definitely pass.
            is_valid = True
    # Return the skin number.
    return game_path

# This function is used to get the value from a settings whose options are True, False, and Ask.
def GetTrueFalseAskSetting(config, section, key, setting_name, question_string, default_setting):
    # Get the numbering convention from the settings.
    setting_value = config[section][key]
    # Set that it's necessary to ask about the value.
    ask_about_value = True
    # Check the possible values.
    if setting_value in ['True', 'False']:
        # The value is a boolean.
        # Convert it to a boolean.
        setting_value = bool_dict[setting_value]
        # Set that it's not necessary to ask about the value.
        ask_about_value = False
    elif ask_about_value == 'Ask':
        # The user wants to be asked about the value.
        # Do nothing here
        pass
    else:
        # The value is something else.
        # Give an error.
        questions.PrintError(f'The value for {setting_name} ("{key}" in settings.ini) is not a recognized value. Please enter a correct value. This will not update settings.ini', skip_pause = True)
    # Determine if it's necessary to ask.
    if ask_about_value == True:
        # It's necessary to ask.
        # Ask about the setting.
        setting_value = questions.Confirm(question_string, default_choice = default_setting)
    # Return the collected setting.
    return setting_value

# This function is used to get a game's special asset name from the settings.
def GetGameSpecialName(config, game):
    # Get the special name from the settings.
    game_special_name = config['ASSET'][f'{game}_special_name']
    # Set a variable to track if the user should be asked. Assume no at first.
    ask_about_value = False
    # Check what was found.
    if game_special_name == "None":
        # No special name is needed.
        # Update this to a None type.
        game_special_name = None
    elif game_special_name == "Ask":
        # The user wants to be asked.
        # Set that it's necessary to ask.
        ask_about_value = True
    elif game_special_name == "NumberOnly":
        # The user only wants a number.
        # Do nothing here.
        pass
    else:
        # Some other value is present. Assume that this is the file name.
        # Check if any slashes are present.
        if (('/' in game_special_name) or ('\\' in game_special_name)):
            # There are slashes in the name.
            # Print the error.
            questions.PrintError(f'The value for the special name for {game} ("{game}_special_name" in settings.ini) includes a slash. The value should be a name, not a path. Please enter the name. This will not update settings.ini.', skip_pause = True)
            # Set that it's necessary to ask.
            ask_about_value = True
        elif game_special_name.endswith('.igb'):
            # There is a file extension in the name.
            # Print the error.
            questions.PrintError(f'The value for the special name for {game} ("{game}_special_name" in settings.ini) includes a file extension. The value should not have a file extension. Please enter the name. This will not update settings.ini.', skip_pause = True)
            # Set that it's necessary to ask.
            ask_about_value = True
        else:
            # The value has no issues.
            # Proceed
            pass
    # Check if it's necessary to ask about the value.
    if ask_about_value == True:
        # It's necessary to ask.
        # Present the question.
        game_special_name = questions.TextInput(f'What is the name of the special name for {game}?', validator = questions.ValidateFileNameNoExt)
    # Return the skin number.
    return game_special_name

# This function is used to get the Advanced Texture ini setting.
def GetAdvancedTextureINIPath(config):
    # Get the setting value.
    setting_value = config['SETTINGS']['advanced_texture_ini']
    # Assume that the value should not be asked about.
    ask_about_value = False
    # Check the value.
    if setting_value == 'None':
        # Nothing is needed.
        # Update the value to a None string.
        setting_value = None
    elif setting_value == 'Ask':
        # It's necessary to ask about the value.
        # Set that the value should be asked about.
        ask_about_value = True
    else:
        # The setting is either a path or not an allowed value.
        try:
            # Check if the string can be made a path.
            setting_value = Path(setting_value)
            # Check if the path exists.
            if not(setting_value.exists()):
                # The value doesn't exist.
                # Show the error to the user.
                questions.PrintError('The value for the advanced texture ini path ("advanced_texture_ini" in settings.ini) does not exist. Please enter a path. This will not update settings.ini.', skip_pause = True)
                # Set that it's necessary to ask about the path.
                ask_about_value = True
        except:
            # The string cannot be made a path.
            questions.PrintError('The value for the advanced texture ini path ("advanced_texture_ini" in settings.ini) is not a recognized value.', skip_pause = True)
            # See what the user wants to do.
            what_to_do = questions.Select('What would you like to do? This will not update settings.ini.', ['Do not use advanced textures', 'Enter the path to an advanced texture ini file'])
            # See what the user picked.
            if what_to_do == 'Do not use advanced textures':
                # The user does not want to use advanced textures.
                # Set the value to None.
                setting_value = None
            else:
                # The user wants to enter the path to advanced textures.
                # Set that the path needs to be asked about.
                ask_about_value = True
    # Determine if it's necessary to ask about the path.
    if ask_about_value == True:
        # It's necessary to ask.
        setting_value = questions.PathInput('What is the path to the ini file for advanced textures?', validator = questions.PathValidator)
    # Return the collected value.
    return setting_value

# This function gets the settings for the program.
def ParseSettings(settings_file_path):
    # Check if the settings file exists.
    VerifySettingsExistence(settings_file_path)
    # Open the settings file to be able to parse its contents
    config = ReadAndConfirmSettingsStructure(settings_file_path)
    # Collect the relevant settings.
    settings_dict = GetSettings(settings_file_path, config)

    '''
    print('DEBUG: settings_dict = {')
    for key, value in settings_dict.items():
        print(f"    '{key}': {value}")
    print('}')
    '''