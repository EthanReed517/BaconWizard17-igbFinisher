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
# To be able to parse the ini file
import configparser


# ######### #
# FUNCTIONS #
# ######### #
# Define the function for getting the settings.
def parseConfig():
    # Check if the config file exists
    verifyConfigExistence()
    # Start a list to store the settings
    settings = []
    # Get the character numbers
    for game in ["XML1", "XML2", "MUA1", "MUA2"]:
        number = characterNumberGetter(game)
        settings.append(number)
    # Get the other settings
    for settingName in ["hexEditChoice","runAlchemyChoice","multiPose"]:
        setting = settingsGetter(settingName)
        settings.append(setting)
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
            resources.printError("ERROR: settings.ini does not exist. Restore the file and try again.")
            # Wait for user confirmation
            resources.pressAnyKey("Press any key to try again...")

# Define the function to get the character numbers
def characterNumberGetter(game):
    # Get the name of the setting to look for
    setting = game + "Num"
    # Prepare to parse the settings
    config = configparser.ConfigParser()
    # Read the settings
    config.read('settings.ini')
    # Get the number
    number = config['Settings'][setting]
    # Check if the number is acceptable
    # Eternal loop until broken
    while True:
        try:
            # Check the acceptance criteria
            assert 0 <= int(number) <= 255
            # break out of the loop if there are no errors
            break
        except ValueError:
            # The value is not a number
            # Check if the value is blank
            if number == "":
                # The value is blank, which is allowed.
                # Break out of the while statement
                break
            else:
                # The value is not blank
                # Get a new use input
                resources.printError("ERROR: Character number for " + str(game) + " is set to " + str(number) + ", which is not a number. Please enter a number.")
                number = input("Enter a new value: ")
        except AssertionError:
            # The number is not within the accepted range (assertion failed)
            resources.printError("ERROR: Character number for " + str(game) + " is set to " + str(number) + ", which is not within the acceptable range (0-255). Please enter a number.")
            number = input("Enter a new value: ")
    # Update the number in the settings
    config['Settings'][setting] = number
    # Write the new value to the settings
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)
    # Return the collected value
    return number

# Define the function to get the other settings
def settingsGetter(settingName):
    # Prepare to parse the settings
    config = configparser.ConfigParser()
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
            # The value is not acceptable
            resources.printError("ERROR: The value for setting " + str(settingName) + " is set to " + str(setting) + ", which is not an acceptable value. It must be True or False. Please enter an acceptable value.")
            setting = input("Enter a new value: ")
    # Update the setting in the settings
    config['Settings'][settingName] = setting
    # Write the new value to the settings
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)
    # Return the collected value
    return setting