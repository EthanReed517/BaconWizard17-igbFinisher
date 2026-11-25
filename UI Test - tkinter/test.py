import tkinter as tk


def update_state(*args):
    choice = radio_var.get()

    if choice in ("Option 1", "Option 2"):
        # Clear the text box and disable (grey out) it
        entry_var.set("")
        entry_box.config(state="disabled")
        test_variable.set(choice)
    elif choice == "Entry":
        # Enable the text box and sync test_variable with its contents
        entry_box.config(state="normal")
        entry_box.focus()
        test_variable.set(entry_var.get())

    # Update the on-screen label so you can see the live value
    status_label.config(text=f"test_variable = '{test_variable.get()}'")


# Set up the main window
root = tk.Tk()
root.title("Radio & Entry Control")
root.geometry("320x220")
root.config(padx=20, pady=20)

# Tkinter variables to track widget states and the final value
test_variable = tk.StringVar(value="Option 1")
radio_var = tk.StringVar(value="Option 1")
entry_var = tk.StringVar()

# Automatically trigger update_state whenever the user types in the Entry box
entry_var.trace_add("write", update_state)

# Create the 3 Radio Buttons
tk.Radiobutton(
    root,
    text="Option 1",
    variable=radio_var,
    value="Option 1",
    command=update_state,
).pack(anchor="w")

tk.Radiobutton(
    root,
    text="Option 2",
    variable=radio_var,
    value="Option 2",
    command=update_state,
).pack(anchor="w")

tk.Radiobutton(
    root,
    text="Entry",
    variable=radio_var,
    value="Entry",
    command=update_state,
).pack(anchor="w")

# Create the Text Entry field (starts disabled because "Option 1" is default)
entry_box = tk.Entry(root, textvariable=entry_var, state="disabled", width=30)
entry_box.pack(anchor="w", pady=(5, 15))

# Label to display the current value of test_variable in real time
status_label = tk.Label(
    root, text=f"test_variable = '{test_variable.get()}'", fg="blue"
)
status_label.pack(anchor="w")

root.mainloop()
