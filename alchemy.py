# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import questions
# External modules
from datetime import datetime, timezone
import os.path
from os import listdir, popen, remove, system
from shutil import copy
import subprocess
from winreg import ConnectRegistry, CreateKeyEx, DeleteKey, HKEY_CURRENT_USER, KEY_READ, KEY_WRITE, OpenKey, QueryValueEx, REG_SZ, SetValueEx

# Global variables
sgOptimizer = '%IG_ROOT%\\bin\\sgOptimizer.exe'

# ######### #
# FUNCTIONS #
# ######### #
# Define the function for checking the date when Alchemy was last reset
def checkAlchemyDate(lastResetDate):
    # Split the string into the year, month, and day
    year = int(lastResetDate.split(" ")[0].split("-")[0])
    month = int(lastResetDate.split(" ")[0].split("-")[1])
    day = int(lastResetDate.split(" ")[0].split("-")[2])
    # Convert the stored date into a new datetime object
    lastResetDatetime = datetime(year, month, day, tzinfo=timezone.utc)
    # Subtract the last reset date from today's date
    diff = datetime.now(timezone.utc) - lastResetDatetime
    # Check if it's been 60 days or more
    if diff.days >= 60:
        # It's been 60 days or more, so the date is no longer valid
        validDate = False
    else:
        # It's been less than 60 days, so the date is valid
        validDate = True
    # Return whether or not the date is acceptable
    return validDate

# Define the function to reset the Alchemy evaluation
def resetAlchemy(marvelModsKeyPath):
    # Define the key that defines the evaluation
    key = "Software\\vicarious visions\\driver"
    # Try to look for the key
    try:
        # Open the key that stores the date
        marvelModsKey = OpenKey(HKEY_CURRENT_USER, marvelModsKeyPath, access=KEY_WRITE)
        # Set the date value to today's date
        SetValueEx(marvelModsKey, "last_reset", 0, REG_SZ, str(datetime.now(timezone.utc)))
        # Open the key that stores the evaluation (will error if it doesn't exist)
        k = OpenKey(HKEY_CURRENT_USER, key)
        # If no errors were raised, delete the key
        DeleteKey(HKEY_CURRENT_USER, key)
    except:
        # The key does not exist
        pass

# Define the function to reset the Alchemy evaluation
def checkAlchemyReset():
    # Define the registry key for the date
    marvelModsKeyPath = "Software\\vicarious visions\\marvel mods"
    # Try to set the date
    try:
        # Open the existing date key. If it doesn't exist, it will raise an error
        marvelModsKey = OpenKey(HKEY_CURRENT_USER, marvelModsKeyPath, access=KEY_READ)
        # Get the value of the current date. If it's not set, it will raise an error
        (lastResetDate, type) = QueryValueEx(marvelModsKey, "last_reset")
        # Check if the date is too far out
        validDate = checkAlchemyDate(lastResetDate)
        # Determine what was found
        if validDate == False:
            # The date is too far out
            # Reset the Alchemy evaluation and update the date to today's date
            resetAlchemy(marvelModsKeyPath)
    except:
        # Create the key where the value will be set
        CreateKeyEx(HKEY_CURRENT_USER, marvelModsKeyPath, access=KEY_WRITE)
        # Reset the Alchemy evaluation and update the date to today's date
        resetAlchemy(marvelModsKeyPath)

# This function checks the presence of the animation producer.
def CheckAnimationProducer():
    # Set a variable that assumes that the animation producer is not installed.
    animation_producer_ready = False
    # Start a while loop so that the program won't run until the animation producer is set up.
    while animation_producer_ready == False:
        # Verify the existence of the folder.
        if os.path.exists('Animation Producer'):
            # The folder exists
            # Verify that the exe exists
            if os.path.exists(os.path.join('Animation Producer', 'animationProducer.exe')):
                # The exe exists
                # Set a variable to check for .dll files
                dll_files = False
                # Loop through the files in the folder
                for file in listdir('Animation Producer'):
                    # Check if the file is a .dll file
                    if os.path.splitext(file)[1] == '.dll':
                        # This is a .dll file
                        # Update the variable to indicate that there are .dll files
                        dll_files = True
                # Check if any .dll files were found.
                if dll_files == True:
                    # .dll files were found. 
                    # Update the variable to break out of the loop.
                    animation_producer_ready = True
                else:
                    # No .dll files were found
                    questions.PrintError('The "Animation Producer" folder does not contain any .dll files. Please install the animation producer and try again.')
            else:
                # The exe does not exist
                questions.PrintError('"animationProducer.exe" does not exist in the "Animation Producer" folder. Please install the animation producer and try again.')
        else:
            # The folder does not exist.
            questions.PrintError('The "Animation Producer" folder does not exist. Please install the animation producer and try again.')

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