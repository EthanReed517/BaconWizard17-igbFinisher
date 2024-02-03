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


# ######### #
# FUNCTIONS #
# ######### #
# Define the function to check if XVI32 was installed
def verifyXVI32Existence():
    # Eternal loop until broken
    while True:
        try:
            # Check if the file exists
            assert os.path.exists("XVI32")
            # Break out of the loop if there are no errors
            break
        except AssertionError:
            # The assertion failed (the file does not exist)
            # Print the error message
            resources.printError("ERROR: folder \"XVI32\" does not exist. Install XVI32 and try again.")
            # Wait for user confirmation
            resources.pressAnyKey("Press any key to try again...")
    # Eternal loop until broken
    while True:
        try:
            # Check if the file exists
            assert os.path.exists("XVI32\\XVI32.exe")
            # Break out of the loop if there are no errors
            break
        except AssertionError:
            # The assertion failed (the file does not exist)
            # Print the error message
            resources.printError("ERROR: XVI32.exe does not exist in the \"XVI32\". Install XVI32 and try again.")
            # Wait for user confirmation
            resources.pressAnyKey("Press any key to try again...")