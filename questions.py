# ########### #
# INFORMATION #
# ########### #
# This module is used to implement the Questionary module into igbFinisher. It abbreviates many of the Questionary operations to keep styling consistent and limit options to needed ones only.


# ####### #
# IMPORTS #
# ####### #
# External modules
import questionary
from questionary import prompt, Style, Validator, ValidationError
from pathlib import Path


# ###### #
# STYLES #
# ###### #
# This style is used with success messages.
success_style = 'fg:#3a96dd'

# This style is used with warning messages.
warning_style = 'bold fg:#ffff00'

# This style is used with error messages.
error_style = 'bold fg:#ff0000'

# This style is used for any important text.
important_text_style = 'bold fg:#ffffff'

# This style is used for plain text.
plain_text_style = 'fg:#ffffff'

# This style is used with any question that has choices.
question_style = Style([
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
# This function prints plain text without formatting.
def PrintPlain(message):
    # Print the message.
    questionary.print(message, style = None)

# This function prints important text, like a title.
def PrintImportant(message):
    # Print the message for the user to see.
    questionary.print(message, style = plain_text_style)

# This function prints a success message.
def PrintSuccess(message, **kwargs):
    # Print the message for the user to see.
    questionary.print(message, style = success_style)
    # Determine if it's necessary to pause before proceeding.
    if kwargs.get('pause', False) == True:
        # It's necessary to pause.
        # Add the pause.
        PressAnyKey(None)

# This function prints a warning message.
def PrintWarning(message, **kwargs):
    # Update the message string with a "Warning: " prefix so that I don't have to add this to every single warning prompt.
    message = f'Warning: {message}'
    # Print the message for the user to see.
    questionary.print(message, style = warning_style)
    # Determine if it's necessary to pause before proceeding. The default is that it is necessary.
    if kwargs.get('skip_pause', False) == False:
        # The pause cannot be skipped.
        # Pause to allow the user to see the warning and acknowledge it.
        PressAnyKey("Press any key to acknowledge this warning and proceed")

# This function prints an error message.
def PrintError(message, **kwargs):
    # Update the message string with an "ERROR: " prefix so that I don't have to add this to every single warning prompt.
    message = f'ERROR: {message}'
    # Determine if the user needs to contact me because of the error.
    if kwargs.get('contact_creator', False) == True:
        # The user needs to contact me because of the error.
        # Place the period accordingly
        if message.endswith('. '):
            # The message already ends with the correct period style, so it's not necessary to add a period or space.
            # Pass through this statement.
            pass
        elif message.endswith('.'):
            # The message ends with a period but not a space.
            # Add a space at the end for proper grammar.
            message += ' '
        else:
            # The message does not end with a period or a space.
            # Add both a period and a space.
            message += '. '
        # Add the message to contact the creator about the error.
        message += 'Please contact the program creator to report this error.'
    # Print the message for the user to see.
    questionary.print(message, style = error_style)
    # Determine if it's necessary to pause before proceeding. The default is that it is necessary.
    if kwargs.get('skip_pause', False) == False:
        # The pause cannot be skipped.
        # Pause to allow the user to see the error and acknowledge it.
        PressAnyKey("Press any key to acknowledge this error and proceed")

# This function gives the user a prompt to press any key to continue.
def PressAnyKey(message):
    # Determine if the message is a None type (None type displays the default message, "Press any key to continue. . .").
    if message is not None:
        # The message is not a None type, meaning that it's custom.
        # Determine if the message ends in ellipses, which should be present at the end for style consistency.
        if not(message.endswith('. . .')):
            # The message does not end in ellipses.
            # Determine if the message ends with spaceless elipses, which is the incorrect style.
            if message.endswith('...'):
                # The message ends with spaceless elipses.
                # Remove them.
                message.replace('...', '')
            # Determine if the message ends in a period, which is not needed for this format.
            if message.endswith('.'):
                # The message ends in a period and should not.
                # Trim the message to take off the period.
                message = message[0:-1]
            # Add the ellipses to the end of the message.
            message += '. . .'
    # Display the prompt.
    questionary.press_any_key_to_continue(message).ask()

# This function displays a question with choices.
def Select(question, options, **kwargs):
    # Pose the question to the user.
    answer = questionary.select(
        question,
        choices = options,
        pointer = '>',
        style = question_style,
        default = kwargs.get('default_choice', None)
    ).ask()
    # Return the collected answer.
    return answer

# This function allows the user to input text.
def TextInput(question, **kwargs):
    # Pose the question to the user.
    answer = questionary.text(
        question,
        style = question_style,
        default = kwargs.get('default_choice', ''),
        validate = kwargs.get('validator', None)
    ).ask()
    # Return the collected answer.
    return answer

# This function allows the user to input a file path.
def PathInput(question, **kwargs):
    # Pose the question to the user.
    answer = questionary.path(
        question,
        style = question_style,
        default = kwargs.get('default_choice', ''),
        validate = kwargs.get('validator', None)
    ).ask()
    # Return the collected answer.
    return answer

# This function asks a confirmation question.
def Confirm(question, **kwargs):
    # Pose the question to the user.
    answer = questionary.confirm(
        question,
        style = question_style,
        default = kwargs.get('default_choice', None)
    ).ask()
    # Return the collected answer.
    return answer

# This function validates a user entering a skin number.
def SkinNumberValidator(number):
    if len(number) == 0:
        return 'Please enter a number.'
    elif number.isnumeric() == False:
        return 'The skin number must be a number.'
    elif ((len(number) > 5) or (len(number) < 4)):
        return 'Skin numbers must be 4 or 5 digits long.'        
    elif not(0 <= int(number[0:-2]) <= 255):
        return 'The character number of the skin number (first 2-3 digits) must be between 00 and 255 (inclusive).'
    else:
        return True

# This function validates a user entering a file path.
def PathValidator(path):
    if len(path) == 0:
        return 'Please enter a file path.'
    elif Path(path).exists() == False:
        return 'Path does not exist'
    else:
        return True

# This function validates a user entering a file path.
def ValidateFileNameNoExt(name):
    if len(name) == 0:
        return 'Please enter a file name.'
    elif '/' in name:
        return 'Enter just a name, not a path.'
    elif '\\' in name:
        return 'Enter just a name, not a path.'
    elif name.endswith('.igb'):
        return 'Do not include a file extension.'
    else:
        return True