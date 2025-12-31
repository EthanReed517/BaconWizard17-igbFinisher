# ########### #
# INFORMATION #
# ########### #
# This module is the main function for igbFinisher that the rest of the program runs on.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import alchemy
import asset_recognition
import hex
import questions
import processing
import settings
import textures
# External modules
from os import environ, listdir, remove, system
from pathlib import Path
import sys
from time import sleep


# ######### #
# FUNCTIONS #
# ######### #
# This function displays the command prompt information.
def DisplayInfo():
    # Display the title.
    questions.PrintPlain('██╗ ██████╗ ██████╗ ███████╗██╗███╗   ██╗██╗███████╗██╗  ██╗███████╗██████╗ ')
    questions.PrintPlain('██║██╔════╝ ██╔══██╗██╔════╝██║████╗  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗')
    questions.PrintPlain('██║██║  ███╗██████╔╝█████╗  ██║██╔██╗ ██║██║███████╗███████║█████╗  ██████╔╝')
    questions.PrintPlain('██║██║   ██║██╔══██╗██╔══╝  ██║██║╚██╗██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗')
    questions.PrintPlain('██║╚██████╔╝██████╔╝██║     ██║██║ ╚████║██║███████║██║  ██║███████╗██║  ██║')
    questions.PrintPlain('╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝')
    # Print the relevant information.
    questions.PrintPlain('\nVersion 4.0.0')
    questions.PrintPlain('https://marvelmods.com/forum/index.php/topic,11440.0.html\n')
    # Print the welcome message.
    questions.PrintImportant("Welcome to BaconWizard17's igb Finisher!\n")

# This function gets the application path.
def GetApplicationPath():
    # Get the execution path by first checking if there is a frozen attribute for the system.
    if getattr(sys, 'frozen', False):
        # There is a frozen attribute, so this is running as the compiled exe.
        # Get the path to the exe's folder.
        application_path = Path(sys.executable).parent
    else:
        # There is no frozen attribute, so this is not compiled.
        # Get the path to the main python file's folder.
        application_path = Path(__file__).parent
    # Return the collected path
    return application_path


# ############## #
# MAIN EXECUTION #
# ############## #
# Set the window title.
system('title BaconWizard17\'s igb Finisher')
# Print the welcome information.
DisplayInfo()
# Get the application path.
application_path = GetApplicationPath()
# Check for the Alchemy installation. This also checks the last reset date.
alchemy.CheckAlchemyStatus()
# Get and process the arguments.
(input_file_path, settings_file_path) = settings.ProcessArguments(application_path)
# Read the settings.
settings_dict = settings.ParseSettings(settings_file_path)
# Get the asset type.
asset_type, settings_dict = asset_recognition.AssetRecognition(input_file_path, settings_dict)
# Get the texture information from the model.
settings_dict, hex_out_list, texture_info_dict = textures.GetTextureInfo(application_path, input_file_path, settings_dict, asset_type)
# Get the geometry information from the model.
geometry_list, has_cel, settings_dict = alchemy.GetModelStats(input_file_path, asset_type, settings_dict)
# Set up the dictionary of processes by game.
game_console_process_dict = {
    'XML1': [processing.ProcessXboxAsset, processing.ProcessPS2Asset, processing.ProcessGCAsset],
    'XML2': [processing.ProcessXboxAsset, processing.ProcessPS2Asset, processing.ProcessGCAsset, processing.ProcessPSPAsset],
    'MUA1': [processing.ProcessPC360Asset, processing.ProcessSteamPS3Asset, processing.ProcessWiiAsset, processing.ProcessXboxAsset, processing.ProcessPS2Asset, processing.ProcessPSPAsset],
    'MUA2': [processing.ProcessWiiAsset, processing.ProcessPS2Asset, processing.ProcessPSPAsset]
}
# Set up the dictionary of operations for getting the output name by asset type.
output_name_process_dict = {
    'Skin': processing.SetUpSkinName,
    'Mannequin': processing.SetUpMannequinName,
    '3D Head': processing.SetUp3DHeadName,
    'Conversation Portrait': processing.SetUpHUDName,
    'Character Select Portrait': processing.SetUpCSPName,
    'Loading Screen': processing.SetUpLoadingName
}
# Determine if this is a skin.
if asset_type == 'Skin':
    # This is a skin.
    # Set up the temp file as an animation DB.
    temp_file_path = alchemy.CreateAnimDB(input_file_path)
else:
    # This is another file.
    # Set up the temp file as a copy.
    temp_file_path = alchemy.SetUpTempFile(input_file_path)
# Announce that processing is beginning.
questions.PrintImportant(f'Processing {input_file_path.name} . . .')
# Loop through the games.
for game in settings.games_list:
    # Determine if the game is in use.
    if ((settings_dict[f'{game}_num'] is not None) and (settings_dict[f'{game}_path'] is not None)):
        # The game is in use.
        # Announce the status.
        questions.PrintImportant(f'Processing for {game} . . .')
        # Set up the output file name. Anything that gets its full name from the special name uses the same function.
        try:
            output_file_name = output_name_process_dict[asset_type](settings_dict, game, has_cel)
        except KeyError:
            output_file_name = processing.SetUpSpecialName(settings_dict, game, has_cel)
        # Hex edit the file.
        temp_file_hexed_path = hex.HexEdit(temp_file_path, 'Skin', hex_out_list, texture_info_dict, geometry_list, game, settings_dict)
        # Loop through the possible functions for the game.
        for console_process in game_console_process_dict[game]:
            # Perform the processing.
            console_process(asset_type, temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel)
        # Delete the hex edited file.
        remove(temp_file_hexed_path)
# Delete the temp file.
remove(temp_file_path)
# Announce completion.
questions.PrintSuccess(f'{input_file_path.name} processed successfully.')
# Wait for 1 second so the user can see the success message.
sleep(1)
# Determine if debug mode is in use.
if settings_dict.get('debug_mode', False) == True:
    # Debug mode is in use.
    # Determine if the user wants to delete the temp files.
    delete_temp = questions.Confirm('Delete the debug temp files?')
    # If the user wants to, delete all the debug temp files.
    if delete_temp == True:
        for file in listdir(Path(environ['temp'])):
            if ((file.startswith('opt')) or (file.startswith('temp - '))):
                if (Path(environ['temp']) / file).is_file():
                    remove(Path(environ['temp']) / file)
    # Pause the program.
    questions.PressAnyKey(None)