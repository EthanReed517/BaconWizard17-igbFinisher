# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import questions
# External modules
import os.path
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
        settings[f"{game}Num"] = number
    # Get the path settings
    for series, gameNames in zip(["XML", "MUA"], [("XML1", "XML2"), ("MUA1", "MUA2")]):
        path = pathGetter(series, gameNames[0], gameNames[1])
        settings[f"{series}Path"] = path
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
            questions.printError("settings.ini does not exist. Restore the file and try again.", False)
            # Wait for user confirmation
            questions.pressAnyKey("Press any key to try again...")

# Define the function to get the character numbers
def characterNumberGetter(game):
    # Get the name of the setting to look for
    setting = f"{game}Num"
    # Prepare to parse the settings
    config = ConfigParser()
    # Read the settings
    config.read('settings.ini')
    # Get the number
    number = config['Settings'][setting]
    # Eternal loop until broken
    while True:
        # Check if the number is a number
        if number.isnumeric() == True:
            # The number is a number
            # Check if the number is the correct length (4-5 digits in length)
            if 4 <= len(number) <= 5:
                # The number is the correct length
                # Check if the character number is between 00 and 255
                if ((0 <= int(number[0:-2])) and (int(number[0:-2]) <= 255)):
                    # The character number is between 00 and 255
                    # The skin number is acceptable, so break out of the loop.
                    break
                else:
                    # The character number is not acceptable
                    # Give the error to let the user know
                    questions.printError(f"The skin number for {game} is set to {number}. The character number (first 2-3 digits) must be between 00 and 255. Please enter a new number.", False)
                    # Get the user input
                    number = questions.textInput("Enter a 4 or 5 digit skin number:", questions.skinNumberValidator)
            else:
                # The number is not the correct length
                # Give the error to let the user know.
                questions.printError(f"The skin number for {game} is set to {number}. Skin numbers must be 4 or 5 digits long. Please enter a new number.", False)
                # Get the user input
                number = questions.textInput("Enter a 4 or 5 digit skin number:", questions.skinNumberValidator)
        else:
            # The number is not a number
            # Check if the number ends in XX
            if ((number[0:-2].isnumeric() == True) and (number[-2:] == "XX")):
                # The number is a 2-3 digit number followed by "XX", which is allowed
                # Break out of the while statement
                break
            # Check if the value is one of the accepted non-numbers
            elif ((number == "None") or (number == "Ask")):
                # The value is None or Ask, which is allowed.
                # Break out of the while statement
                break
            else:
                # The value is not a number, "None", or "Ask".
                # Display an error to the user so that they know that their input is not acceptable.
                questions.printError(f"The skin number for {game} is set to {number}, which is not an acceptable value. Please enter an acceptable value.", False)
                # Find out what the user wants in their settings.
                valueType = questions.select(f"What setting do you want to use for the {game}number?", ["Update the settings with a permanent number", f"Don't enter a number (the character is not in {game})", "Ask each time an asset is processed"])
                # Determine what to do based on the settings.
                if valueType == "Update the settings with a permanent number":
                    # The user wants to enter a number.
                    # Ask the user for a number.
                    number = questions.textInput("Enter a 2 or 3 digit character number.", questions.skinNumberValidator)
                elif valueType == f"Don't enter a number (the character is not in {game})":
                    # The user wants to skip this number.
                    # Set the setting.
                    number = "None"
                else:
                    # The user wants to be asked each time the asset is processed.
                    # Set the setting.
                    number = "Ask"
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

# Define the function for getting path settings
def pathGetter(series, game1Name, game2Name):
    # Get the name of the setting to look for
    setting = f"{series}Path"
    # Prepare to parse the settings
    config = ConfigParser()
    # Read the settings
    config.read('settings.ini')
    # Get the path
    path = config['Settings'][setting]
    # Get the numbers
    game1Num = config['Settings'][f"{game1Name}Num"]
    game2Num = config['Settings'][f"{game2Name}Num"]
    # Determine which games are in use
    if (game1Num == "None") and (game2Num == "None"):
        # Neither game is in use
        path = "None"
    else:
        # At least one game is in use
        if game1Num is not None:
            # Game 1 is in use
            if game2Num is not None:
                # Game 1 and Game 2 are in use
                games = f"{game1Name}/{game2Name}"
            else:
                # Only Game 1 is in use
                games = game1Name
        else:
            # Only Game 2 is in use
            games = game2Name
        # Check if the path is acceptable
        # Eternal loop until broken
        while True:
            try:
                # Check if the path exists
                assert os.path.exists(path)
                # If there are no errors, break out of the loop.
                break            
            except AssertionError:
                # The AssertionError happens because the earlier "assert" statement failed, meaning that the path doesn't exist.
                # Check if the option is "Ask", which is also allowed.
                if path in ["Ask", "Detect", "None"]:
                    # The path is one of the acceptable non-path values
                    # Break out of the loop.
                    break
                else:
                    # The value is not ask or an existing file path, so something went wrong.
                    questions.printError(f"The value for the path for {games} is set to {path}, which is not an acceptable value. Please decide what you'd like the value to be.", False)
                    # Find out what the user wants in their settings.
                    valueType = questions.select(f"What setting do you want to use for the path for {games}?", ["Update the settings with a permanent path", "Detect the output path using the model's texture path.", f"Don't enter a number (the character is not in {games})", "Ask each time an asset is processed"])
                    if valueType == "Update the settings with a permanent path":
                        # The user wants to write a new path to the settings.
                        # Create the message for the prompt
                        message = f"Enter the path to the folder for the {games} release:"
                        # Ask the question
                        path = questions.path(message, questions.pathValidator)
                    elif valueType == "Detect the output path using the model's texture path.":
                        # The user wants to detect paths from the model's texture folder
                        path = "Detect"
                    elif valueType == f"Don't enter a number (the character is not in {games})":
                        # The user wants to skip this series.
                        # Set the setting.
                        path = "None"
                    else:
                        # The user wants to be asked each time.
                        # Set the setting.
                        path = "Ask"
        # Determine if a path was entered
        if not(path in ["Ask", "Detect", "None"]):
            # A path was entered
            # Replace any incorrect slashes
            path = path.replace("\\", "/")
        # Update the path in the settings
        config['Settings'][setting] = path
        # Write the new value to the settings
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
    # Check if the number value is "None"
    if path == "None":
        # The number is "None"
        # Update this to a None type
        path = None
    # Return the collected value
    return path    

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
            questions.printError(f"The value for setting {settingName} is set to {setting}, which is not an acceptable value. It must be True or False. Please enter an acceptable value.", False)
            # Let the user pick the new option.
            choice = questions.select("Which console are you processing for?", ["All consoles", "PC only"])
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