import sys
import os
import shutil
import configparser
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import argparse
from pathlib import Path

CONFIG_FILE = "settings.ini"

def load_destination():
    """Reads the output destination from settings.ini."""
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        return config.get("Settings", "destination", fallback="")
    return ""

def save_destination(dest_path):
    """Saves the output destination to settings.ini."""
    config = configparser.ConfigParser()
    if not config.has_section("Settings"):
        config.add_section("Settings")
    config.set("Settings", "destination", dest_path)
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

def copy_file(source_file, dest_dir):
    """Copies a file to the target destination directory."""
    if not dest_dir:
        return False, "Destination path is empty."
    if not os.path.exists(source_file):
        return False, f"Source file does not exist: {source_file}"
    
    try:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        shutil.copy(source_file, dest_dir)
        return True, f"Successfully copied to {dest_dir}"
    except Exception as e:
        return False, str(e)

class FileCopierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Copier Dropzone")
        self.root.geometry("500x300")
        
        # Destination Entry Setup
        tk.Label(root, text="Output Destination:").pack(anchor="w", padx=10, pady=(10, 0))
        
        self.dest_var = tk.StringVar(value=load_destination())
        # Triggers saving to settings.ini whenever the entry text changes
        self.dest_var.trace_add("write", self.on_destination_change)
        
        self.entry = tk.Entry(root, textvariable=self.dest_var, width=60)
        self.entry.pack(fill="x", padx=10, pady=5)
        
        # Drag and Drop Area Setup
        self.drop_label = tk.Label(
            root, 
            text="Drag & Drop Files Here to Copy", 
            bg="lightgray", 
            relief="groove", 
            height=10
        )
        self.drop_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Register for TkinterDnD Drop Events
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self.handle_drop)

    def on_destination_change(self, *args):
        """Updates settings.ini when the entry modifications occur."""
        save_destination(self.dest_var.get())

    def handle_drop(self, event):
        """Processes files dropped into the interface."""
        dest = self.dest_var.get().strip()
        if not dest:
            messagebox.showerror("Error", "Please specify a destination path first.")
            return

        # TkinterDnD passes file lists as a single string wrapped in curly braces if spaces exist
        raw_data = event.data
        files = self.parse_dropped_files(raw_data)
        
        success_count = 0
        errors = []
        
        for file_path in files:
            if os.path.isfile(file_path):
                success, msg = copy_file(file_path, dest)
                if success:
                    success_count += 1
                else:
                    errors.append(f"{os.path.basename(file_path)}: {msg}")
        
        # Provide visual feedback on operation success
        if errors:
            err_msg = "\n".join(errors)
            messagebox.showerror("Copy Alerts", f"Copied {success_count} files.\nFailures:\n{err_msg}")
        elif success_count > 0:
            messagebox.showinfo("Success", f"Successfully copied {success_count} file(s)!")

    def parse_dropped_files(self, data_str):
        """Parses the specialized file paths string provided by tkinterdnd2."""
        import re
        # Find matches for both wrapped paths {with spaces} and standard single paths
        matches = re.findall(r'\{(.*?)\}|(\S+)', data_str)
        # Flatten the tuples into a single list of clean path strings
        return [match[0] if match[0] else match[1] for match in matches]

def hide_console():
    """Hides the console window if running on Windows."""
    if sys.platform == "win32":
        import ctypes
        # Get the handle of the current console window
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd != 0:
            # SW_HIDE = 0 hides the window
            ctypes.windll.user32.ShowWindow(hwnd, 0)

# This function gets the application path.
def GetApplicationPath():
    if getattr(sys, 'frozen', False):
        application_path = Path(sys.executable).parent
    else:
        application_path = Path(__file__).parent
    return application_path

def ProcessArguments(application_path):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_path', nargs = '?')
    parser.add_argument('-s', '--settings', default = 'settings.ini')
    parser.add_argument('-d', '--debug')
    args = parser.parse_args()
    input_file_path = args.input_file_path
    print(f'DEBUG: input_file_path = {input_file_path}')
    return input_file_path

def main():
    application_path = GetApplicationPath()
    input_file_path = ProcessArguments(application_path)
    # CLI Logic: Argument passed
    if input_file_path is not None:
        destination = load_destination()
        
        if not destination:
            print("Error: No destination configured in settings.ini.", file=sys.stderr)
            sys.exit(1)
            
        success, message = copy_file(input_file_path, destination)
        if success:
            print(message)
            sys.exit(0)
        else:
            print(f"Error: {message}", file=sys.stderr)
            sys.exit(1)
            
    # GUI Logic: No arguments passed
    else:
        hide_console()
        root = TkinterDnD.Tk()
        app = FileCopierGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main()
