# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import questions
# External modules
import xml.etree.ElementTree as ET


# ######### #
# FUNCTIONS #
# ######### #
# Define the function for opening an xml file and getting the tree and root
def openGetTreeAndRoot(file):
    # Parse the file to get the tree
    try:
        tree = ET.parse(file)
    except:
        questions.printError(f"Failed to open {file} due to a formatting error.", False)
        tree = ET.parse(file)
    # Get the root from the tree
    root = tree.getroot()
    # Return the root for further operations
    return root