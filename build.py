# ####### #
# IMPORTS #
# ####### #
# Internal modules
import questions
# External modules
from os import makedirs, remove, system
from pathlib import Path
from shutil import copy, copytree, rmtree


# ############## #
# MAIN EXECUTION #
# ############## #
# Get the folder that this is functioning in.
application_path = Path(__file__).parent
# Get the path to the dist folder.
dist_folder = application_path / 'dist'
# Determine if the dist folder exists.
if dist_folder.exists():
    # The dist folder exists.
    # Announce that the dist folder will be removed.
    questions.PrintImportant('Clearing existing folder . . .')
    # Remove the dist folder.
    rmtree(dist_folder)
# Remake the dist folder.
makedirs(dist_folder)
# Determine which build is being done.
build_to_do = questions.Select('Which build are you compiling?', ['Personal Build', 'Release Build'])
# Announce that resources are being copied.
questions.PrintImportant('Copying resources . . .')
# Determine which build was selected.
if build_to_do == 'Personal Build':
    # This is the personal build.
    # Copy the personal folder detection folder.
    copytree((application_path / 'Folder Detection'), (dist_folder / 'Folder Detection'))
    remove(dist_folder / 'Folder Detection' / 'Cyclops (Example).xml')
    # Copy the settings.ini file.
    copy((application_path / 'settings.ini'), dist_folder)
else:
    # This is the release build.
    # Set up the release version of the folder detection folder.
    makedirs(dist_folder / 'Folder Detection')
    copy((application_path / 'Folder Detection' / 'Cyclops (Example).xml'), (dist_folder / 'Folder Detection' / 'Cyclops.xml'))
    # Set up the release version of settings.ini.
    with open((dist_folder / 'settings.ini'), 'w') as file:
        file.write('[CHARACTER]\n')
        file.write('XML1_num = None\nXML2_num = 0101\nMUA1_num = 17201\nMUA2_num = Ask\n')
        file.write('XML1_path = None\nXML2_path = Detect\nMUA1_path = C:\\Users\\ethan\\Desktop\\New Folder\nMUA2_path = Ask\n')
        file.write('\n[ASSET]\n')
        file.write('XML1_num_XX = False\nXML2_num_XX = True\nMUA1_num_XX = True\nMUA2_num_XX = True\n')
        file.write('XML1_special_name = None\nXML2_special_name = Boss Skin\nMUA1_special_name = None\nMUA2_special_name = None\n')
        file.write('\n[CONSOLES]\n')
        file.write('PC = True\nSteam = True\nGameCube = False\nPS2 = False\nPS3 = True\nPSP = False\nWii = True\nXbox = True\nXbox_360 = True\n')
        file.write('\n[SETTINGS]\n')
        file.write('big_texture = False\nsecondary_skin = False\nuntextured_okay = False\ngenerate_collision = False\nigBlend_to_igAlpha_transparency = False\n')
        file.write('skip_subfolder = False\nforce_adv_tex_folders = False\nadvanced_texture_ini = None\nfoced_asset_type = None')
# Open the existing batch file.
with open((application_path / 'igbFinisher.bat'), 'r') as file:
    # Create a list of lines.
    batch_file_lines = []
    for line in file:
        batch_file_lines.append(line)
# Open the new batch file.
with open((dist_folder / 'igbFinisher.bat'), 'w') as file:
    # Loop through the lines in the batch file.
    for line in batch_file_lines:
        # Make sure this isn't a pause line.
        if not('pause' in line):
            # This isn't a pause line.
            # Check if this has the py file in it.
            if 'igbFinisher.py' in line:
                line = line.replace('igbFinisher.py', 'igbFinisher.exe')
            if 'py ' in line:
                line = line.replace('py ', '')
            # Write the line to the file.
            file.write(line)
# Announce that pyinstaller will be run.
questions.PrintImportant('Running pyinstaller . . .')
# Run pyinstaller.
system('pyinstaller igbFinisher.py --onefile --icon=icon.ico --add-data "icon.ico:."')