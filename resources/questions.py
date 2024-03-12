# ########### #
# INFORMATION #
# ########### #


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
# Define the style for success messages
successStyle = "fg:#3a96dd"

# Define the style for warning messages
warningStyle = "bold fg:#ffff00"

# Define the style for error messages
errorStyle = "bold fg:#ff0000"

# Define the style for important text messages
importantTextStyle = "bold fg:#ffffff"

# Define the style for plain text messages
plainTextStyle = "fg:#ffffff"

# Define the style for choices
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
# Define the function for printing a warning
def printSuccess(message):
    # Define the general form for printing
    questionary.print(message, style = successStyle)

# Define the function for printing a warning
def printWarning(message):
    # Define the general form for printing
    questionary.print(message, style = warningStyle)

# Define the function for printing an error
def printError(message):
    # Define the general form for printing
    questionary.print(message, style = errorStyle)

# Define the function for printing a warning
def printImportant(message):
    # Define the general form for printing
    questionary.print(message, style = plainTextStyle)

# Define the function for printing a warning
def printPlain(message):
    # Define the general form for printing
    questionary.print(message, style = None)

# Define the function to press any key to continue
def pressAnyKey(message):
    # Define the general form for this prompt
    questionary.press_any_key_to_continue(message).ask()

# Define the function for choice-based questions
def select(question, options):
    # Define the general form for asking questions
    answer = questionary.select(
        question,
        choices = options,
        pointer = ">",
        style = questionStyle
    ).ask()
    # Return the collected value
    return answer

# Define the function for choice-based questions
def selectDefault(question, options, defaultChoice):
    # Define the general form for asking questions
    answer = questionary.select(
        question,
        choices = options,
        pointer = ">",
        default = defaultChoice,
        style = questionStyle
    ).ask()
    # Return the collected value
    return answer

# Define the function for path-based questions
def path(question, validator):
    # Define the general form for asking questions
    answer = questionary.path(
        question,
        validate = validator,
        style = questionStyle
    ).ask()
    # Return the collected value
    return answer

# Define the function for confirmation questions
def confirm(question, defaultChoice):
    # Define the general form for asking questions
    answer = questionary.confirm(
        question,
        default = defaultChoice,
        style = questionStyle
    ).ask()
    # Return the collected value
    return answer

# Define the validator for the file name of unknown assets
def fileNameValidatorStart(fileName):
    if len(fileName) == 0:
        return "Please enter a file name."
    elif ".igb" in fileName:
        return "Do not include the file extension."
    elif not(os.path.exists(fileName + ".igb")):
        return "The file does not exist."
    else:
        return True

# Define the validator for the file path
def pathValidator(path):
    if len(path) == 0:
        return "Please enter a file path."
    elif os.path.exists(path) == False:
        return "Path does not exist"
    else:
        return True