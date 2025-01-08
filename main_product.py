import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def open_main_product(root):
    # Create a new window for Main Ledger
    main_ledger_window = tk.Toplevel()
    main_ledger_window.title("Main Ledger Master")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    main_ledger_window.geometry(f"{screen_width}x{screen_height}")
    main_ledger_window.configure(bg="lightblue")

    # Database connection
    conn = sqlite3.connect("stock.db")
    cursor = conn.cursor()


    # Create table if not exists
    cursor.execute("""CREATE TABLE IF NOT EXISTS main_product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )""")
    conn.commit()

    # String variables for name entry and buttons' state
    name_var = tk.StringVar()
    correction_id = None  # To hold the ID of the record being corrected

    # Outer frame to hold everything
    outer_frame = tk.Frame(main_ledger_window, bg="lightblue")
    outer_frame.grid(row=0, column=1, padx=250, pady=20, sticky="nsew")

    # Title Label for "Main Ledger Master"
    main_ledger_label = tk.Label(outer_frame, text="Main Product", font=("Times", 25, "bold"), fg="green", bg="lightblue")
    main_ledger_label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

    # Name Entry Label and Entry Field
    tk.Label(outer_frame, text="Name:", font=("Times", 20), bg="lightblue").grid(row=1, column=0, padx=5, pady=10, sticky="e")
    name_entry = tk.Entry(outer_frame, textvariable=name_var, font=("Times", 16), bd=4, width=30)
    name_entry.grid(row=1, column=1, padx=2, pady=10)

    # Treeview for displaying names
    columns = ("Name",)
    treeview_frame = tk.Frame(outer_frame, bg="lightblue")
    treeview_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

    # Treeview for displaying the names
    name_treeview = ttk.Treeview(treeview_frame, columns=columns, show="headings", height=10)
    name_treeview.heading("Name", text="Name")
    name_treeview.column("Name", width=200, anchor="center")
    name_treeview.grid(row=0, column=0, padx=10, pady=10)

    # Function to fetch and display names in Treeview
    def update_name_treeview():
        for item in name_treeview.get_children():
            name_treeview.delete(item)  # Clear existing data
        cursor.execute("SELECT UPPER(name) FROM main_product")
        names = cursor.fetchall()
        for name in names:
            name_treeview.insert("", "end", values=(name[0].upper(),))  # Display names in uppercase

    # Display the names in the Treeview initially
    update_name_treeview()

    # Show Names List and handle selection
    def on_name_selected(event):
        nonlocal correction_id  # Use the outer correction_id
        selected_name = name_treeview.item(name_treeview.selection(), 'values')[0].lower()  # Get selected name
        cursor.execute("SELECT id, name FROM main_product WHERE LOWER(name) = ?", (selected_name,))
        row = cursor.fetchone()
        if row:
            correction_id = row[0]
            name_var.set(row[1])  # Set the selected name into the entry field

    # Bind the selection event of the Treeview
    name_treeview.bind("<<TreeviewSelect>>", on_name_selected)

    # Save Entry
    def save_entry():
        if name_var.get():
            try:
                cursor.execute("INSERT INTO main_product (name) VALUES (?)", (name_var.get(),))
                conn.commit()
                messagebox.showinfo("Saved", "Details Saved Successfully!")
                update_name_treeview()  # Update the treeview after saving
                name_var.set("")  # Clear the entry field after saving
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
        else:
            messagebox.showwarning("Missing Fields", "Please fill all the fields!")

    # Update Entry
    def update_entry():
        nonlocal correction_id  # Use the outer correction_id
        if correction_id:
            new_name = name_var.get()
            if new_name:
                try:
                    cursor.execute("UPDATE main_product SET name = ? WHERE id = ?", (new_name, correction_id))
                    conn.commit()
                    messagebox.showinfo("Updated", "Record updated successfully!")
                    update_name_treeview()  # Update the treeview after updating
                    name_var.set("")  # Clear the entry field after updating
                    correction_id = None  # Reset the correction ID
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"Error: {e}")
            else:
                messagebox.showwarning("Missing Fields", "Please fill all the fields!")
        else:
            messagebox.showwarning("No Selection", "Please select a record to correct.")

    # Delete Entry
    def delete_entry():
        nonlocal correction_id  # Use the outer correction_id
        if correction_id:
            try:
                cursor.execute("DELETE FROM main_product WHERE id = ?", (correction_id,))
                conn.commit()
                messagebox.showinfo("Deleted", "Record deleted successfully!")
                update_name_treeview()  # Update the treeview after deleting
                name_var.set("")  # Clear the entry field after deleting
                correction_id = None  # Reset the correction ID
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
        else:
            messagebox.showwarning("No Selection", "Please select a record to delete.")

    # Cancel Action
    def cancel_action():
        nonlocal correction_id
        name_var.set("")  # Clear the entry field
        correction_id = None  # Clear the correction ID

    # Create a frame for the buttons
    button_frame = tk.Frame(outer_frame, bg="lightblue")
    button_frame.grid(row=2, column=0, columnspan=3, pady=20, sticky="nsew")

    # Buttons inside the button frame
    save_button = tk.Button(button_frame, text="Save", bg="green", fg="white", width=10, command=save_entry)
    save_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    update_button = tk.Button(button_frame, text="Correction", bg="orange", fg="white", width=10, command=update_entry)
    update_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    delete_button = tk.Button(button_frame, text="Delete", bg="blue", fg="white", width=10, command=delete_entry)
    delete_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    cancel_button = tk.Button(button_frame, text="Cancel", bg="gray", fg="white", width=10, command=cancel_action)
    cancel_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

    exit_button = tk.Button(button_frame, text="Exit", bg="red", fg="white", width=10, command=lambda: (conn.close(), main_ledger_window.destroy()))
    exit_button.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

    # Make the button frame expand evenly and center it
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)
    button_frame.grid_columnconfigure(3, weight=1)
    button_frame.grid_columnconfigure(4, weight=1)

    # Center the button frame in the main window
    outer_frame.grid_rowconfigure(2, weight=1)


