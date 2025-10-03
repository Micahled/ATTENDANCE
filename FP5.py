import tkinter as tk
from tkinter import messagebox
import sqlite3
import re

# --- Database Management Class ---
class DatabaseManager:
    """Handles the connection to and operations on the SQLite database."""
    def __init__(self, db_name='customers.db'):
        # Connect to the SQLite database file. It will be created if it doesn't exist.
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        print(f"Database connected: {db_name}")

    def create_table(self):
        """Creates the 'customers' table with all required fields."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birthday TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                contact_method TEXT
            )
        """)
        self.conn.commit()

    def insert_customer(self, data):
        """Inserts a new customer record into the database."""
        # data is expected as a tuple: (name, birthday, email, phone, address, contact_method)
        sql = """
            INSERT INTO customers (name, birthday, email, phone, address, contact_method)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
            print(f"Data saved for: {data[0]}")
            return True
        except sqlite3.Error as e:
            # Print error to console and return False if insertion fails
            print(f"Database error during insertion: {e}")
            return False

    def close(self):
        """Closes the database connection."""
        self.conn.close()
        print("Database connection closed.")

# --- GUI Application Class ---
class CustomerFormApp:
    """Manages the Tkinter GUI and interacts with the DatabaseManager."""
    def __init__(self, master, db_manager):
        self.master = master
        master.title("Customer Information Management System")
        # Define a consistent size for the window
        master.geometry("550x450")
        
        # CHANGED: Set main window background to white
        master.config(bg='#ffffff') 
        
        self.db_manager = db_manager

        # Frame to hold all form elements
        # Set frame background to white
        self.form_frame = tk.Frame(master, padx=20, pady=20, bg='#ffffff', relief='groove', bd=1)
        self.form_frame.pack(padx=30, pady=30, fill='x')

        self.fields = {}
        self.create_widgets()

    def create_widgets(self):
        """Creates all labels, entry fields, and buttons for the GUI."""
        
        # Title Label
        title_label = tk.Label(
            self.form_frame, 
            text="Customer Registration Form", 
            font=("Helvetica", 16, "bold"), 
            bg='#ffffff', 
            fg='black' # CHANGED: Set title font to black
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")

        field_names = {
            "Name": "Customer Name (Required)", 
            "Birthday": "Birthday (YYYY-MM-DD)", 
            "Email": "Email Address", 
            "Phone Number": "Phone Number", 
            "Address": "Full Address"
        }
        
        # Create Entry Fields and Labels
        for i, (key, placeholder) in enumerate(field_names.items()):
            label = tk.Label(
                self.form_frame, 
                text=key + ":", 
                font=("Helvetica", 10), 
                bg='#ffffff', # Set label background to white
                fg='black',   # Set label font to black
                anchor='w'
            )
            label.grid(row=i + 1, column=0, sticky="w", pady=5, padx=10)
            
            # UPDATED: Added bg='#eeeeee' for a light gray background on the entry fields
            entry = tk.Entry(self.form_frame, width=45, relief='solid', bd=1, font=("Helvetica", 10), bg='#eeeeee')
            entry.grid(row=i + 1, column=1, pady=5, padx=10, ipady=3)
            # Add a placeholder text (via a function for simplicity)
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>", lambda event, e=entry, p=placeholder: self.on_focus_in(e, p))
            entry.bind("<FocusOut>", lambda event, e=entry, p=placeholder: self.on_focus_out(e, p))
            self.fields[key] = entry

        # Dropdown for Preferred Contact Method (Requirement 2)
        contact_label = tk.Label(
            self.form_frame, 
            text="Preferred Contact:", 
            font=("Helvetica", 10), 
            bg='#ffffff', # Set label background to white
            fg='black',   # Set label font to black
            anchor='w'
        )
        contact_label.grid(row=len(field_names) + 1, column=0, sticky="w", pady=10, padx=10)
        
        self.contact_var = tk.StringVar(self.form_frame)
        self.contact_var.set("Email") # Set default value
        
        contact_options = ["Email", "Phone", "Mail"]
        contact_menu = tk.OptionMenu(self.form_frame, self.contact_var, *contact_options)
        
        # Kept the dropdown background slightly off-white for contrast against the white form
        contact_menu.config(width=42, relief='flat', bd=1, bg='#ecf0f1', activebackground='#bdc3c7', direction='below', fg='black') 
        contact_menu.grid(row=len(field_names) + 1, column=1, pady=10, padx=10)
        
        # Submit Button (Requirement 2) (Color unchanged to maintain prominence)
        submit_button = tk.Button(
            self.form_frame, 
            text="Submit Information", 
            command=self.submit_data, 
            bg="#3498db", # Blue color
            fg="white", 
            font=("Helvetica", 12, "bold"),
            relief='raised',
            activebackground='#2980b9'
        )
        submit_button.grid(row=len(field_names) + 2, column=0, columnspan=2, pady=(20, 10), ipadx=20, ipady=8, sticky="ew")

    # Helper function to handle placeholder text in entry fields
    def on_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    def clear_form(self):
        """Clears all entry fields and resets the dropdown menu."""
        placeholders = {
            "Name": "Customer Name (Required)", 
            "Birthday": "Birthday (YYYY-MM-DD)", 
            "Email": "Email Address", 
            "Phone Number": "Phone Number", 
            "Address": "Full Address"
        }
        for key, entry in self.fields.items():
            entry.delete(0, tk.END)
            # Reset placeholder text
            entry.insert(0, placeholders[key])
            entry.config(fg='grey')
            
        self.contact_var.set("Email")

    def validate_email(self, email):
        """Simple email regex validation."""
        if not email:
            return True # Allow empty email
        # Basic regex pattern for email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def submit_data(self):
        """Collects data, validates it, saves it to the database, and clears the form."""
        
        # 1. Collect Data (Handle placeholder text removal)
        name = self.fields["Name"].get().strip()
        birthday = self.fields["Birthday"].get().strip()
        email = self.fields["Email"].get().strip()
        phone = self.fields["Phone Number"].get().strip()
        address = self.fields["Address"].get().strip()
        contact_method = self.contact_var.get()
        
        # Remove placeholders if they are still present
        if name == "Customer Name (Required)": name = ""
        if birthday == "Birthday (YYYY-MM-DD)": birthday = ""
        if email == "Email Address": email = ""
        if phone == "Phone Number": phone = ""
        if address == "Full Address": address = ""

        # 2. Basic Data Validation (Tip implementation)
        if not name:
            messagebox.showerror("Validation Error", "The Customer Name field is required.")
            return

        if email and not self.validate_email(email):
             messagebox.showerror("Validation Error", "Please enter a valid email address or leave it blank.")
             return
        
        # Create the data tuple for insertion
        data = (name, birthday, email, phone, address, contact_method)
        
        # 3. Database Storage
        if self.db_manager.insert_customer(data):
            # 4. Success and Form Clearing
            messagebox.showinfo("Success", f"Customer '{name}' submitted successfully and saved to 'customers.db'.")
            self.clear_form()
        else:
            messagebox.showerror("Database Error", "Failed to save data. Check the console for details.")

# --- Main Execution ---
if __name__ == "__main__":
    # 1. Set Up the Database
    db_manager = DatabaseManager()
    
    # Create the main Tkinter window
    root = tk.Tk()
    
    # 2. Create the GUI
    app = CustomerFormApp(root, db_manager)
    
    # Start the Tkinter event loop
    root.mainloop()
    
    # Close the database connection when the GUI is closed
    db_manager.close()
