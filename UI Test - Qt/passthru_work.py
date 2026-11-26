'''
To achieve this cleanly without freezing your PySide6 interface, I recommend using QProcess in the UI application paired with stdout / stderr flushing in the worker executable.
QProcess is built specifically for this: it runs external executables asynchronously and emits signals whenever the child process prints text, allowing you to update your UI in real time.

In your second program, use sys.stdout for normal status updates and sys.stderr for errors.
Crucial Step: When Python is compiled into an .exe (or run without a console), it buffers output in memory instead of sending it immediately. You must pass flush=True to every print() statement, or the UI won't receive anything until the worker finishes.
'''
import sys
import time


def process_file(file_path):
    try:
        # Send status updates to stdout (flush=True is mandatory!)
        print(f"Starting processing for: {file_path}", flush=True)
        time.sleep(1)  # Simulating work

        print("Step 1/2: Reading data...", flush=True)
        time.sleep(1)

        # Example error condition
        if file_path.endswith(".bad"):
            raise ValueError("Unsupported or corrupted file format.")

        print("Step 2/2: Finalizing...", flush=True)
        time.sleep(1)

        print("Processing complete!", flush=True)

    except Exception as e:
        # Send errors to stderr so the UI knows to trigger a popup
        print(f"Error processing {file_path}: {str(e)}", file=sys.stderr, flush=True)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No file path provided.", file=sys.stderr, flush=True)
        sys.exit(1)

    target_file = sys.argv[1]
    process_file(target_file)
