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
from os import environ, listdir, makedirs, popen, remove, rename, system
from pathlib import Path
from shutil import copy
import subprocess
from winreg import ConnectRegistry, CreateKeyEx, DeleteKey, HKEY_CURRENT_USER, KEY_READ, KEY_WRITE, OpenKey, QueryValueEx, REG_SZ, SetValueEx


# ################ #
# GLOBAL VARIABLES #
# ################ #
# This is the path to sgOptimizer in Alchemy 3.2.
SG_OPTIMIZER_32 = '%IG_ROOT%\\bin32\\sgOptimizer.exe'
# This is the path to sgOptimizer in Alchemy 5.
SG_OPTIMIZER = '%IG_ROOT%\\bin\\sgOptimizer.exe'
# This is the path to the key that stores the last Alchemy reset date.
MARVEL_MODS_KEY_PATH = 'Software\\Vicarious Visions\\Marvel Mods'
# This is the list of files in ALchemy 3.2 (not all of them, just some important ones that are hopefully a big enough sample size).
ALCHEMY_32_FILES_LIST = [
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
    # Convert the stored date into a new datetime object and subtract from today's date.
    last_reset_datetime = datetime.fromisoformat(last_reset_date)
    diff = datetime.now(timezone.utc) - last_reset_datetime
    # The evaluation period is still valid if it's been less than 60 days.
    if diff.days >= 60:
        valid_date = False
    else:
        valid_date = True
    return valid_date

# This function is used to reset the Alchemy evaluation.
def ResetAlchemy():
    # This key defines the evaluation.
    key = 'Software\\Vicarious Visions\\Driver'
    try:
        # Open the key that stores the date and set the value to today's date.
        marvel_mods_key = OpenKey(HKEY_CURRENT_USER, MARVEL_MODS_KEY_PATH, access=KEY_WRITE)
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
    try:
        # Open the existing date key. If it doesn't exist, it will raise an error.
        marvel_mods_key = OpenKey(HKEY_CURRENT_USER, MARVEL_MODS_KEY_PATH, access=KEY_READ)
        # Get the value of the current date. If it's not set, it will raise an error.
        (last_reset_date, type) = QueryValueEx(marvel_mods_key, 'last_reset')
        # Check if the date is too far out and reset if needed.
        valid_date = CheckAlchemyDate(last_reset_date)
        if valid_date == False:
            ResetAlchemy()
    except:
        # Create the key where the date value will be set.
        CreateKeyEx(HKEY_CURRENT_USER, MARVEL_MODS_KEY_PATH, access=KEY_WRITE)
        # Reset the Alchemy evaluation and update the date to today's date.
        ResetAlchemy()

# This function checks for the existence of Alchemy.
def CheckAlchemyStatus():
    # Try to get the IG_ROOT environment variable. Abort if not found.
    try:
        environ['IG_ROOT']
    except KeyError:
        questions.PrintError('Alchemy 5 is not properly installed. Please properly install Alchemy 5 and try again.', system_exit = True)
    # Check if the Alchemy 3.2 folder exists and verify its files. Error if any files or folders are missing.
    alchemy_32_folder = Path(environ['IG_ROOT']) / 'bin32'
    if alchemy_32_folder.exists():
        # Check through the list of Alchemy 3.2 files to make sure that they exist.
        for file in ALCHEMY_32_FILES_LIST:
            if not((alchemy_32_folder / file).exists()):
                questions.PrintError(f'{file} is missing from {alchemy_32_folder}. Please properly install Alchemy 3.2 and try again.', system_exit = True)
        # For Alchemy 3.2, the necessary dll files must also exist, either in the Alchemy 3.2 folder or in SysWOW64.
        for file in ['msvcp70.dll', 'msvcr70.dll']:
            if not((alchemy_32_folder / file).exists()):
                if not((Path('C:\\Windows\\SysWOW64') / file).exists()):
                    questions.PrintError(f'{file} could not be found in either {alchemy_32_folder} or C:\\Windows\\SysWOW64. The file should have been included in the Alchemy 3.2 download. Please properly install Alchemy 3.2 and try again.')
    else:
        questions.PrintError(f'There is no "bin32" folder in the Alchemy 5 installation ({environ['IG_ROOT']}). Please properly install Alchemy 3.2 and try again.', system_exit = True)
    # Check the Alchemy reset date.
    CheckAlchemyReset()

# This function gets information about the model's textures.
def GetTextureInfo(file_name) -> list:
    # Write the optimization and the command and call it.
    optimizations.WriteOptimization(['igStatisticsTexture'])
    cmd = f'"{SG_OPTIMIZER}" "{file_name}" "%temp%\\tex_out.igb" "{Path(environ['temp']) / 'opt.ini'}"'
    output = popen(cmd).read()
    # Initialize a list of textures.
    textures_list = []
    # Run through the lines in the return and collect the necessary information.
    for texture in output.split('\n'):
        texture_dict = {}
        if texture.find('IG_GFX_TEXTURE_FORMAT_') > 0:
            texture_dict['Name'] = Path(texture.split('^|')[0].rstrip())
            texture_dict['Width'] = int(texture.split('^|')[1])
            texture_dict['Height'] = int(texture.split('^|')[2])
            texture_dict['Format'] = texture.split('^|')[3].rstrip()
            texture_dict['Type'] = texture.split('^|')[4].rstrip()
            textures_list.append(texture_dict)
    # Delete the temp file.
    if (Path(environ['temp']) / 'tex_out.igb').exists():
        remove(Path(environ['temp']) / 'tex_out.igb')
    return textures_list

# This function gets information about the model's geometry.
def GetModelStats(input_file_path, asset_type, settings_dict):
    # Write the optimization and the command and call it.
    optimizations.WriteOptimization(['igStatisticsGeometry'])
    cmd = f'"{SG_OPTIMIZER}" "{input_file_path}" "%temp%\\model_out.igb" "{Path(environ['temp']) / 'opt.ini'}"'
    output = popen(cmd).read()
    # Initialize a list to store the geometry information.
    geometry_list = []
    # Run the optimization and isolate the model names.
    for geometry in output.split('\n'):
        if geometry.find('igGeometryAttr') > 0:
            geometry_list.append((geometry.split('^|'))[0].rstrip())
    # Initialize a variable to check for cel shading (assume none).
    has_cel = False
    # Loop through the geometry entries to check for cel shading.
    for geometry in geometry_list:
        if '_outline' in geometry:
            has_cel = True
            # MUA1 and MUA2 do not use cel shading and will be skipped.
            settings_dict['MUA1_num'] = None
            settings_dict['MUA2_num'] = None
            settings_dict['MUA1_path'] = None
            settings_dict['MUA2_path'] = None
    # Make sure this is an asset that can have cel shading and give an error if not.
    if ((asset_type in ['Conversation Portrait', 'Character Select Portrait', 'Power Icons', 'Comic Cover', 'Concept Art', 'Loading Screen']) and (has_cel == True)):
        questions.PrintError(f'Assets of type {asset_type} cannot use cel shading, but cel shading was detected.', system_exit = True)
    # Determine if this is an other model and update the name to remove the no cel descriptor for MUA.
    if asset_type == 'Other':
        for game in ['MUA1', 'MUA2']:
            if settings_dict[f'{game}_special_name'] is not None:
                if ' - No Cel' in settings_dict[f'{game}_special_name']:
                    settings_dict[f'{game}_special_name'].replace(' - No Cel', '')
    # Print the debug information if needed.
    if settings_dict.get('debug_mode', False) == True:
        questions.PrintPlain('\n\nDebug information from GetModelStats in alchemy.py:')
        questions.PrintDebug('settings_dict', settings_dict)
        questions.PrintDebug('geometry_list', geometry_list)
        questions.PrintDebug('has_cel', has_cel)
        questions.PrintPlain('\n\n')
    # Delete the temp file.
    if (Path(environ['temp']) / 'model_out.igb').exists():
        remove(Path(environ['temp']) / 'model_out.igb')
    return geometry_list, has_cel, settings_dict

# This function is used to create a proper anim DB for a skin.
def CreateAnimDB(input_file_path):
    # Set up the paths to the animation producer.
    animation_producer_folder = Path(environ['IG_ROOT']) / 'bin32'
    temp_anim_producer_file = animation_producer_folder / 'temp.igb'
    animation_producer_txt_path = animation_producer_folder / 'temp.txt'
    temp_skin_path = Path(environ['TEMP']) / 'temp.igb'
    # Copy the input file to the animation producer folder.
    copy(input_file_path, temp_anim_producer_file)
    # Write the text file.
    with open(animation_producer_txt_path, 'w') as file:
        file.write('create_animation_database 12301\nload_actor temp.igb\nextract_skeleton igActor01Skeleton\nextract_skin igActor01Appearance\nsave_external_animation_database temp.igb')
    # Call the process for the animation producer.
    subprocess.run('@animationProducer.exe temp.txt', shell=True, stdout=subprocess.DEVNULL, cwd=animation_producer_folder, stderr=subprocess.STDOUT)
    # Copy the new file to the temp directory for further processing.
    copy(temp_anim_producer_file, temp_skin_path)
    # Delete the lingering files.
    remove(temp_anim_producer_file)
    remove(animation_producer_txt_path)
    return temp_skin_path

# This function is used to set up a non-skin asset as a temp file.
def SetUpTempFile(input_file_path):
    # Set up a dummy optimization so that the asset is processed through Alchemy 3.2. This slightly reduces the file size.
    optimizations.WriteOptimization(['igResizeImage'], alchemy_version = 'Alchemy 3.2', scale_to = 1.0)
    # Set up the output path as the temp folder and perform the optimization.
    temp_file_path = Path(environ['TEMP']) / 'temp.igb'
    CallAlchemy(input_file_path, alchemy_version = 'Alchemy 3.2', output_path = temp_file_path)
    return temp_file_path

# This function performs Alchemy optimizations on a file.
def CallAlchemy(input_file_path, **kwargs):
    # Set up the Alchemy version as a variable for convenience.
    alchemy_version = kwargs.get('alchemy_version', 'Alchemy 5')
    # Get the correct optimizer.
    if alchemy_version == 'Alchemy 3.2':
        optimizer_path = SG_OPTIMIZER_32
    else:
        optimizer_path = SG_OPTIMIZER 
    # Set up a unique output path for the optimization if needed.
    if kwargs.get('output_path', None) is not None:
        output_file_path = kwargs['output_path']
        makedirs(output_file_path.parent, exist_ok = True)
    else:
        output_file_path = input_file_path
    # Set up the optimization paths as a variable for convenience.
    optimization_path = kwargs.get('optimization_path', (Path(environ['temp']) / 'opt.ini'))
    # Set up paths to the other possible path types to be able to delete/rename them later.
    optimization_path2 = Path(environ['temp']) / 'opt2.ini'
    temp_txt_path = Path(environ['temp']) / 'temp.txt'
    # Set up the Alchemy command and run it.
    cmd = f'"{optimizer_path}" "{input_file_path}" "{output_file_path}" "{optimization_path}"'
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    # If debug mode is active, create copies of the files at the specific state. Otherwise, clean up.
    if kwargs.get('debug_mode', False) == True:
        console = kwargs.get('console', 'none')
        time_stamp = str(datetime.now(timezone.utc)).replace(':', '-')
        rename(optimization_path, (Path(environ['temp']) / f'{optimization_path.stem} - {console} - {alchemy_version} - {time_stamp}.ini'))
        copy(output_file_path, (Path(environ['temp']) / f'{output_file_path.stem} - {console} - {alchemy_version} - {time_stamp}.igb'))
        if not(output_file_path == input_file_path):
            copy(input_file_path, (Path(environ['temp']) / f'{input_file_path.stem} - {console} - {alchemy_version} - {time_stamp}.igb'))
        for file in [optimization_path2, temp_txt_path]:
            if file.exists():
                rename(file, (Path(environ['temp']) / f'{file.stem} - {console} - {alchemy_version} - {time_stamp}.{file.suffix}'))
    else:
        remove(optimization_path)
        for file in [optimization_path2, temp_txt_path]:
            if file.exists():
                remove(file)

# This function cleans up the debug files in the temp directory.
def CleanUpDebugTemp(settings_dict):
    if settings_dict.get('debug_mode', False) == True:
        delete_temp = questions.Confirm('Delete the debug temp files?')
        # If the user wants to, delete all the debug temp files.
        if delete_temp == True:
            for file in listdir(Path(environ['temp'])):
                if ((file.startswith('opt')) or (file.startswith('temp - ')) or (file.endswith('.igb'))):
                    if (Path(environ['temp']) / file).is_file():
                        remove(Path(environ['temp']) / file)
        # Pause the program.
        questions.PressAnyKey(None)