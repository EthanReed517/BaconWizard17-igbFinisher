# ########### #
# INFORMATION #
# ########### #
# This module is used to open and process XML files.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import questions
# External modules
from pathlib import Path
import xml.etree.ElementTree as ET


# ######### #
# FUNCTIONS #
# ######### #
# This function is used to open an xml file and get its tree and root.
def OpenGetTreeAndRoot(file):
    # Parse the file to get the tree.
    try:
        tree = ET.parse(file)
    except Exception as e:
        # There was an error when opening the file, so print an error.
        questions.PrintError(f'Failed to open {file} due to a formatting error.', error_text = e, system_exit = True)
    # Get the root from the tree
    root = tree.getroot()
    # Return the root for further operations
    return root

# This function is used to get the output path for folder detection.
def GetOutputPath(game, application_path, character, asset_type_folder, sub_folder, asset_type, settings_dict):
    # Set up the path to the xml file.
    xml_file_path = application_path / 'Folder Detection' / f'{character}.xml'
    # Check if the file exists.
    if not(xml_file_path.exists()):
        # The file doesn't exist.
        # Give an error.
        questions.PrintError(f'Folder detection detected that {character}.xml is the xml file for this asset, but this file does not exist.', system_exit = True)
    # Open the xml file and get its root.
    paths_root = OpenGetTreeAndRoot(xml_file_path)
    # Determine which dictionary should be used for the assets.
    if asset_type_folder.startswith('Default '):
        # These are my personal versions of default assets.
        # Set up the dictionary.
        elems_dict = {
            'Skin': {'parent_elem': 'd_skins', 'child_elem': 'skin'},
            'Mannequin': {'parent_elem': 'd_skins', 'child_elem': 'skin'},
            '3D Head': {'parent_elem': 'd_skins', 'child_elem': 'skin'},
            'Conversation Portrait': {'parent_elem': 'd_huds', 'child_elem': 'portrait'},
            'Character Select Portrait': {'parent_elem': 'd_csps', 'child_elem': 'portrait'},
            'Power Icons': {'parent_elem': 'd_icons', 'child_elem': 'icon'},
            'Comic Cover': {'parent_elem': 'd_covers', 'child_elem': 'cover'},
            'Concept Art': {'parent_elem': 'd_concepts', 'child_elem': 'concept'},
            'Loading Screen': {'parent_elem': 'd_lscreens', 'child_elem': 'lscreen'},
            'Other': {'parent_elem': 'd_others', 'child_elem': 'other'}
        }
    else:
        # These are standard assets.
        # Set up the dictionary.
        elems_dict = {
            'Skin': {'parent_elem': 'skins', 'child_elem': 'skin'},
            'Mannequin': {'parent_elem': 'skins', 'child_elem': 'skin'},
            '3D Head': {'parent_elem': 'skins', 'child_elem': 'skin'},
            'Conversation Portrait': {'parent_elem': 'skins', 'child_elem': 'skin'},
            'Character Select Portrait': {'parent_elem': 'skins', 'child_elem': 'skin'},
            'Power Icons': {'parent_elem': 'icons', 'child_elem': 'icon'},
            'Comic Cover': {'parent_elem': 'covers', 'child_elem': 'cover'},
            'Concept Art': {'parent_elem': 'concepts', 'child_elem': 'concept'},
            'Loading Screen': {'parent_elem': 'lscreens', 'child_elem': 'lscreen'},
            'Other': {'parent_elem': 'others', 'child_elem': 'other'}
        }
    # Find the element for the asset type.
    parent_elem = paths_root.find(elems_dict[asset_type]['parent_elem'])
    # Determine if anything was found.
    if parent_elem is None:
        # Nothing was found.
        # Give an error.
        questions.PrintError(f'{xml_file_path} does not list an element for asset type {asset_type}. The element should be {elems_dict[asset_type]['parent_elem']}.', system_exit = True)
    # Get the main path for this game's assets.
    try:
        main_path = Path(parent_elem.get(game))
    except Exception as e:
        questions.PrintError(f'Attempted to access the {game} attribute in {elems_dict[asset_type]['parent_elem']} within {xml_file_path.name} but failed.', error_text = e, system_exit = True)
    # Initialize a variable for the output subfolder
    output_subfolder = None
    # Loop through the child elements of the parent element.
    for child_elem in parent_elem.findall(elems_dict[asset_type]['child_elem']):
        # Check if the element's tex_folder attribute matches with the skin's subfolder.
        if child_elem.get('tex_folder') == sub_folder:
            # This is a match.
            # Update the output subfolder.
            output_subfolder = child_elem.get('output_folder')
    # Determine if an output folder was found.
    if output_subfolder is None:
        # Nothing was found.
        # Give an error.
        questions.PrintError(f'The detected texture folder for this asset is {sub_folder}, but there is no matching entry for this in {xml_file_path.name}.', system_exit = True)
    # Set the output path.
    output_path = main_path / output_subfolder
    # Check if the output path exists.
    if not(output_path.exists()):
        # The path doesn't exist.
        # Give an error.
        questions.PrintError(f'Folder detection detected {output_path} as the output file path for {game}, but this folder does not exist.', system_exit = True)
    # Announce the path.
    questions.PrintSuccess(f'Folder detection successfully detected {output_path} as the output file path for {game}.')
    # Determine if it's necessary to print the debug information.
    if settings_dict.get('debug_mode', False) == True:
        # It's necessary to print the debug information.
        # Print the title.
        questions.PrintPlain('\n\nDebug information from GetOutputPath in basic_xml_ops.py:')
        questions.PrintDebug('settings_dict', settings_dict)
        questions.PrintPlain('\n\n')
    # Return the collected path.
    return output_path