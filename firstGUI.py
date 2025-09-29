import tkinter as tk
from tkinter import ttk

def on_button_click():
    """
    Function to run when the button is pressed.
    It reads the text from the entry box and displays it in the output label.
    """
    # 1. Get the text from the input box (Entry widget)
    input_text = entry.get()

    # 2. Update the output label
    if input_text:
        output_label.config(text=f"Hello, {input_text}!")
    else:
        output_label.config(text="Please enter your name!")

# --- Main Window Setup ---
# Create the main window object
root = tk.Tk()
root.title("Simple Tkinter App")
root.geometry("300x200") # Set an initial size for the window

# --- Widget Creation ---

# 1. Text Box (Entry Widget)
# This is a single-line text input field.
# The `ttk.Entry` version is used for a slightly more modern look.
entry_label = ttk.Label(root, text="Enter Name:")
entry_label.pack(pady=5) # Add padding below the label

entry = ttk.Entry(root, width=20)
entry.pack(pady=5)

# 2. Button Widget
# This widget is linked to the 'on_button_click' function using the 'command' argument.
button = ttk.Button(root, text="Say Hello", command=on_button_click)
button.pack(pady=10)

# 3. Output Display (Label Widget)
# A Label is used to display static or changing text (our output).
# We use a tk.StringVar to easily manage the text content.
output_label = ttk.Label(root, text="Waiting for input...")
output_label.pack(pady=5)

# --- Start the Main Loop ---
# This is required to make the window appear and listen for events (like button clicks).
root.mainloop()