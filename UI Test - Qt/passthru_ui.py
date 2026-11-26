'''
In your PySide6 application, use QProcess to launch worker.exe. Connect its readyReadStandardOutput signal to your output text box, and readyReadStandardError to a QMessageBox popup.
'''
import sys
from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
# Import your generated UI class
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Enable drag and drop on the main window (or your specific drop widget)
        self.setAcceptDrops(True)

        # Initialize QProcess
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

    # --- Drag & Drop Handlers ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.start_worker(file_path)

    # --- Process Management ---
    def start_worker(self, file_path):
        # Prevent starting a new process if one is already running
        if self.process.state() != QProcess.NotRunning:
            QMessageBox.warning(
                self, "Busy", "A file is currently being processed."
            )
            return

        # Assuming self.outputTextEdit is your output window in the .ui file
        self.outputTextEdit.append(f"--- Launching worker for {file_path} ---")

        # Path to your compiled second exe, followed by the list of arguments
        worker_exe = "worker.exe"
        self.process.start(worker_exe, [file_path])

    def handle_stdout(self):
        # Read raw bytes from stdout and decode to string
        data = self.process.readAllStandardOutput().data().decode("utf-8")
        # .strip() removes trailing newlines so QTextEdit doesn't double-space
        self.outputTextEdit.append(data.strip())

    def handle_stderr(self):
        # Read raw bytes from stderr and show a popup
        error_msg = (
            self.process.readAllStandardError().data().decode("utf-8").strip()
        )
        if error_msg:
            QMessageBox.critical(self, "Processing Error", error_msg)

    def process_finished(self, exit_code, exit_status):
        self.outputTextEdit.append(f"--- Finished (Exit Code: {exit_code}) ---\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

'''
Key Tips for Compiling to .exe (PyInstaller / Nuitka)

1. Hide the Console Window on worker.exe: When compiling worker.exe (e.g., with PyInstaller's --noconsole or --windowed flag), Windows will not flash an empty black command prompt window every time a file is dropped. QProcess will still capture stdout and stderr invisibly in the background.
2. File Paths: When main.exe calls worker.exe, use os.path.join(os.path.dirname(sys.executable), "worker.exe") in production so it reliably finds worker.exe sitting next to it, regardless of what directory the user launched the app from.
3. Multiple Files at Once: The dropEvent loop above will trigger a warning if the user drops 5 files at once because QProcess only handles one instance per object. If users will drop batches of files, store dropped paths in a Python collections.deque (a queue) and pop the next file inside process_finished().




To get both behaviors, compile worker.exe as a standard console application (do not use --noconsole or --windowed), and let QProcess handle hiding the window on Windows when launched from main_ui.exe.
If you compile worker.exe with --noconsole, Windows strips its ability to attach to the command prompt when run manually. Compiling it normally keeps console output intact for CLI users, while QProcess intercepts the pipes and suppresses the window when called from your UI.


1. Compiling with PyInstaller

Compile your two scripts with different console flags:
• UI Executable: Use --windowed so the GUI doesn't open a background terminal.

pyinstaller --windowed main_ui.py

Worker Executable: Omit --windowed (or explicitly pass --console) so it behaves like a normal CLI tool when double-clicked or run in cmd

pyinstaller --console worker.py



2. Suppressing the Window in main_ui.py

By default, QProcess on Windows already suppresses the console window for child processes (CREATE_NO_WINDOW) when stdout/stderr pipes are managed by Qt.
However, to guarantee Windows never flashes a console window—even if the user launches main_ui.exe from a terminal or file explorer—explicitly set the CREATE_NO_WINDOW flag (0x08000000) using setCreateProcessArgumentsModifier in your MainWindow.__init__:


import sys
from PySide6.QtCore import QProcess


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.process = QProcess(self)

        # Explicitly prevent Windows from creating a console window for worker.exe
        if sys.platform == "win32":
            self.process.setCreateProcessArgumentsModifier(
                lambda args: args.update({"flags": args["flags"] | 0x08000000})
            )

        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

'''