# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Resources for this program
import resources
# To be able to copy and move files
import os
# To be able to copy files
import shutil
# To be able to edit the registry
from winreg import *


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
        # This block has to exist so I'm just going to have it do something random
        hi = None

# Define the function for performing Alchemy operations
def callAlchemy(fileName, iniName, runAlchemyChoice):
    # Determine if the operation should be run
    if runAlchemyChoice == True:
        # Need to run Alchemy
        # Determine if the file actually exists
        if not(fileName == None):
            # There is a file
            # Copy the Alchemy ini file
            shutil.copy("Scripts/" + iniName, "./")
            # Call the operation
            os.system("%IG_ROOT%\\bin\\sgOptimizer.exe \"" + fileName + "\" \"" + fileName + "\" " + iniName)
            # Make sure that the ini file still exists
            if os.path.isfile(iniName):
                # The file exists
                # Delete it
                os.remove(iniName)