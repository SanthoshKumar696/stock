import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def open_main_ledger(root):
    # Create a new window for Main Ledger
    main_ledger_window = tk.Toplevel()
    main_ledger_window.title("Main Product Master")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    main_ledger_window.geometry(f"{screen_width}x{screen_height}")
    main_ledger_window.configure(bg="lightblue")

    # Database connection
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS main_ledger (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operation TEXT,
        main_ledger TEXT,
        code TEXT,
        name TEXT
    )
    """)
    conn.commit()

    # Variables for input fields
    operation_var = tk.StringVar(value="Addition")  # Default radio button selection
    main_ledger_var = tk.StringVar()  # Dropdown selection
    code_var = tk.StringVar()
    name_var = tk.StringVar()

    # Title Label
    main_ledger_label = tk.Label(
        main_ledger_window, 
        text="Main Ledger Master", 
        font=("Times", 25, "bold"), 
        fg="black", 
        bg="lightblue"
    )
    main_ledger_label.grid(row=0, column=0, columnspan=8, pady=10)

    # Operation Radio Buttons
    tk.Label(
        main_ledger_window,
        text="Select Operation:",
        font=("Arial", 12, "bold"),
        bg="lightblue"
    ).grid(row=1, column=0, sticky="w", padx=10, pady=10)

    operations = ["Addition", "Correction", "Deletion", "View"]
    for i, operation in enumerate(operations):
        tk.Radiobutton(
            main_ledger_window,
            text=operation,
            variable=operation_var,
            value=operation,
            font=("Arial", 10),
            bg="lightblue"
        ).grid(row=1, column=i + 1, padx=10)

    # Main Ledger Dropdown
    tk.Label(
        main_ledger_window,
        text="Main Ledger:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=2, column=0, sticky="w", padx=10, pady=10)

    main_ledger_dropdown = ttk.Combobox(
        main_ledger_window,
        textvariable=main_ledger_var,
        values=["Ledger A", "Ledger B", "Ledger C"],  # Example options
        font=("Arial", 12),
        width=28
    )
    main_ledger_dropdown.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

    # Code Entry
    tk.Label(
        main_ledger_window,
        text="Code:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=3, column=0, sticky="w", padx=10, pady=10)

    code_entry = tk.Entry(
        main_ledger_window,
        textvariable=code_var,
        font=("Arial", 12),
        width=30
    )
    code_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

    # Name Entry
    tk.Label(
        main_ledger_window,
        text="Name:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=4, column=0, sticky="w", padx=10, pady=10)

    name_entry = tk.Entry(
        main_ledger_window,
        textvariable=name_var,
        font=("Arial", 12),
        width=30
    )
    name_entry.grid(row=4, column=1, columnspan=3, padx=10, pady=10)

    # Right-side Frame for Details
    details_frame = tk.Frame(main_ledger_window, bg="lightgray", width=400, height=300)
    details_frame.grid(row=1, column=4, rowspan=7, padx=20, pady=10)

    # Display Entered Details
    def display_entered_details():
        operation = operation_var.get()
        main_ledger = main_ledger_var.get()
        code = code_var.get()
        name = name_var.get()

        # Clear previous details
        for widget in details_frame.winfo_children():
            widget.destroy()

        details_label = tk.Label(
            details_frame,
            text=f"Operation: {operation}\n"
                 f"Main Ledger: {main_ledger}\n"
                 f"Code: {code}\n"
                 f"Name: {name}\n",
            font=("Arial", 12),
            bg="lightgray",
            justify="left"
        )
        details_label.pack(padx=10, pady=10)

    # Save Entry
    def save_entry():
        if operation_var.get() and main_ledger_var.get() and code_var.get() and name_var.get():
            try:
                cursor.execute("""
                INSERT INTO main_ledger (operation, main_ledger, code, name)
                VALUES (?, ?, ?, ?)
                """, (operation_var.get(), main_ledger_var.get(), code_var.get(), name_var.get()))
                conn.commit()
                messagebox.showinfo("Saved", "Details Saved Successfully!")
                display_entered_details()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
        else:
            messagebox.showwarning("Missing Fields", "Please fill all the fields!")

    # Cancel Entry
    def cancel_entry():
        operation_var.set("Addition")
        main_ledger_var.set("")
        code_var.set("")
        name_var.set("")

    # Show Name List
    def show_name_list():
        cursor.execute("SELECT name FROM main_ledger")
        names = cursor.fetchall()
        names_list = "\n".join([name[0] for name in names]) if names else "No names found."
        messagebox.showinfo("Name List", f"Names:\n{names_list}")

    # Buttons
    tk.Button(
        main_ledger_window,
        text="Save",
        font=("Arial", 12),
        bg="green",
        fg="white",
        width=10,
        command=save_entry
    ).grid(row=7, column=0, pady=20)

    tk.Button(
        main_ledger_window,
        text="Cancel",
        font=("Arial", 12),
        bg="orange",
        fg="white",
        width=10,
        command=cancel_entry
    ).grid(row=7, column=1, pady=20)

    tk.Button(
        main_ledger_window,
        text="Exit",
        font=("Arial", 12),
        bg="red",
        fg="white",
        width=10,
        command=lambda: (conn.close(), main_ledger_window.destroy())
    ).grid(row=7, column=2, pady=20)

    tk.Button(
        main_ledger_window,
        text="Name List",
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=10,
        command=show_name_list
    ).grid(row=7, column=3, pady=20)
