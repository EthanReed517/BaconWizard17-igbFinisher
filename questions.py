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
    questionary.print(message, style = None)

# This function prints important text, like a title.
def PrintImportant(message):
    questionary.print(message, style = plain_text_style)

# This function prints a success message with an optional pause.
def PrintSuccess(message, **kwargs):
    questionary.print(message, style = success_style)
    if kwargs.get('pause', False) == True:
        PressAnyKey(None)

# This function prints a warning message with a default pause that can be skipped.
def PrintWarning(message, **kwargs):
    # Update the message string with a "Warning: " prefix so that I don't have to add this to every single warning prompt.
    message = f'Warning: {message}'
    questionary.print(message, style = warning_style)
    if kwargs.get('skip_pause', False) == False:
        PressAnyKey('Press any key to acknowledge this warning and proceed')

# This function adds a period and space as needed to the end of a string.
def AddPeriod(message):
    if ((message.endswith('. ')) or (message.endswith('\n'))):
        pass
    elif message.endswith('.'):
        message += ' '
    else:
        message += '. '
    return message

# This function prints an error message.
def PrintError(message, **kwargs):
    # Update the message string with an "ERROR: " prefix so that I don't have to add this to every single warning prompt.
    message = f'ERROR: {message}'
    # Show the error text if needed.
    if kwargs.get('error_text', None) is not None:
        message = AddPeriod(message)
        message += f'Error text:\n\n{kwargs['error_text']}\n\n'
    # Add information if I need to be contacted.
    if kwargs.get('contact_creator', False) == True:
        message = AddPeriod(message)
        message += 'Please contact the program creator to report this error.'
    # Set the exit information, but don't exit yet.
    if kwargs.get('system_exit', False) == True:
        message = AddPeriod(message)
        message += 'The program will now close.'
    questionary.print(message, style = error_style)
    # Determine if it's necessary to pause before proceeding. The default is that it is necessary.
    if kwargs.get('skip_pause', False) == False:
        PressAnyKey('Press any key to acknowledge this error and proceed')
    # Exit if needed.
    if kwargs.get('system_exit', False) == True:
        raise SystemExit(1)

# This function prints a debug statement.
def PrintDebug(variable_name, variable_value, **kwargs):
    if isinstance(variable_value, dict):
        PrintPlain(f'DEBUG: {variable_name} = {{')
        for key, value in variable_value.items():
            PrintPlain(f'    {key}: {value} (type: {type(value)})')
        PrintPlain('}')
    elif isinstance(variable_value, list):
        PrintPlain(f'DEBUG: {variable_name} = [')
        for item in variable_value:
            PrintPlain(f'    {item} (type: {type(item)})')
        PrintPlain(']')
    else:
        PrintPlain(f'DEBUG: {variable_name}: {variable_value} (type: {type(variable_value)})')

# This function gives the user a prompt to press any key to continue. "None" displays the default "Press any key to continue. . ."
def PressAnyKey(message):
    if message is not None:
        # Add the appropriate type of ellipses if needed.
        if not(message.endswith('. . .')):
            if message.endswith('...'):
                message.replace('...', '')
            if message.endswith('.'):
                message = message[0:-1]
            message += '. . .'
    questionary.press_any_key_to_continue(message).ask()

# This function displays a question with choices.
def Select(question, options, **kwargs):
    answer = questionary.select(
        question,
        choices = options,
        pointer = '>',
        style = question_style,
        default = kwargs.get('default_choice', None)
    ).ask()
    return answer

# This function allows the user to input text.
def TextInput(question, **kwargs):
    answer = questionary.text(
        question,
        style = question_style,
        default = kwargs.get('default_choice', ''),
        validate = kwargs.get('validator', None)
    ).ask()
    return answer

# This function allows the user to input a file path.
def PathInput(question, **kwargs):
    answer = questionary.path(
        question,
        style = question_style,
        default = kwargs.get('default_choice', ''),
        validate = kwargs.get('validator', None)
    ).ask()
    # Convert to a pathlib Path.
    return Path(answer)

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