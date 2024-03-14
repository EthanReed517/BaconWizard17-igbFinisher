# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Resources for this program
import resources
# To be able to copy and move files
import os.path
# To be able to parse the ini file
from configparser import ConfigParser


# ######### #
# FUNCTIONS #
# ######### #
# Define the function for getting the settings.
def parseConfig():
    # Check if the config file exists
    verifyConfigExistence()
    # Start a list to store the settings
    settings = {}
    # Get the character numbers
    for game in ["XML1", "XML2", "MUA1", "MUA2"]:
        number = characterNumberGetter(game)
        settings[game + "Num"] = number
    # Get the other settings
    setting = settingsGetter("pcOnly")
    settings["pcOnly"] = setting
    # Return the collected data
    return settings

# Define the function to check if the config file exists
def verifyConfigExistence():
    # Eternal loop until broken
    while True:
        try:
            # Check if the file exists
            assert os.path.exists("settings.ini")
            # Break out of the loop if there are no errors
            break
        except AssertionError:
            # The assertion failed (the file does not exist)
            # Print the error message
            resources.printError("settings.ini does not exist. Restore the file and try again.", False)
            # Wait for user confirmation
            resources.pressAnyKey("Press any key to try again...")

# Define the function to get the character numbers
def characterNumberGetter(game):
    # Get the name of the setting to look for
    setting = game + "Num"
    # Prepare to parse the settings
    config = ConfigParser()
    # Read the settings
    config.read('settings.ini')
    # Get the number
    number = config['Settings'][setting]
    # Check if the number is acceptable
    # Eternal loop until broken
    while True:
        try:
            # Check if the number is an acceptable number (between 0 and 255)
            assert 0 <= int(number) <= 255
            # If there are no errors, break out of the loop.
            break
        except ValueError:
            # The ValueError occurs because the input is not a number.
            # Check if the value is blank
            if ((number == "None") or (number == "Ask")):
                # The value is None or Asl, which is allowed.
                # Break out of the while statement
                break
            else:
                # The value is not a number, not "None", or not "Ask"
                # Display an error to the user so that they know that their input is not acceptable.
                resources.printError("Character number for " + str(game) + " is set to " + str(number) + ", which is not an acceptable value. Please enter an acceptable value.", False)
                # Find out what the user wants in their settings.
                valueType = resources.select("What setting do you want to use for the " + game + "number?", ["Update the settings with a permanent number", "Don't enter a number (the character is not in " + game + ")", "Ask each time an asset is processed"])
                # Determine what to do based on the settings.
                if valueType == "Update the settings with a permanent number":
                    # The user wants to enter a number.
                    # Ask the user for a number.
                    number = resources.textInput("Enter a 2 or 3 digit character number.", resources.characterNumberValidator)
                elif valueType == "Don't enter a number (the character is not in " + game + ")":
                    # The user wants to skip this number.
                    # Set the setting.
                    number = "None"
                else:
                    # The user wants to be asked each time the asset is processed.
                    # Set the setting.
                    number = "Ask"
        except AssertionError:
            # The AssertionError happens because the earlier "assert" statement failed, meaning that the value is a number but not within the acceptable range.
            resources.printError("Character number for " + str(game) + " is set to " + str(number) + ", which is not within the acceptable range (0-255). Please enter a number.", False)
            number = resources.textInput("Enter a 2 or 3 digit character number:", resources.characterNumberValidator)
    # Update the number in the settings
    config['Settings'][setting] = number
    # Write the new value to the settings
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)
    # Check if the number value is "None"
    if number == "None":
        # The number is "None"
        # Update this to a None type
        number = None
    # Return the collected value
    return number

# Define the function to get the other settings
def settingsGetter(settingName):
    # Prepare to parse the settings
    config = ConfigParser()
    # Read the settings
    config.read('settings.ini')
    # Get the general settings
    setting = config['Settings'][settingName]
    # Check if the value is acceptable
    # Eternal loop until broken
    while True:
        try:
            # Check the acceptance criteria
            assert (setting == "True") or (setting == "False")
            # break out of the loop if there are no errors
            break
        except (ValueError, AssertionError):
            # The value is not acceptable. Print an error
            resources.printError("The value for setting " + str(settingName) + " is set to " + str(setting) + ", which is not an acceptable value. It must be True or False. Please enter an acceptable value.", False)
            # Let the user pick the new option.
            choice = resources.select("Which console are you processing for?", ["All consoles", "PC only"])
            # Determine which option was picked
            if choice == "All consoles":
                # This is for all consoles
                # Set the setting to False (have to do as strings because otherwise it can't write to the ini)
                setting = "False"
            else:
                # This is for PC only
                # Set the setting to True (have to do as strings because otherwise it can't write to the ini)
                setting = "True"
    # Update the setting in the settings
    config['Settings'][settingName] = setting
    # Write the new value to the settings
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)
    # Determine what the setting is
    if setting == "True":
        # True as a string
        # Set as a bool
        settingBool = True
    else:
        # False as a string
        # Set as a bool
        settingBool = False
    # Return the collected value
    return settingBool