import tkinter as tk
from tkinter import ttk

class LanguageSelectorApp:
    """
    A Tkinter application using a class structure to display greetings
    in various languages based on button clicks.
    """
    def __init__(self, master):
        # The 'master' argument is the root Tk window.
        self.master = master
        master.title("Language Selector")
        master.geometry("450x300")
        
        # Data storage: Dictionary mapping language names to greetings
        self.greetings = {
            "English": "Hello! Thank you for clicking.",
            "Spanish": "¡Hola! Gracias por hacer clic.",
            "French": "Bonjour ! Merci d'avoir cliqué.",
            "German": "Hallo! Danke fürs Klicken.",
            "Japanese": "こんにちは！クリックしていただきありがとうございます。",
        }
        
        # --- 1. Set up the main frame and styling ---
        # ttk.Frame is used to hold the content, often better than placing directly on root.
        main_frame = ttk.Frame(master, padding="15 15 15 15")
        main_frame.pack(fill='both', expand=True)

        # --- 2. Greeting/Instruction Label ---
        self.instruction_label = ttk.Label(
            main_frame,
            text="Welcome! Please select a language below:",
            font=('Helvetica', 14, 'bold')
        )
        # Use grid for more flexible layout control (put it in the first row, center it)
        self.instruction_label.grid(row=0, column=0, columnspan=5, pady=20)
        
        # --- 3. Button Container Frame ---
        # A separate frame to group the buttons nicely
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=5, pady=10)
        
        # --- 4. Dynamically Create Buttons ---
        col_index = 0
        for language in self.greetings.keys():
            # The 'lambda' function captures the current 'language' value 
            # and passes it as an argument to the self.change_greeting method when clicked.
            button = ttk.Button(
                button_frame, 
                text=language, 
                command=lambda lang=language: self.change_greeting(lang)
            )
            # Place each button in the container frame with some padding
            button.grid(row=0, column=col_index, padx=5, pady=5)
            col_index += 1

        # --- 5. Output Label (The only label that changes) ---
        self.output_label = ttk.Label(
            main_frame,
            text="Awaiting your selection...",
            font=('Helvetica', 12),
            foreground='blue' # Make the output stand out
        )
        self.output_label.grid(row=2, column=0, columnspan=5, pady=30)


    def change_greeting(self, language_key):
        """
        Updates the text in the output_label based on the button clicked.

        :param language_key: The string key (e.g., "English", "French") 
                             that corresponds to the button clicked.
        """
        # Retrieve the specific greeting from the dictionary
        new_greeting = self.greetings.get(language_key, "Error: Greeting not found.")
        
        # Update the output label's text configuration
        self.output_label.config(text=new_greeting)


# --- Application Execution ---
if __name__ == "__main__":
    # Create the root window instance
    root = tk.Tk()
    
    # Create an instance of our application class, passing the root window
    app = LanguageSelectorApp(root)
    
    # Start the Tkinter event loop
    root.mainloop()
