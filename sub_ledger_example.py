import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def open_sub_ledger(root):
    # Create a new window for Sub Ledger
    sub_ledger_window = tk.Toplevel()
    sub_ledger_window.title("Sub Ledger Master")
    
    # Get screen dimensions to make window full size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    sub_ledger_window.geometry(f"{screen_width}x{screen_height}")
    sub_ledger_window.configure(bg="lightblue")

    # Database connection (assuming a database named 'stock.db')
    conn = sqlite3.connect("stock.db")
    cursor = conn.cursor()

    # Function to fetch Main Ledger values from the database
    def fetch_main_ledger():
        try:
            cursor.execute("SELECT name FROM main_ledger")  # Assuming 'name' field exists in main_ledger table
            result = cursor.fetchall()
            return [row[0].upper() for row in result]  # Convert to uppercase for display
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching data: {e}")
            return []

    # Variables to hold the user input
    main_ledger_var = tk.StringVar()
    name_var = tk.StringVar()
    ob_rate_var = tk.DoubleVar()
    ob_balance_var = tk.DoubleVar()
    credit_days_var = tk.IntVar()
    operation_variable_1 = tk.StringVar()  # For OB Rate
    operation_variable_2 = tk.StringVar()  # For OB Balance

    # Function to move focus to the next widget when Enter is pressed
    def focus_next_widget(event):
        """Move the focus to the next widget."""
        event.widget.tk_focusNext().focus()
        return "break"

    # Frame to hold all widgets (for better organization)
    main_frame = tk.Frame(sub_ledger_window, bg="lightblue")
    main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Label for Sub Ledger
    tk.Label(main_frame, text="Sub Ledger", font=("Times", 25, "bold"), fg="green", bg="lightblue").grid(row=0, column=2, columnspan=2, pady=20)

    # Main Ledger Label and ComboBox
    tk.Label(main_frame, text="Main Ledger", font=("Times", 15), bg="lightblue").grid(row=1, column=0, padx=20, pady=10, sticky="w")
    main_ledger_combo = ttk.Combobox(main_frame, values=fetch_main_ledger(), state="readonly", justify="center", font=("Times", 14), textvariable=main_ledger_var)
    main_ledger_combo.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    main_ledger_combo.bind("<Return>", focus_next_widget)

    # Name Label and Entry
    tk.Label(main_frame, text="Name", font=("Times", 14), bg="lightblue").grid(row=2, column=0, padx=20, pady=10, sticky="w")
    name_entry = tk.Entry(main_frame, width=20, justify="center", bd=4, font=("Times", 14), textvariable=name_var)
    name_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    name_entry.bind("<Return>", focus_next_widget)

    # OB Rate Label and Entry
    tk.Label(main_frame, text="OB in Rs", font=("Times", 15), bg="lightblue").grid(row=3, column=0, padx=20, pady=10, sticky="w")
    ob_rate_entry = tk.Entry(main_frame, width=20, justify="center", bd=4, font=("Times", 14), textvariable=ob_rate_var)
    ob_rate_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    ob_rate_entry.bind("<Return>", focus_next_widget)

    # Radio Buttons for "Receipt/Issue" - OB Rate
    tk.Radiobutton(main_frame, text="Receipt", variable=operation_variable_1, value="Receipt", bg="lightblue", font=("Times", 15)).grid(row=3, column=2, padx=20, pady=10, sticky="w")
    tk.Radiobutton(main_frame, text="Issue", variable=operation_variable_1, value="Issue", bg="lightblue", font=("Times", 15)).grid(row=3, column=3, padx=20, pady=10, sticky="w")

    # OB Balance Label and Entry
    tk.Label(main_frame, text="OB in Metal", font=("Times", 15), bg="lightblue").grid(row=4, column=0, padx=20, pady=10, sticky="w")
    ob_balance_entry = tk.Entry(main_frame, width=20, justify="center", bd=4, font=("Times", 14), textvariable=ob_balance_var, bg="white")
    ob_balance_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    ob_balance_entry.bind("<Return>", focus_next_widget)

    # Radio Buttons for "Receipt/Issue" - OB Balance
    tk.Radiobutton(main_frame, text="Receipt", variable=operation_variable_2, value="Receipt", bg="lightblue", font=("Times", 15)).grid(row=4, column=2, padx=20, pady=10, sticky="w")
    tk.Radiobutton(main_frame, text="Issue", variable=operation_variable_2, value="Issue", bg="lightblue", font=("Times", 15)).grid(row=4, column=3, padx=20, pady=10, sticky="w")

    
    # Details Frame to show entered details
    details_frame = tk.Frame(main_frame, bg="white", width=300, height=300)
    details_frame.grid(row=1, column=5, rowspan=5, padx=20, pady=10, sticky="nsew")

    # Function to display entered details in the details frame
    def display_entered_details():
        main_ledger = main_ledger_var.get()
        name = name_var.get()
        ob_rate = ob_rate_var.get()
        ob_balance = ob_balance_var.get()
        credit_days = credit_days_var.get()
        operation_1 = operation_variable_1.get()
        operation_2 = operation_variable_2.get()

        # Clear previous details
        for widget in details_frame.winfo_children():
            widget.destroy()

        # Display the new details
        details_label = tk.Label(
            details_frame,
            text=f"Main Ledger: {main_ledger}\n"
                 f"Name: {name}\n"
                 f"OB in Rs: {ob_rate}\n"
                 f"OB in Metal: {ob_balance}\n"
                 f"Credit Days: {credit_days}\n"
                 f"Operation (OB Rate): {operation_1}\n"
                 f"Operation (OB Balance): {operation_2}",
            font=("Arial", 12),
            bg="lightgray",
            justify="left"
        )
        details_label.pack(padx=10, pady=10)

    # Save Entry (insert into database)
    def save_entry():
        if main_ledger_var.get() and name_var.get():
            try:
                cursor.execute(""" 
                    INSERT INTO sub_ledger (main_ledger, name, ob_rate, ob_balance, credit_days, operation_1, operation_2)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (main_ledger_var.get(), name_var.get(), ob_rate_var.get(), ob_balance_var.get(), credit_days_var.get(), operation_variable_1.get(), operation_variable_2.get()))
                conn.commit()
                messagebox.showinfo("Saved", "Details Saved Successfully!")
                display_entered_details()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error saving data: {e}")
        else:
            messagebox.showwarning("Missing Fields", "Please fill all the fields!")

    # Button Frame for actions
    button_frame = tk.Frame(main_frame, bg="lightblue")
    button_frame.grid(row=6, column=0, columnspan=5, pady=20)  # Placing the button_frame after other components

    # Buttons
    save_button = tk.Button(
        button_frame,
        text="Save",
        font=("Arial", 12),
        bg="green",
        fg="white",
        width=10,
        command=save_entry
    )
    save_button.grid(row=0, column=0, pady=20, padx=10)

    correction_button = tk.Button(
        button_frame,
        text="Correction",
        font=("Arial", 12),
        bg="orange",
        fg="white",
        width=10,
        command=lambda: messagebox.showinfo("Correction", "Correction logic to be implemented.")
    )
    correction_button.grid(row=0, column=1, pady=20, padx=10)

    exit_button = tk.Button(
        button_frame,
        text="Exit",
        font=("Arial", 12),
        bg="red",
        fg="white",
        width=10,
        command=sub_ledger_window.destroy
    )
    exit_button.grid(row=0, column=2, pady=20, padx=10)

    name_list_button = tk.Button(
        button_frame,
        text="Name List",
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=10,
        command=lambda: messagebox.showinfo("Name List", "Display the name list logic here.")
    )
    name_list_button.grid(row=0, column=3, pady=20, padx=10)
