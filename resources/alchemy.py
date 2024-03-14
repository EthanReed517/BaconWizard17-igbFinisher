# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
import resources
# To be able to call Alchemy and expand paths
import os
# To be able to edit the registry
from winreg import *
# To be able to run the Alchemy processes to completion
import subprocess

# Global variables
sgOptimizer = '%IG_ROOT%\\bin\\sgOptimizer.exe'

# ######### #
# FUNCTIONS #
# ######### #
# Define the function to reset the Alchemy evaluation
def resetAlchemy():
    # Define the registry key
    key = "Software\\vicarious visions\\driver"
    # Try to look for the key
    try:
        # Connect the key to the current computer (None)
        reg = ConnectRegistry(None, HKEY_CURRENT_USER)
        # Try to open the key
        k = OpenKey(reg, key)
        # If no errors were brought up previously, then the key exists and can be deleted
        DeleteKey(reg, key)
    except:
        # The key does not exist
        pass

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

# Define the function for performing Alchemy operations
def callAlchemy(file_name, ini_name, run_alchemy_choice):
    # Determine if the operation should be run
    if run_alchemy_choice == True:
        # Need to run Alchemy
        # Determine if the file actually exists
        if not(file_name == None):
            # There is a file
            # Define the Alchemy ini file & command
            ini_file = os.path.abspath("Scripts/" + ini_name)
            cmd = f'"{sgOptimizer}" "{file_name}" "{file_name}" "{ini_file}"'
            # Call the operation
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)