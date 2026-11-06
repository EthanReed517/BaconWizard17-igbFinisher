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


# ################ #
# GLOBAL VARIABLES #
# ################ #
# The app version.
__version__ = '4.1.1'


# ######### #
# FUNCTIONS #
# ######### #
# This function displays the command prompt information.
def DisplayInfo():
    questions.PrintPlain('██╗ ██████╗ ██████╗ ███████╗██╗███╗   ██╗██╗███████╗██╗  ██╗███████╗██████╗ ')
    questions.PrintPlain('██║██╔════╝ ██╔══██╗██╔════╝██║████╗  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗')
    questions.PrintPlain('██║██║  ███╗██████╔╝█████╗  ██║██╔██╗ ██║██║███████╗███████║█████╗  ██████╔╝')
    questions.PrintPlain('██║██║   ██║██╔══██╗██╔══╝  ██║██║╚██╗██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗')
    questions.PrintPlain('██║╚██████╔╝██████╔╝██║     ██║██║ ╚████║██║███████║██║  ██║███████╗██║  ██║')
    questions.PrintPlain('╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝')
    questions.PrintPlain(f'\nVersion v{__version__}')
    questions.PrintPlain('https://marvelmods.com/forum/index.php/topic,11440.0.html\n')
    questions.PrintImportant("Welcome to BaconWizard17's igb Finisher!\n")

# This function gets the application path to check if it's running as a .exe or .py.
def GetApplicationPath():
    if getattr(sys, 'frozen', False):
        # There is a frozen attribute, so this is running as the compiled exe.
        application_path = Path(sys.executable).parent
    else:
        application_path = Path(__file__).parent
    return application_path


# ############## #
# MAIN EXECUTION #
# ############## #
if __name__ == '__main__':
    # Set the window title and display welcome info.
    system('title BaconWizard17\'s igb Finisher')
    DisplayInfo()
    # Perform initial checks and gather information.
    application_path = GetApplicationPath()
    alchemy.CheckAlchemyStatus()
    (input_file_path, settings_file_path) = settings.ProcessArguments(application_path)
    settings_dict = settings.ParseSettings(settings_file_path)
    # Get the asset type.
    asset_type, settings_dict = asset_recognition.AssetRecognition(input_file_path, settings_dict)
    # Get information from the model.
    settings_dict, hex_out_list, texture_info_dict = textures.GetTextureInfo(application_path, input_file_path, settings_dict, asset_type)
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
    # Set up temp files. Skins need their temp file set up as an animation DB, otherwise it's a copy.
    if asset_type == 'Skin':
        temp_file_path = alchemy.CreateAnimDB(input_file_path)
    else:
        temp_file_path = alchemy.SetUpTempFile(input_file_path)
    # Begin processing for each game if it is in use.
    questions.PrintImportant(f'Processing {input_file_path.name} . . .')
    for game in settings.games_list:
        if ((settings_dict[f'{game}_num'] is not None) and (settings_dict[f'{game}_path'] is not None)):
            questions.PrintImportant(f'Processing for {game} . . .')
            # Set up the output file name. Anything that gets its full name from the special name uses the same function.
            try:
                output_file_name = output_name_process_dict[asset_type](settings_dict, game, has_cel)
            except KeyError:
                output_file_name = processing.SetUpSpecialName(input_file_path, settings_dict, game, has_cel)
            # Hex edit and process the file.
            temp_file_hexed_path = hex.HexEdit(temp_file_path, 'Skin', hex_out_list, texture_info_dict, geometry_list, game, settings_dict)
            for console_process in game_console_process_dict[game]:
                console_process(asset_type, temp_file_hexed_path, output_file_name, settings_dict, texture_info_dict, game, has_cel)
            # Delete the hex edited file.
            remove(temp_file_hexed_path)
    # Announce completion and clean up.
    remove(temp_file_path)
    questions.PrintSuccess(f'{input_file_path.name} processed successfully.')
    sleep(1)
    alchemy.CleanUpDebugTemp(settings_dict)