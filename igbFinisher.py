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
import questions
import processing
import settings
import textures
# External modules
from os import system
from pathlib import Path
import sys


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
    questions.PrintPlain('\nVersion 3.1.0')
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
# Read the settings
settings_dict = settings.ParseSettings(settings_file_path)
# Get the asset type.
asset_type, settings_dict = asset_recognition.AssetRecognition(input_file_path, settings_dict)
# Get the texture information from the model.
settings_dict, hex_out_list, texture_info_dict = textures.GetTextureInfo(application_path, input_file_path, settings_dict, asset_type)
# Get the geometry information from the model.
geometry_list, has_cel, settings_dict = alchemy.GetModelStats(input_file_path, asset_type, settings_dict)