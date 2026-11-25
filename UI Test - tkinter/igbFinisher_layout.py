# Rough layout plans, will not be coded like this in the final build

import sys
import os
import shutil
import configparser
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import argparse
from pathlib import Path
import ctypes as ct
from PIL import Image, ImageTk
import webbrowser

APP_NAME = 'igbFinisher'
APP_VERSION = '5.0.0'
APP_AUTHOR = 'BaconWizard17'
APP_DESCRIPTION = 'A program to process igb files after exporting from 3ds Max.'
APP_URL = 'https://marvelmods.com/forum/index.php/topic,11440.0.html'
APP_GITHUB = 'https://github.com/EthanReed517/BaconWizard17-igbFinisher'


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

class ToolTip:
    def __init__(self, parent, text):
        self.icon_img = ImageTk.PhotoImage(Image.open("info_icon.png").resize((16, 16)))
        self.widget = tk.Label(parent, image=self.icon_img, cursor="hand2")
        self.widget.pack(side='left')
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Removes window border/titlebar
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            tw, text=self.text, background="#ffffe0", 
            relief="solid", borderwidth=1, padx=5, pady=2, wraplength=250
        )
        label.pack()

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class FileCopierGUI:
    def __init__(self, root):
        # Create the main window.
        self.root = root
        self.root.title('igbFinisher')
        root.iconbitmap('logo.ico')
        
        # Create the toolbar.
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        # File menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=lambda: print("New"), underline=0)
        self.file_menu.add_command(label="Open...", command=lambda: print("Open"))
        self.file_menu.add_separator()  
        self.file_menu.add_command(label="Exit", accelerator="Alt+F4", command=self.root.quit)
        # Help menu
        self.about_icon = ImageTk.PhotoImage(Image.open("about.png").resize((16, 16)))
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Help', menu=self.help_menu)
        self.help_menu.add_command(label='About', image=self.about_icon, compound=tk.LEFT, command=self.show_about)
        
        # Keyboard shortcuts
        self.root.bind("<Control-n>", lambda event: print("New"))
        self.root.bind("Alt-F4", root.quit())
        
        # Divide the main window into 2 main areas.
        self.settings_frame = tk.Frame(root)
        self.settings_frame.pack(expand=False, side=tk.LEFT, padx=5, pady=5, fill=tk.Y, anchor='w')
        separator = ttk.Separator(root, orient="vertical")
        separator.pack(side="left", fill="y", padx=5, anchor='w')
        self.drop_frame = tk.Frame(root)
        self.drop_frame.pack(expand=True, side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH)
        
        # Build the notebook where the settings will be stored.
        self.notebook_label = tk.Label(self.settings_frame, text='Processing Settings:').pack(anchor='w', padx=10, pady=(10, 0))
        self.notebook = ttk.Notebook(self.settings_frame)
        self.notebook.pack(expand=False, fill='both', padx=10, pady=10)
        
        # Temporary: define a variable for all radio buttons.
        self.temp_radio_var = tk.StringVar(value='test')
        self.temp_string_var = tk.StringVar(value='12301')
        self.temp_path_var = tk.StringVar(value=r'C:\GitHub\BaconWizard17-Mod-Releases\Custom Models - XML1, XML2\Cable\3. 90s')
        
        # Build the character tab for the notebook.
        self.character_tab = ttk.Frame(self.notebook)
        # Character numbers
        self.num_label_frame = tk.Frame(self.character_tab)
        self.num_label = tk.Label(self.num_label_frame, text=f'Skin Numbers:').pack(side='left')
        ToolTip(self.num_label_frame, 'Enter a 4- or 5- digit skin number for each game. Skin numbers are not used by "other" assets. If "None" is selected, the game will be skipped.')
        self.num_label_frame.pack(expand=True, fill='both')
        self.num_frame = tk.Frame(self.character_tab, relief='groove', borderwidth=1)
        for game in ['XML1', 'XML2', 'MUA1', 'MUA2']:
            self.num_entry_frame = tk.Frame(self.num_frame)
            self.game_num_label = tk.Label(self.num_entry_frame, text=f'{game}:').pack(side='left')
            self.num_radiobutton_none = tk.Radiobutton(
                self.num_entry_frame,
                text='None',
                variable=self.temp_radio_var,
                value='None',
            ).pack(side='left', anchor='e')
            self.num_radiobutton_entry = tk.Radiobutton(
                self.num_entry_frame,
                text='',
                variable=self.temp_radio_var,
                value='Value',
            ).pack(side='left', anchor='e')
            self.num_entry = tk.Entry(self.num_entry_frame, textvariable=self.temp_string_var, width=10)
            self.num_entry.pack(fill='x', side='left', anchor='e')
            self.num_entry_frame.pack(padx=5, pady=5, anchor='w')
        self.num_frame.pack(anchor='w', fill=tk.X, padx=5, pady=5)
        # Paths
        self.path_label_frame = tk.Frame(self.character_tab)
        self.path_label = tk.Label(self.path_label_frame, text=f'Output Folder Paths:').pack(side='left')
        ToolTip(self.path_label_frame, 'Enter the output folder for each game. If "Detect" is selected, output folder detection will be used. If "None" is selected, the game will be skipped.')
        self.path_label_frame.pack(expand=True, fill='both')
        self.path_frame = tk.Frame(self.character_tab, relief='groove', borderwidth=1)
        for game in ['XML1', 'XML2', 'MUA1', 'MUA2']:
            self.path_entry_frame = tk.Frame(self.path_frame)
            self.path_radio_frame = tk.Frame(self.path_entry_frame)
            self.path_label = tk.Label(self.path_radio_frame, text=f'{game}:').pack(side='left')
            self.path_radiobutton_none = tk.Radiobutton(
                self.path_radio_frame,
                text='None',
                variable=self.temp_radio_var,
                value='None',
            ).pack(side='left', anchor='e')
            self.path_radiobutton_detect = tk.Radiobutton(
                self.path_radio_frame,
                text='Detect',
                variable=self.temp_radio_var,
                value='Detect',
            ).pack(side='left', anchor='e')
            self.path_radiobutton_entry = tk.Radiobutton(
                self.path_radio_frame,
                text='Value:',
                variable=self.temp_radio_var,
                value='Value',
            ).pack(side='left', anchor='e')
            self.path_radio_frame.pack(anchor='w')
            self.path_entry = tk.Entry(self.path_entry_frame, textvariable=self.temp_path_var, width=50)
            self.path_entry.xview_moveto(1.0)
            self.path_entry.pack(fill='x', padx=10, pady=5, anchor='e')
            self.path_entry_frame.pack(padx=5, pady=5, anchor='w')
        self.path_frame.pack(anchor='w', fill=tk.X, padx=5, pady=5)
        # Pack the notebook
        self.notebook.add(self.character_tab, text='Game')
        
        # Build the tab for the naming settings.
        self.asset_tab = ttk.Frame(self.notebook)
        # Number XX
        self.num_label_frame = tk.Frame(self.asset_tab)
        self.num_label = tk.Label(self.num_label_frame, text=f'Number ends in XX:').pack(side='left')
        ToolTip(self.num_label_frame, 'Select if the last two digits of the skin number in the file name should be "XX" (True) or if the file name should use the full skin number (False). This setting does not apply to files that do not use the skin number in the file name. This setting does not impact hex editing.')
        self.num_label_frame.pack(expand=True, fill='both')
        self.num_frame = tk.Frame(self.asset_tab, relief='groove', borderwidth=1)
        for game in ['XML1', 'XML2', 'MUA1', 'MUA2']:
            self.num_entry_frame = tk.Frame(self.num_frame)
            self.game_num_label = tk.Label(self.num_entry_frame, text=f'{game}:').pack(side='left')
            self.num_radiobutton_none = tk.Radiobutton(
                self.num_entry_frame,
                text='None',
                variable=self.temp_radio_var,
                value='None',
            ).pack(side='left', anchor='e')
            self.num_radiobutton_entry = tk.Radiobutton(
                self.num_entry_frame,
                text='',
                variable=self.temp_radio_var,
                value='Value',
            ).pack(side='left', anchor='e')
            self.num_entry = tk.Entry(self.num_entry_frame, textvariable=self.temp_string_var, width=10)
            self.num_entry.pack(fill='x', side='left', anchor='e')
            self.num_entry_frame.pack(padx=5, pady=5, anchor='w')
        self.num_frame.pack(anchor='w', fill=tk.X, padx=5, pady=5)
        # Pack the notebook
        self.notebook.add(self.asset_tab, text="Naming")
        
        
   
        self.game_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        self.asset_content = tk.Label(self.game_tab, text="Content for Tab 3").pack(pady=20)
        self.asset_content = tk.Label(self.settings_tab, text="Content for Tab 4").pack(pady=20)
        self.notebook.add(self.game_tab, text="Console")
        self.notebook.add(self.settings_tab, text="Other")
        
        # Drag and Drop Area Setup
        self.drop_image = tk.PhotoImage(file='alchemy_logo.png')
        self.drop_label = tk.Label(self.drop_frame, text='Drop igb files below or click to select files:').pack(anchor='w')
        self.drop_area = tk.Label(
            self.drop_frame, 
            image=self.drop_image, 
            bg="lightgray", 
            relief="groove", 
            height=10
        )
        self.drop_area.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Register for TkinterDnD Drop Events
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.handle_drop)
        self.drop_area.bind("<Button-1>", self.on_click)
    
        # Set the minimum window size dynamically.
        self.root.update_idletasks()
        self.root.minsize(root.winfo_width(), root.winfo_height())

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
    
    def on_click(self, event):
        """Triggered when the drop zone label is clicked."""
        files = filedialog.askopenfilenames(
            title="Select Files", filetypes=[("All Files", "*.*")]
        )
        if files:  # Only update if the user didn't cancel the dialog
            print('yay')

    def parse_dropped_files(self, data_str):
        """Parses the specialized file paths string provided by tkinterdnd2."""
        import re
        # Find matches for both wrapped paths {with spaces} and standard single paths
        matches = re.findall(r'\{(.*?)\}|(\S+)', data_str)
        # Flatten the tuples into a single list of clean path strings
        return [match[0] if match[0] else match[1] for match in matches]
    
    def show_about(self):
        """Opens a modal About window with program information."""
        self.about_win = tk.Toplevel(self.root)
        self.about_win.title(f"About {APP_NAME}")
        self.about_win.iconbitmap('logo.ico')
        #self.about_win.geometry("320x180")
        self.about_win.resizable(False, False)
        
        # Keep the About window on top of the main window and block background clicks
        self.about_win.transient(self.root)
        self.about_win.grab_set()
        
        self.logo_image = tk.PhotoImage(file='logo.png')
        self.drop_area = tk.Label(
            self.about_win, 
            image=self.logo_image, 
        )
        self.drop_area.pack(fill="both", expand=True, padx=10, pady=10)

        self.app_label = ttk.Label(self.about_win, text=APP_NAME, font=("Segoe UI", 13, "bold")).pack(pady=(18, 4))
        self.version_label = ttk.Label(self.about_win, text=f"Version v{APP_VERSION}").pack()
        self.info_label = ttk.Label(
            self.about_win,
            text=APP_DESCRIPTION,
            wraplength=280,
            justify=tk.CENTER
        ).pack(padx=12, pady=12)
        
        self.link_lbl = ttk.Label(
            self.about_win,
            text="Project Website",
            foreground="#1E88E5",
            font=("Segoe UI", 9, "underline"),
            cursor="hand2"  # Changes mouse pointer to a pointing hand on hover
        )
        self.link_lbl.pack(pady=4)
        self.link_lbl.bind("<Button-1>", lambda e: webbrowser.open_new_tab(APP_URL))
        
        self.gh_lbl = ttk.Label(
            self.about_win,
            text="GutHub Page",
            foreground="#1E88E5",
            font=("Segoe UI", 9, "underline"),
            cursor="hand2"  # Changes mouse pointer to a pointing hand on hover
        )
        self.gh_lbl.pack(pady=4)
        self.gh_lbl.bind("<Button-1>", lambda e: webbrowser.open_new_tab(APP_GITHUB))

        self.ok_button = ttk.Button(self.about_win, text="OK", command=self.about_win.destroy).pack(pady=(0, 12))
        
        self.about_win.update()
        hwnd = ct.windll.user32.GetParent(self.about_win.winfo_id())
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        value = ct.c_int(1)
        ct.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ct.byref(value), ct.sizeof(value)
        )
    
        # Set the minimum window size dynamically.
        self.about_win.update_idletasks()
        self.about_win.minsize(self.about_win.winfo_width(), self.about_win.winfo_height())
        

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
        root.update()
        hwnd = ct.windll.user32.GetParent(root.winfo_id())
        '''
        hex_color = '110800'
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        bgr_color = (b << 16) | (g << 8) | r
        DWMWA_CAPTION_COLOR = 35
        ct.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_CAPTION_COLOR, ct.byref(ct.c_int(bgr_color)), ct.sizeof(ct.c_int)
        )
        '''
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        value = ct.c_int(1)
        ct.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ct.byref(value), ct.sizeof(value)
        )
        root.mainloop()

if __name__ == "__main__":
    main()
