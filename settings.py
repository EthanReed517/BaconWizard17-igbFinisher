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
from configparser import ConfigParser
import os.path
from pathlib import Path, PurePath
import sys


# ######### #
# FUNCTIONS #
# ######### #    
# This function determines if the settings.ini file exists.
def VerifySettingsExistence():
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
def ReadAndConfirmSettingsStructure():
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
            questions.PrintError(f'Failed to open settings.ini due to the following error:\n\n{e}\n\nAddress the error and try again.')
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
def GetSettings():
    # Initialize a dictionary to store the settings.
    settings_dict = {}
    # Get the game-specific settings.
    settings_dict = GetGameSpecificSettings(settings_dict)
    # Get the console-specific settings.
    settings_dict = GetConsoleSpecificSettings(settings_dict)
    # Return the dictionary of settings.
    return settings_dict

# This function gets the game-specific settings.
def GetGameSpecificSettings(settings_dict):
    # Loop through the games in the series.
    for game in games_list:
        # Get the skin number for that game.
        game_number = SkinNumberGetter(game)
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
            game_path = GamePathGetter(game)
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
                game_num_XX = GetGameNumConvention(game)
                # Get the special name for this game.
                game_special_name = GetGameSpecialName(game)
        # Write the game-specific settings.
        settings_dict[f'{game}_num'] = game_number
        settings_dict[f'{game}_path'] = game_path
        settings_dict[f'{game}_num_XX'] = game_num_XX
        settings_dict[f'{game}_special_name'] = game_special_name
    # Return the dictionary of settings.
    return settings_dict

# This function is used to get skin numbers from the settings.
def SkinNumberGetter(game):
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
                    game_number = questions.TextInput(f'The first {len(game_number) - 2} digits of the skin number for {game} (\'{game}_num\' in settings.ini) are not between 00 and 255. Please enter the skin number. settings.ini will not be updated.', validator = questions.SkinNumberValidator)
            else:
                # The number is not numeric.
                # Get the correct number from the user.
                game_number = questions.TextInput(f'The skin number for {game} (\'{game}_num\' in settings.ini) is not a number. Please enter the skin number. settings.ini will not be updated.', validator = questions.SkinNumberValidator)
        else:
            # The number is not the correct length.
            # Get the correct number from the user.
            game_number = questions.TextInput(f'The skin number for {game} (\'{game}_num\' in settings.ini) is not the correct length (4 or 5 digits). Please enter the skin number. settings.ini will not be updated.', validator = questions.SkinNumberValidator)
    # Return the skin number.
    return game_number

# This function is used to get game paths from the settings.
def GamePathGetter(game):
    # Get the number from the settings.
    game_number = 0
    # Return the skin number.
    return game_number

# This function is used to get a game's numbering convention from the settings.
def GetGameNumConvention(game):
    # Get the number from the settings.
    game_number = 0
    # Return the skin number.
    return game_number

# This function is used to get a game's special asset name from the settings.
def GetGameSpecialName(game):
    # Get the number from the settings.
    game_number = 0
    # Return the skin number.
    return game_number

# This function gets the console-specific settings.
def GetConsoleSpecificSettings(settings_dict):
    # Loop through the possible consoles.
    for console in consoles_list:
        # Get the status of that console.
        console_status = GetConsoleStatus(console)
        # Write the console's status to the settings.
        settings_dict[console.replace(' ', '_')] = console_status
    # Return the dictionary of settings.
    return settings_dict

# This function is used to get the status of a console from the settings.
def GetConsoleStatus(game):
    # Get the number from the settings.
    game_number = 0
    # Return the skin number.
    return game_number

# This function gets the remaining settings.
def GetRemainingSettings(settings_dict):
    # Set up a list of True/False settings and their descriptions.
    true_false_settings_list = [
        ['big_texture', 'Does this model need to keep large textures at full size for less powerful consoles? Only choose Yes if this is a large character like Galactus or if this is a map.', 'whether or not this model needs to keep large textures at full size for less poweful consoles.', False],
        ['secondary_skin', 'If processing a skin, will this be a secondary skin?', 'whether or not this is a secondary skin (if processing a skin).', False],
        ['PSP_PNG4', 'Use PNG4 textures with PSP 3D assets?', 'whether or not PSP 3D assets should use PNG4 textures.', False],
        ['untextured_okay', 'If processing a 3D model and no texture is found, is it okay to proceed?', 'whether or not it\'s okay to proceed if an 3D model has no textures.', True],
        ['generate_collision', 'For other models, generate collision? Choose Yes for maps and map models, choose No for boltons.', 'whether or not collision should be generated for other models.', False],
        ['igBlend_to_igAlpha_transparency', 'If a transparent texture is detected, should igBlendStateAttr/igBlendFunctionAttr be converted to igAlphaStateAttr/igAlphaFunctionAttr?', 'whether or not igBlendStateAttr/igBlendFunctionAttr should be converted to igAlphaStateAttr/igAlphaFunctionAttr.', True]
    ]
    # Loop through the True/False settings.
    for true_false_setting in true_false_settings_list:
        # Get the value for this setting.
        true_false_setting_value = GetTrueFalseSettingValue(true_false_setting)
        # Write this setting value to the settings.
        settings_dict[true_false_setting[0]] = true_false_setting_value
    # Return the dictionary of settings.
    return settings_dict

# ############## #
# MAIN EXECUTION #
# ############## #
# Get the execution path by first checking if there is a frozen attribute for the system.
if getattr(sys, 'frozen', False):
    # There is a frozen attribute, so this is running as the compiled exe.
    # Get the path to the exe's folder.
    application_path  = Path(('/').join(Path(sys.executable).parts[0:-1]))
else:
    # There is no frozen attribute, so this is not compiled.
    # Get the path to the main python file's folder.
    application_path = Path(('/').join(Path(__file__).resolve().parts[0:-1]))
# Set the path to the settings file.
settings_file_path = application_path / 'settings.ini'
# Create a list of the games and consoles so that they can be a global variable and don't need to be written each time.
games_list = ['XML1', 'XML2', 'MUA1', 'MUA2']
consoles_list = ['PC', 'Steam', 'GameCube', 'PS2', 'PS3', 'PSP', 'Wii', 'Xbox', 'Xbox 360']
# Check if the settings file exists.
VerifySettingsExistence()
# Open the settings ifle to be able to parse its contents
config = ReadAndConfirmSettingsStructure()
# Collect the relevant settings.
settings = GetSettings()