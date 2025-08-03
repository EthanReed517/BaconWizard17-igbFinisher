# ########### #
# INFORMATION #
# ########### #
# THis module is used to automate the various alchemy processes.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import questions
# External modules
from datetime import datetime, timezone
import os.path
from os import environ, listdir, popen, remove, system
from pathlib import Path
from shutil import copy
import subprocess
from winreg import ConnectRegistry, CreateKeyEx, DeleteKey, HKEY_CURRENT_USER, KEY_READ, KEY_WRITE, OpenKey, QueryValueEx, REG_SZ, SetValueEx


# ################ #
# Global variables #
# ################ #
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
    # Split the string into the year, month, and day.
    year = int(last_reset_date.split(' ')[0].split('-')[0])
    month = int(last_reset_date.split(' ')[0].split('-')[1])
    day = int(last_reset_date.split(' ')[0].split('-')[2])
    # Convert the stored date into a new datetime object.
    last_reset_datetime = datetime(year, month, day, tzinfo=timezone.utc)
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
        os.environ['IG_ROOT']
    except KeyError:
        # The IG_ROOT environment variable does not exist. Notify the user.
        questions.PrintError('Alchemy 5 is not properly installed. Please properly install Alchemy 5 and try again.', system_exit = True)
    # Set up the path to the Alchemy 3.2 folder.
    alchemy_32_folder = Path(os.environ['IG_ROOT']) / 'bin32'
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
        questions.PrintError(f'There is no "bin32" folder in the Alchemy 5 installation ({os.environ['IG_ROOT']}). Please properly install Alchemy 3.2 and try again.', system_exit = True)
    # Check the Alchemy reset date.
    CheckAlchemyReset()

def GetTexPath(file_name) -> list:
    # Define the Alchemy ini file & command
    ini_file = os.path.abspath("Scripts/statsT.ini")
    cmd = f'"{sgOptimizer}" "{file_name}" "%temp%\\temp.igb" "{ini_file}"'
    output = os.popen(cmd).read()
    # Initialize the return list as an empty list
    texturePaths = []
    textureFormats = []
    # Run the optimization and isolate the texture paths 
    for l in output.split('\n'):
        if l.find('IG_GFX_TEXTURE_FORMAT_') > 0:
            # If a texture exists, it's listed with a texture format
            # Append the path from the same line (first listed)
            texturePaths.append((l.split('^|'))[0])
            textureFormats.append((l.split('^|'))[1])
    # Return all found texture paths
    return texturePaths, textureFormats

def GetModelStats(file_name) -> list:
    # Define the Alchemy ini file & command
    ini_file = os.path.abspath("Scripts/statsM.ini")
    cmd = f'"{sgOptimizer}" "{file_name}" "%temp%\\temp.igb" "{ini_file}"'
    output = os.popen(cmd).read()
    # Initialize the return list as an empty list
    geometryNames = []
    # Run the optimization and isolate the model names
    for l in output.split('\n'):
        if l.find('igGeometryAttr') > 0:
            # If a model exists, it's listed with a model type
            # Append the path from the same line (first listed)
            geometryNames.append((l.split('^|'))[0])
    # Return all found texture paths
    return geometryNames

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

# Define the function for performing Alchemy operations
def callAlchemy(file_name, ini_name):
    # Determine if the file actually exists
    if file_name is not None:
        # There is a file
        # Define the Alchemy ini file & command
        ini_file = os.path.abspath("Scripts/" + ini_name)
        cmd = f'"{sgOptimizer}" "{file_name}" "{file_name}" "{ini_file}"'
        # Call the operation
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)