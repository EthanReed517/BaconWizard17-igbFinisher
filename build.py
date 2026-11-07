# ####### #
# IMPORTS #
# ####### #
# Internal modules
import questions
# External modules
from datetime import datetime
from os import makedirs, remove
from pathlib import Path
import pyinstaller_versionfile
from shutil import copy, copytree, make_archive, rmtree
import subprocess


# ######### #
# FUNCTIONS #
# ######### #
# This function checks for the version number.
def GetVersion(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__') and '=' in line:
                version_str = line.split('=')[1].strip().strip('\'"')
                # Windows requires a 4-number version number.
                return f'{version_str}.0', version_str


# ############## #
# MAIN EXECUTION #
# ############## #
if __name__ == '__main__':
    # Get the folder that this is functioning in.
    application_path = Path(__file__).parent
    # Remove the dist folder if it exists and (re)make it.
    dist_folder = application_path / 'dist'
    if dist_folder.exists():
        questions.PrintImportant('Clearing existing folder . . .')
        rmtree(dist_folder)
    makedirs(dist_folder)
    # Determine which build is being done.
    build_to_do = questions.Select('Which build are you compiling?', ['Personal Build', 'Release Build'])
    # Announce that resources are being copied.
    questions.PrintImportant('Copying resources . . .')
    # The personal build copies the main files. The release build gets specific files to show off.
    if build_to_do == 'Personal Build':
        copytree((application_path / 'Folder Detection'), (dist_folder / 'Folder Detection'))
        remove(dist_folder / 'Folder Detection' / 'Cyclops (Example).xml')
        copy((application_path / 'settings.ini'), dist_folder)
    else:
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
            file.write('skip_subfolder = False\nforce_adv_tex_folders = False\nadvanced_texture_ini = None\nforced_asset_type = None')
    # Parse the existing batch file.
    with open((application_path / 'igbFinisher.bat'), 'r') as file:
        batch_file_lines = []
        for line in file:
            batch_file_lines.append(line)
    # Write a new batch file for the exe instead of the py and don't pause.
    with open((dist_folder / 'igbFinisher.bat'), 'w') as file:
        for line in batch_file_lines:
            if not('pause' in line):
                if 'igbFinisher.py' in line:
                    line = line.replace('igbFinisher.py', 'igbFinisher.exe')
                if 'py ' in line:
                    line = line.replace('py ', '')
                file.write(line)
    # Get the version number and the current year.
    app_version_windows, app_version = GetVersion(application_path / 'igbFinisher.py')
    copyright_year = datetime.now().year
    # Create the Windows version file.
    pyinstaller_versionfile.create_versionfile(
        output_file='version_info.txt',
        version=app_version_windows,
        company_name='Marvel Mods',
        file_description='Process igb Files After Export',
        internal_name='igbFinisher',
        legal_copyright=f'Copyright © {copyright_year} BaconWizard17. All Rights Reserved.',
        original_filename='igbFinisher.exe',
        product_name='igbFinisher'
    )
    # Run pyinstaller.
    questions.PrintImportant('Running pyinstaller . . .')
    subprocess.run([
        'pyinstaller',
        'igbFinisher.py',
        '--onefile',
        '--icon=icon.ico',
        '--version-file=version_info.txt'
    ], check=True)
    # Create the zip file.
    make_archive(
        base_name=f'igbFinisher-v{app_version}',
        format='zip',
        root_dir=application_path / 'dist'
    )
    copy(application_path / f'igbFinisher-v{app_version}.zip', application_path / 'dist')
    remove(application_path / f'igbFinisher-v{app_version}.zip')
    # Clean up the version file.
    if (application_path / 'version_info.txt').exists():
        remove(application_path / 'version_info.txt')
    questions.PrintSuccess('Build complete!')