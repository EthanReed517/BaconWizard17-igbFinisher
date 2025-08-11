# ########### #
# INFORMATION #
# ########### #
# THis module is used to automate the various alchemy processes.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import optimizations
import questions
# External modules
from datetime import datetime, timezone
from os import environ, listdir, makedirs, popen, remove, system
from pathlib import Path
from shutil import copy
import subprocess
from winreg import ConnectRegistry, CreateKeyEx, DeleteKey, HKEY_CURRENT_USER, KEY_READ, KEY_WRITE, OpenKey, QueryValueEx, REG_SZ, SetValueEx


# ################ #
# Global variables #
# ################ #
# This is the path to sgOptimizer in Alchemy 3.2.
sgOptimizer32 = '%IG_ROOT%\\bin32\\sgOptimizer.exe'
# This is the path to sgOptimizer in Alchemy 5.
sgOptimizer = '%IG_ROOT%\\bin\\sgOptimizer.exe'
# This is the list of files in ALchemy 3.2 (not all of them, just some important ones that are hopefully a big enough sample size).
alchemy_32_files_list = [
    'plugins\\optimizations\\libIGOptExtension.dll',
    'plugins\\optimizations\\libIGOptExtensionRaven.dll',
    'alchemy.ini',
    'animationProducer.exe',
    'sgOptimizer.exe'
]


# ######### #
# FUNCTIONS #
# ######### #
# This function checks when Alchemy was last reset.
def CheckAlchemyDate(last_reset_date):
    # Convert the stored date into a new datetime object.
    last_reset_datetime = datetime.fromisoformat(last_reset_date)
    # Subtract the last reset date from today's date.
    diff = datetime.now(timezone.utc) - last_reset_datetime
    # Check if it's been 60 days or more.
    if diff.days >= 60:
        # It's been 60 days or more.
        # The date is no longer valid.
        valid_date = False
    else:
        # It's been less than 60 days.
        # The date is valid
        valid_date = True
    # Return whether or not the date is acceptable.
    return valid_date

# This function is used to reset the Alchemy evaluation.
def ResetAlchemy(marvel_mods_key_path):
    # Define the key that defines the evaluation.
    key = 'Software\\Vicarious Visions\\Driver'
    # Try to look for the key.
    try:
        # Open the key that stores the date.
        marvel_mods_key = OpenKey(HKEY_CURRENT_USER, marvel_mods_key_path, access=KEY_WRITE)
        # Set the date value to today's date.
        SetValueEx(marvel_mods_key, 'last_reset', 0, REG_SZ, str(datetime.now(timezone.utc)))
        # Open the key that stores the evaluation (will error if it doesn't exist).
        k = OpenKey(HKEY_CURRENT_USER, key)
        # If no errors were raised, delete the key.
        DeleteKey(HKEY_CURRENT_USER, key)
    except:
        # The key does not exist, which means it's already been reset.
        pass

# This function checks if it's necessary to reset the Alchemy evaluation.
def CheckAlchemyReset():
    # Define the registry key for the date.
    marvel_mods_key_path = 'Software\\Vicarious Visions\\Marvel Mods'
    # Try to set the date.
    try:
        # Open the existing date key. If it doesn't exist, it will raise an error.
        marvel_mods_key = OpenKey(HKEY_CURRENT_USER, marvel_mods_key_path, access=KEY_READ)
        # Get the value of the current date. If it's not set, it will raise an error.
        (last_reset_date, type) = QueryValueEx(marvel_mods_key, 'last_reset')
        # Check if the date is too far out.
        valid_date = CheckAlchemyDate(last_reset_date)
        # Determine what was found.
        if valid_date == False:
            # The date is too far out.
            # Reset the Alchemy evaluation and update the date to today's date.
            ResetAlchemy(marvel_mods_key_path)
    except:
        # Create the key where the value will be set.
        CreateKeyEx(HKEY_CURRENT_USER, marvel_mods_key_path, access=KEY_WRITE)
        # Reset the Alchemy evaluation and update the date to today's date.
        ResetAlchemy(marvel_mods_key_path)

# This function checks for the existence of Alchemy.
def CheckAlchemyStatus():
    # Try to get the IG_ROOT environment variable.
    try:
        environ['IG_ROOT']
    except KeyError:
        # The IG_ROOT environment variable does not exist. Notify the user.
        questions.PrintError('Alchemy 5 is not properly installed. Please properly install Alchemy 5 and try again.', system_exit = True)
    # Set up the path to the Alchemy 3.2 folder.
    alchemy_32_folder = Path(environ['IG_ROOT']) / 'bin32'
    # Check if the Alchemy 3.2 folder exists.
    if alchemy_32_folder.exists():
        # The path exists.
        # Check through the list of Alchemy 3.2 files.
        for file in alchemy_32_files_list:
            # Check if the file exists.
            if not((alchemy_32_folder / file).exists()):
                # The necessary file doesn't exist.
                # Give an Error.
                questions.PrintError(f'{file} is missing from {alchemy_32_folder}. Please properly install Alchemy 3.2 and try again.', system_exit = True)
        for file in ['msvcp70.dll', 'msvcr70.dll']:
            # Check if the file exists in the Alchemy 3.2 folder.
            if not((alchemy_32_folder / file).exists()):
                # The necessary file doesn't exist in the Alchemy 3.2 folder.
                # Check if the file exists in the SysWOW64 folder.
                if not((Path('C:\\Windows\\SysWOW64') / file).exists()):
                    # The necessary file doesn't exist in the SysWOW64 folder either.
                    # Give an error.
                    questions.PrintError(f'{file} could not be found in either {alchemy_32_folder} or C:\\Windows\\SysWOW64. The file should have been included in the Alchemy 3.2 download. Please properly install Alchemy 3.2 and try again.')
    else:
        # The path doesn't exist.
        # Give an error.
        questions.PrintError(f'There is no "bin32" folder in the Alchemy 5 installation ({environ['IG_ROOT']}). Please properly install Alchemy 3.2 and try again.', system_exit = True)
    # Check the Alchemy reset date.
    CheckAlchemyReset()

def GetTextureInfo(file_name) -> list:
    # Write the optimization.
    optimizations.WriteOptimization(['igStatisticsTexture'])
    # Write the command.
    cmd = f'"{sgOptimizer}" "{file_name}" "%temp%\\temp.igb" "{Path(environ['temp']) / 'opt.ini'}"'
    # Call the command.
    output = popen(cmd).read()
    # Initialize a list of textures.
    textures_list = []
    # Run through the lines in the return.
    for texture in output.split('\n'):
        # Initialize a dictionary for this line.
        texture_dict = {}
        # Check if a format is found.
        if texture.find('IG_GFX_TEXTURE_FORMAT_') > 0:
            # If a texture exists, it's listed with a texture format.
            # Add the necessary information to the dictionary.
            texture_dict['Name'] = Path(texture.split('^|')[0].rstrip())
            texture_dict['Width'] = int(texture.split('^|')[1])
            texture_dict['Height'] = int(texture.split('^|')[2])
            texture_dict['Format'] = texture.split('^|')[3].rstrip()
            texture_dict['Type'] = texture.split('^|')[4].rstrip()
            textures_list.append(texture_dict)
    # Return the collected texture information.
    return textures_list

def GetModelStats(input_file_path, asset_type, settings_dict):
    # Write the optimization.
    optimizations.WriteOptimization(['igStatisticsGeometry'])
    # Write the command.
    cmd = f'"{sgOptimizer}" "{input_file_path}" "%temp%\\temp.igb" "{Path(environ['temp']) / 'opt.ini'}"'
    # Call the command.
    output = popen(cmd).read()
    # Initialize a list to store the geometry information.
    geometry_list = []
    # Run the optimization and isolate the model names
    for geometry in output.split('\n'):
        if geometry.find('igGeometryAttr') > 0:
            # If a model exists, it's listed with a model type
            # Append the path from the same line (first listed)
            geometry_list.append((geometry.split('^|'))[0].rstrip())
    # Initialize a variable to check for cel shading (assume none).
    has_cel = False
    # Loop through the geometry entries.
    for geometry in geometry_list:
        # Determine if this is outline geometry.
        if '_outline' in geometry:
            # This is outline geometry.
            # Update the cel shading status.
            has_cel = True
            # Update the necessary settings.
            settings_dict['MUA1_num'] = None
            settings_dict['MUA2_num'] = None
            settings_dict['MUA1_path'] = None
            settings_dict['MUA2_path'] = None
    # Make sure this is an asset that can have cel shading.
    if asset_type in ['Conversation Portrait', 'Character Select Portrait', 'Power Icons', 'Comic Cover', 'Concept Art', 'Loading Screen']:
        # This is an asset type that doesn't support cel shading.
        # Give an error.
        questions.PrintError(f'Assets of type {asset_type} cannot use cel shading, but cel shading was detected.', system_exit = True)
    # Determine if it's necessary to print the debug information.
    if settings_dict.get('debug_mode', False) == True:
        # It's necessary to print the debug information.
        # Print the title.
        questions.PrintPlain('\n\nDebug information from GetModelStatus in alchemy.py:')
        questions.PrintDebug('settings_dict', settings_dict)
        questions.PrintDebug('geometry_list', geometry_list)
        questions.PrintDebug('has_cel', has_cel)
        questions.PrintPlain('\n\n')
    # Return all found texture paths
    return geometry_list, has_cel, settings_dict

# This function is used to create a proper anim DB for a skin.
def CreateAnimDB(temp_file, num):
    # Copy the temp file to the animation producer folder
    copy(temp_file, 'Animation Producer')
    # Write the text file for this skin
    with open(os.path.join('Animation Producer', 'remove.txt'), 'w') as file:
        file.write(f'create_animation_database {num}\nload_actor temp.igb\nextract_skeleton igActor01Skeleton\nextract_skin igActor01Appearance\nsave_external_animation_database temp.igb')
    # Get the absolute paths for the command
    anim_producer_folder = os.path.abspath('Animation Producer')
    # Call the process for the animation producer
    subprocess.run('@animationProducer.exe remove.txt', shell=True, stdout=subprocess.DEVNULL, cwd=anim_producer_folder, stderr=subprocess.STDOUT)
    # Copy the temp file back for further processing
    copy(os.path.join('Animation Producer', 'temp.igb'), temp_file)
    # Delete the text file
    remove(os.path.join('Animation Producer', 'remove.txt'))

# This function performs Alchemy optimizations on a file.
def CallAlchemy(input_file_path, **kwargs):
    # Get the correct optimizer.
    if kwargs.get('alchemy_version', 'Alchemy 5') == 'Alchemy 3.2':
        optimizer_path = sgOptimizer32
    else:
        optimizer_path = sgOptimizer
    # Determine if an output path was given.
    if kwargs.get('output_path', None) is not None:
        # An output path was given.
        # Set up the output path.
        output_file_path = kwargs['output_path']
        # Set up the output folder.
        makedirs(output_file_path.parent, exist_ok = True)
    else:
        # There is no special output path.
        # The output path is just the input path.
        output_file_path = input_file_path
    # Set up the Alchemy command.
    cmd = f'"{optimizer_path}" "{input_file_path}" "{output_file_path}" "{kwargs.get('optimization_path', (Path(environ['temp']) / 'opt.ini'))}"'
    # Call the operation.
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    # Delete the optimization path.
    remove(kwargs.get('optimization_path', (Path(environ['temp']) / 'opt.ini')))