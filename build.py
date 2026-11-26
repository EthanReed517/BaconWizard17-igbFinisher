# ####### #
# IMPORTS #
# ####### #
# Internal modules
import basic_xml_ops
import questions
# External modules
import configparser
from datetime import datetime
import xml.etree.ElementTree as ET
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
                if 'igbFinisher-cmd.py' in line:
                    line = line.replace('igbFinisher-cmd.py', 'igbFinisher-cmd.exe')
                if 'py ' in line:
                    line = line.replace('py ', '')
                file.write(line)

# This function gathers the information from the forum release post.
def GetReleasePostText(application_path):
    # Open the release post and read its contents.
    with open(application_path / 'Site Resources' / 'Release.bbcode', 'r') as file:
        all_lines = file.readlines()
    # Initialize the lists to store lines before and after the changelog.
    lines_before = []
    lines_after = []
    state = 'before'
    for line in all_lines:
        # When encountering the changelog, stop recording the lines. Start again after.
        if 'Changelog' in line:
            state = 'skip'
        if 'Installation Instructions' in line:
            state = 'after'
        # Record the line if needed.
        if state == 'before':
            lines_before.append(line)
        if state == 'after':
            lines_after.append(line)
    # Add the necessary info to the beginning and end, then return the lists.
    lines_before += ['[u][b]Changelog[/b][/u]:\n', '[spoiler="Expand to see changelog"]\n', '[list]\n']
    lines_after = ['[/list]\n', '[/spoiler]\n', '\n', '\n'] + lines_after
    return lines_before, lines_after

# This function writes the release documentation.
def WriteReleaseDocs(application_path):
    # Get the release post info and prepare other lists.
    lines_before, lines_after = GetReleasePostText(application_path)
    lines_changelog = []
    # Open the versions file and loop through the versions.
    versions_root = basic_xml_ops.OpenGetTreeAndRoot(application_path / 'versions.xml')
    for version_elem in versions_root.findall('Version'):
        version_number_attr = version_elem.get('Number')
        # Prepare the version-specific files lines.
        bbcode_lines = []
        md_lines = []
        # Get the text.
        lines_changelog.append(f'[li]Version {version_number_attr}:')
        if version_elem.get('PreText') is not None:
            bbcode_lines.append(version_elem.get('PreText'))
        # Start with an initial indent of 1
        indent = 0
        # Loop through the changes for this version.
        for change_elem in version_elem.findall('Change'):
            # Get the info for this change.
            desc_attr = change_elem.get('Desc')
            desc_gh_attr = change_elem.get('Desc_GH', default=change_elem.get('Desc'))
            # Calculate the change from the old indent before updating the variable.
            indent_change = int(change_elem.get('Indent', default='1')) - indent
            indent = int(change_elem.get('Indent', default='1'))
            # Process the BBCode lines and their tags.
            for lines in [lines_changelog, bbcode_lines]:
                if indent_change > 0:
                    lines.append('\n[list]\n')
                else:
                    if indent_change < 0:
                        for i in range(abs(indent_change)):
                            lines.append('[/li]\n[/list]\n')
                    lines.append('[/li]\n')
                lines.append(f'[li]{change_elem.get('Desc')}')
            # Markdown lines are more straightforward to format.
            if change_elem.get('Desc_GH') is not None:
                md_lines.append(f'{'  ' * (indent - 1)}- {change_elem.get('Desc_GH')}\n')
            else:
                md_lines.append(f'{'  ' * (indent - 1)}- {change_elem.get('Desc')}\n')
        # Close out necessary info.
        if not(indent == 1):
            for i in range(abs(indent_change)):
                bbcode_lines.append('[/li]\n[/list]\n')
                lines_changelog.append('[/li]\n[/list]\n')
        bbcode_lines.append('[/li]\n[/list]\n')
        lines_changelog.append('[/li]\n[/list]\n[/li]\n')
        if version_elem.get('PostText') is not None:
            bbcode_lines.append('\n' + version_elem.get('PostText') + '\n')
        # Write the resulting files.
        if not(version_elem.get('NoUpdate') == 'True'):
            with open(application_path / 'Site Resources' / f'Update-v{version_number_attr}.bbcode', 'w') as file:
                for line in bbcode_lines:
                    file.write(line)
        with open(application_path / 'Site Resources' / f'Update-v{version_number_attr}.md', 'w') as file:
            for line in md_lines:
                file.write(line)
    with open(application_path / 'Site Resources' / 'Release.bbcode', 'w') as file:
            for line in lines_before + lines_changelog + lines_after:
                file.write(line)

# This function updates the .iss file with the latest version number.
def UpdateISSVersion(application_path, app_version):
    with open(application_path / 'igbFinisher-setup.iss', 'r') as file:
        lines = [line.rstrip("\n") for line in file]
    new_lines = []
    for line in lines:
        if line.startswith('#define MyAppVersion'):
            new_lines.append(f'#define MyAppVersion "{app_version}"')
        else:
            new_lines.append(line)
    with open(application_path / 'igbFinisher-setup.iss', 'w') as file:
        for line in new_lines:
            file.write(f'{line}\n')


# ############## #
# MAIN EXECUTION #
# ############## #
if __name__ == '__main__':
    # Get the folder that this is functioning in.
    application_path = Path(__file__).parent
    # Get the version number.
    app_version_windows, app_version = GetVersion(application_path / 'igbFinisher-cmd.py')
    questions.PrintImportant(f'Building igbFinisher v{app_version} . . .')
    # Remove the dist and release folder if it exists and (re)make it.
    dist_folder = application_path / 'dist'
    release_folder = application_path / 'release'
    for subfolder in [dist_folder, release_folder]:
        if subfolder.exists():
            questions.PrintImportant('Clearing existing folder . . .')
            rmtree(subfolder)
        makedirs(subfolder)
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
    # Create the Windows version file.
    pyinstaller_versionfile.create_versionfile(
        output_file='version_info.txt',
        version=app_version_windows,
        company_name='Marvel Mods',
        file_description='Command line tool to process igb Files After Export',
        internal_name='igbFinisher',
        legal_copyright=f'Copyright © {datetime.now().year} BaconWizard17. All Rights Reserved.',
        original_filename='igbFinisher-cmd.exe',
        product_name='igbFinisher Command Line'
    )
    # Run pyinstaller.
    questions.PrintImportant('Running pyinstaller . . .')
    copy(application_path / 'design' / 'logo.ico', application_path)
    subprocess.run([
        'pyinstaller',
        'igbFinisher-cmd.py',
        '--onefile',
        '--icon=logo.ico',
        '--version-file=version_info.txt'
    ], check=True)
    # Create the zip file. It is made in the main folder to avoid self-referencing.
    zip_file_path = application_path / f'igbFinisher-v{app_version}-portable'
    make_archive(
        base_name=zip_file_path,
        format='zip',
        root_dir=application_path / 'dist'
    )
    copy(f'{zip_file_path}.zip', release_folder)
    remove(f'{zip_file_path}.zip')
    # Build the installer.
    UpdateISSVersion(application_path, app_version)
    subprocess.run([
        str(Path('C:\\Program Files\\Inno Setup 7\\ISCC.exe')),
        '/dist',
        f'/igbFinisher-v{app_version}-installer',
        str(Path('igbFinisher-setup.iss').resolve()),
    ], check=True)
    # Clean up the version file.
    if (application_path / 'version_info.txt').exists():
        remove(application_path / 'version_info.txt')
    remove(application_path / 'logo.ico')
    # Write the release docs.
    WriteReleaseDocs(application_path)
    questions.PrintSuccess(f'Successfully built igbFinisher v{app_version}!')