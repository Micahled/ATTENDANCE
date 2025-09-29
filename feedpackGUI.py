import tkinter as tk
from tkinter import ttk, messagebox

class FeedbackApp:
    """
    A simple Tkinter application for collecting customer feedback.
    
    The application collects Name, Email, and a multi-line Feedback message.
    Upon submission, the data is printed to the console and the form is cleared.
    """
    def __init__(self, root):
        # Set up the main window (root)
        self.root = root
        self.root.title("Customer Experience Feedback")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        # Configure styling (using ttk for modern widgets)
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=5)

        # Create a main frame for padding and structure
        main_frame = ttk.Frame(root, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Allow the frame to expand slightly
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # --- Input Variables ---
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()

        # --- Name Input (Row 0) ---
        ttk.Label(main_frame, text="Your Name:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=50)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.name_entry.focus() # Start cursor here

        # --- Email Input (Row 1) ---
        ttk.Label(main_frame, text="Your Email:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.email_entry = ttk.Entry(main_frame, textvariable=self.email_var, width=50)
        self.email_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        # --- Feedback Text Area (Row 2 & 3) ---
        ttk.Label(main_frame, text="Your Feedback:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        
        # Use a Text widget for multi-line input
        self.feedback_text = tk.Text(main_frame, height=10, width=40, wrap=tk.WORD, font=('Arial', 10), relief=tk.FLAT, borderwidth=1, highlightthickness=1, highlightbackground="lightgray")
        self.feedback_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=5)

        # Add a scrollbar to the Text widget
        text_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.feedback_text.yview)
        text_scrollbar.grid(row=3, column=2, sticky=(tk.N, tk.S, tk.W))
        self.feedback_text['yscrollcommand'] = text_scrollbar.set

        # Configure columns for responsive sizing
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)

        # --- Submit Button (Row 4) ---
        submit_button = ttk.Button(main_frame, text="Submit Feedback", command=self.submit_feedback)
        submit_button.grid(row=4, column=0, columnspan=3, pady=20, padx=5)

    def submit_feedback(self):
        """
        Handles the submission process:
        1. Retrieves and prints the data to the console.
        2. Clears all input fields.
        """
        # 1. Retrieve data
        name = self.name_var.get()
        email = self.email_var.get()
        # Text widgets require specific indexing: '1.0' is line 1, character 0. 
        # 'end-1c' removes the automatic newline character added by the Text widget.
        feedback = self.feedback_text.get('1.0', 'end-1c').strip()

        # Simple validation (optional, but good practice)
        if not name or not email or not feedback:
            messagebox.showerror("Error", "Please fill in all fields before submitting.")
            return

        # 2. Print the text to the console (the user's request)
        print("--- FEEDBACK SUBMITTED ---")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Feedback:\n{feedback}\n" + "="*40)

        # 3. Clear the text fields
        self.name_var.set("")
        self.email_var.set("")
        self.feedback_text.delete('1.0', 'end')
        
        # Confirmation message (using Tkinter's messagebox)
        messagebox.showinfo("Success", "Thank you for your feedback! Your submission has been processed.")
        self.name_entry.focus()


if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    
    # Initialize and run the application
    app = FeedbackApp(root)
    
    # Start the Tkinter event loop
    root.mainloop()
