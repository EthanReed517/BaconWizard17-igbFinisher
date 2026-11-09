# ####### #
# IMPORTS #
# ####### #
# Internal modules
import questions
# External modules
import configparser
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

# This function writes the release version of settings.ini.
def WriteReleaseSettings(dist_folder):
    # Set up the release version of settings.ini.
    config = configparser.ConfigParser()
    # This allows the keys to be capitalized.
    config.optionxform = str
    # Set up the keys and write the file.
    config['CHARACTER'] = {
        'XML1_num': 'None', 'XML2_num': '0101', 'MUA1_num': '17201', 'MUA2_num': 'Ask',
        'XML1_path': 'None', 'XML2_path': 'Detect', 'MUA1_path': 'C:\\Users\\ethan\\Desktop\\New Folder', 'MUA2_path': 'Ask'
    }
    config['ASSET'] = {
        'XML1_num_XX': 'False', 'XML2_num_XX': 'True', 'MUA1_num_XX': 'True', 'MUA2_num_XX': 'True',
        'XML1_special_name': 'None', 'XML2_special_name': 'Boss Skin', 'MUA1_special_name': 'None', 'MUA2_special_name': 'None'
    }
    config['CONSOLES'] = {'PC': 'True', 'Steam': 'True', 'GameCube': 'False', 'PS2': 'False', 'PS3': 'True', 'PSP': 'False', 'Wii': 'True', 'Xbox': 'True', 'Xbox_360': 'True'}
    config['SETTINGS'] = {
        'big_texture': 'False', 'secondary_skin': 'False', 'untextured_okay': 'False', 'generate_collision': 'False', 'igBlend_to_igAlpha_transparency': 'False',
        'skip_subfolder': 'False', 'force_adv_tex_folders': 'False', 'advanced_texture_ini': 'None', 'forced_asset_type': 'None'
    }
    with open((dist_folder / 'settings.ini'), 'w') as file:
        config.write(file)

# This function writes a batch file that works with the exe.
def WriteExeBatchFile(application_path, dist_folder):
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
        WriteReleaseSettings(dist_folder)
    # Set up a correct batch file to work with the exe.
    WriteExeBatchFile(application_path, dist_folder)
    # Get the version number and the current year.
    app_version_windows, app_version = GetVersion(application_path / 'igbFinisher.py')
    # Create the Windows version file.
    pyinstaller_versionfile.create_versionfile(
        output_file='version_info.txt',
        version=app_version_windows,
        company_name='Marvel Mods',
        file_description='Process igb Files After Export',
        internal_name='igbFinisher',
        legal_copyright=f'Copyright © {datetime.now().year} BaconWizard17. All Rights Reserved.',
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
    # Create the zip file. It is made in the main folder to avoid self-referencing.
    zip_file_path = application_path / f'igbFinisher-v{app_version}'
    make_archive(
        base_name=zip_file_path,
        format='zip',
        root_dir=application_path / 'dist'
    )
    copy(zip_file_path, application_path / 'dist')
    remove(zip_file_path)
    # Clean up the version file.
    if (application_path / 'version_info.txt').exists():
        remove(application_path / 'version_info.txt')
    questions.PrintSuccess('Build complete!')