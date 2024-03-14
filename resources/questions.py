# ########### #
# INFORMATION #
# ########### #
# This module is used to implement the Questionary module into igbFinisher. It abbreviates many of the Questionary operations to keep styling consistent and limit options to needed ones only.


# ####### #
# IMPORTS #
# ####### #
# To be able to create command line list questions
import questionary
# Necessary functions for asking questions
from questionary import prompt, Style, Validator, ValidationError


# ###### #
# STYLES #
# ###### #
# This style is used with success messages.
successStyle = "fg:#3a96dd"

# This style is used with warning messages.
warningStyle = "bold fg:#ffff00"

# This style is used with error messages.
errorStyle = "bold fg:#ff0000"

# This style is used for any important text.
importantTextStyle = "bold fg:#ffffff"

# This style is used for plain text.
plainTextStyle = "fg:#ffffff"

# This style is used with any question that has choices.
questionStyle = Style([
    ('qmark', 'fg:#3a96dd bold'),
    ('question', 'bold'),
    ('answer', 'fg:#3a96dd bold'),
    ('pointer', 'fg:#3a96dd bold'),
    ('highlighted', 'fg:#3a96dd bold underline'),
    ('instruction', ''),
    ('text', ''),
    ('disabled', 'fg:#858585 italic')
])


# ######### #
# FUNCTIONS #
# ######### #
# Define the function for printing a success message.
def printSuccess(message):
    # Print the message for the user to see.
    questionary.print(message, style = successStyle)

# Define the function for printing a warning message.
def printWarning(message):
    # Update the message string with a "Warning: " prefix so that I don't have to add this to every single warning prompt.
    message = "Warning: " + message
    # Print the message for the user to see.
    questionary.print(message, style = warningStyle)
    # Pause to allow the user to see the warning and acknowledge it.
    pressAnyKey("Press any key to acknowledge this warning and proceed")

# Define the function for printing an error message.
def printError(message, contactCreator):
    # Update the message string with an "ERROR: " prefix so that I don't have to add this to every single warning prompt.
    message = "ERROR: " + message
    # Determine if the user needs to contact me because of the error.
    if contactCreator == True:
        # The user needs to contact me because of the error.
        # Determine if the error string doesn't end in a period.
        if not(message[-2:] == ". "):
            # The message doesn't end in a period.
            # Add a period for consistent styling.
            message += ". "
        # Add the message to contact the creator about the error.
        message += "Please contact the program creator to report this error."
    # Print the message for the user to see.
    questionary.print(message, style = errorStyle)
    # Pause to allow the user to see the error and acknowledge it.
    pressAnyKey("Press any key to acknowledge this error and proceed")

# Define the function for printing important text.
def printImportant(message):
    # Print the message for the user to see.
    questionary.print(message, style = plainTextStyle)

# Define the function for printing a warning
def printPlain(message):
    # Define the general form for printing
    questionary.print(message, style = None)

# Define the function to display a message for the user to press any key to continue.
def pressAnyKey(message):
    # Determine if the message is not a None type (None type displays the default message, "Press any key to continue. . .").
    if not(message == None):
        # The message is not a None type, meaning that it's custom.
        # Determine if the message does not end in ellipses, which should be present at the end for style consistency.
        if not(message[-5:] == ". . ."):
            # The message does not end in ellipses.
            # Determine if the message ends in a period, which is not needed for the format.
            if message[-1] == ".":
                # The message ends in a period and should not.
                # Trim the message to take off the period.
                message = message[0:-1]
            # Add the ellipses to the end of the message.
            message += ". . ."
    # Display the prompt.
    questionary.press_any_key_to_continue(message).ask()

# Define the function that will display a question with choices.
def select(question, options):
    # Pose the question to the user.
    answer = questionary.select(
        question,
        choices = options,
        pointer = ">",
        style = questionStyle
    ).ask()
    # Return the collected answer.
    return answer

# Define the function that will display a questionn with choices and a default option.
def selectDefault(question, options, defaultChoice):
    # Pose the question to the user.
    answer = questionary.select(
        question,
        choices = options,
        pointer = ">",
        default = defaultChoice,
        style = questionStyle
    ).ask()
    # Return the collected answer.
    return answer

# Define the function for asking questions to get a file path.
def path(question, validator):
    # Pose the question to the user.
    answer = questionary.path(
        question,
        validate = validator,
        style = questionStyle
    ).ask()
    # Return the collected answer.
    return answer

# Define the function for confirmation questions.
def confirm(question, defaultChoice):
    # Pose the question to the user.
    answer = questionary.confirm(
        question,
        default = defaultChoice,
        style = questionStyle
    ).ask()
    # Return the collected answer.
    return answer

# Define the validator for the file name of assets that aren't recognized by igbFinisher.
def fileNameValidatorStart(fileName):
    if len(fileName) == 0:
        return "Please enter a file name."
    elif ".igb" in fileName:
        return "Do not include the file extension."
    elif not(os.path.exists(fileName + ".igb")):
        return "The file does not exist."
    else:
        return True

# Define the validator for the destination file paths of assets.
def pathValidator(path):
    if len(path) == 0:
        return "Please enter a file path."
    elif os.path.exists(path) == False:
        return "Path does not exist"
    else:
        return True