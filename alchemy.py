# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# External modules
from datetime import datetime, timezone
import os
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
    # Check if it's been 30 days or more
    if diff.days >= 60:
        # It's been 30 days or more, so the date is no longer valid
        validDate = False
    else:
        # It's been less than 30 days, so the date is valid
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