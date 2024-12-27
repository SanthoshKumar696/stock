import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# database connection
conn = sqlite3.connect('stock.db')
cursor = conn.cursor()

# Create main_ledger table
cursor.execute("""
CREATE TABLE IF NOT EXISTS main_product (
    code TEXT PRIMARY KEY,
    name TEXT UNIQUE
)
""")
conn.commit()


def open_main_product(root):
    # Create a new window for Main Ledger
    ledger_window = tk.Toplevel()
    ledger_window.title("Main Product")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    ledger_window.geometry(f"{screen_width}x{screen_height}")
    
    ledger_window.configure(bg="lightblue")

    tk.Label(ledger_window,text="Main Product", font=("Times", 25, "bold"), fg="green", bg="lightblue").pack(padx=10, pady=20)

    # Frame for the left section (Radio Buttons and Inputs)
    left_frame = tk.Frame(ledger_window, bg="lightblue", height=300)  # Decreased height
    left_frame.pack(side="left", fill="y", padx=5, pady=10)  # Reduced horizontal padding

    # Input for Code
    tk.Label(
        left_frame, 
        text="Code:", 
        font=("Arial", 12), 
        bg="lightblue"
    ).pack(anchor="w", padx=10, pady=5)

    code_entry = tk.Entry(left_frame, width=30, font=("Arial", 12))
    code_entry.pack(padx=10, pady=5)

    # Input for Name
    tk.Label(
        left_frame, 
        text="Name:", 
        font=("Arial", 12), 
        bg="lightblue"
    ).pack(anchor="w", padx=10, pady=5)

    name_entry = tk.Entry(left_frame, width=30, font=("Arial", 12))
    name_entry.pack(padx=10, pady=5)

    # Save button functionality
    def save_entry():
        code = code_entry.get().strip()
        name = name_entry.get().strip()
        if code and name:
            stored_details_tree.insert("", "end", values=(code, name))
            code_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)

            try:
                cursor.execute("INSERT INTO main_product (code, name) VALUES (?, ?)", (code, name))
                conn.commit()
                messagebox.showinfo("Success", f"Product '{name}' added successfully!")
                code_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
            except sqlite3.IntegrityError as e:
                messagebox.showerror("Database Error", f"Error: {e}")

        else:
            messagebox.showwarning("Input Error", "Please enter both Code and Name")

    # Buttons (in a single row)
    button_frame = tk.Frame(left_frame, bg="lightblue")  # Frame to hold buttons horizontally
    button_frame.pack(pady=10)

    tk.Button(
        button_frame, 
        text="Save", 
        font=("Arial", 12), 
        bg="green", 
        fg="white", 
        width=10, 
        command=save_entry
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame, 
        text="Cancel", 
        font=("Arial", 12), 
        bg="orange", 
        fg="white", 
        width=10, 
        command=lambda: [code_entry.delete(0, tk.END), name_entry.delete(0, tk.END)]
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame, 
        text="Exit", 
        font=("Arial", 12), 
        bg="red", 
        fg="white", 
        width=10, 
        command=ledger_window.destroy
    ).pack(side="left", padx=10)

    # Frame for the right section (Stored Details Table)
    right_frame = tk.Frame(ledger_window, bg="lightblue", height=250, width=100)  # Decreased height and increased width
    right_frame.pack(padx=5, pady=10)  # Reduced horizontal padding

    tk.Label(
        right_frame, 
        text="Stored Details", 
        font=("Arial", 12, "bold"), 
        bg="lightblue"
    ).pack(pady=10)

    # Treeview (Table) for displaying stored details
    columns = ("Code", "Name")
    stored_details_tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=10)  # Reduced height
    stored_details_tree.heading("Code", text="Code")
    stored_details_tree.heading("Name", text="Name")
    stored_details_tree.column("Code", width=100, anchor="center")  # Adjusted width
    stored_details_tree.column("Name", width=200, anchor="center")  # Increased width
    stored_details_tree.pack(fill="both", expand=True, padx=20)

    # Fetch and populate preloaded data from the database
    def populate_treeview():
        for item in stored_details_tree.get_children():
            stored_details_tree.delete(item)  # Clear existing data
        try:
            cursor.execute("SELECT code, name FROM main_product")
            for row in cursor.fetchall():
                stored_details_tree.insert("", "end", values=row)
        except sqlite3.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    # Populate Treeview on opening the window
    populate_treeview()

    # Function to delete the selected entry
    def delete_selected_entry():
        selected_item = stored_details_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to delete.")
            return

        # Get the code and name of the selected row
        code, name = stored_details_tree.item(selected_item, 'values')

        try:
            # Delete from database
            cursor.execute("DELETE FROM main_product WHERE code = ?", (code,))
            conn.commit()

            # Delete from treeview
            stored_details_tree.delete(selected_item)

            messagebox.showinfo("Success", f"Product '{name}' deleted successfully!")
        except sqlite3.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    # Add the delete functionality to the "Deletion" radio button
    tk.Button(
        left_frame, 
        text="Delete Selected", 
        font=("Arial", 12), 
        bg="red", 
        fg="white", 
        width=15, 
        command=delete_selected_entry
    ).pack(pady=10)

    # Function to correct the selected entry
    def correct_selected_entry():
        selected_item = stored_details_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row to correct.")
            return

        # Get the current code and name of the selected row
        code, name = stored_details_tree.item(selected_item, 'values')

        # Populate the code and name entry fields for correction
        code_entry.delete(0, tk.END)
        code_entry.insert(0, code)
        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)

        # Update the save button functionality to perform an update on correction
        def update_entry():
            new_code = code_entry.get().strip()
            new_name = name_entry.get().strip()

            if new_code and new_name:
                try:
                    # Update in the database
                    cursor.execute("UPDATE main_product SET code = ?, name = ? WHERE code = ?", 
                                   (new_code, new_name, code))
                    conn.commit()

                    # Update the treeview
                    stored_details_tree.item(selected_item, values=(new_code, new_name))

                    messagebox.showinfo("Success", f"Product '{new_name}' updated successfully!")
                    code_entry.delete(0, tk.END)
                    name_entry.delete(0, tk.END)
                except sqlite3.DatabaseError as e:
                    messagebox.showerror("Database Error", f"Error: {e}")
            else:
                messagebox.showwarning("Input Error", "Please enter both Code and Name")

        # Add the update button
        tk.Button(
            left_frame, 
            text="Update", 
            font=("Arial", 12), 
            bg="green", 
            fg="white", 
            width=10, 
            command=update_entry
        ).pack(pady=10)

    # Add the correction functionality to the "Correction" radio button
    tk.Button(
        left_frame, 
        text="Correct Selected", 
        font=("Arial", 12), 
        bg="blue", 
        fg="white", 
        width=15, 
        command=correct_selected_entry
    ).pack(pady=10)
