import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from tkinter import Toplevel, Text

def open_sub_ledger(root):
    # Create a new window for Sub Ledger
    sub_ledger_window = tk.Toplevel()
    sub_ledger_window.title("Sub Ledger Master")
    #this function is using Enter button cliking move the next column
    def focus_next_widget(event):
        """Move the focus to the next widget."""
        event.widget.tk_focusNext().focus()
        return "break"

    # Get screen dimensions to make window full size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    sub_ledger_window.geometry(f"{screen_width}x{screen_height}")
    sub_ledger_window.configure(bg="lightblue")

    # Database connection (assuming a database named 'stock.db')
    conn = sqlite3.connect("stock.db")
    cursor = conn.cursor()

    # Create the sub_ledger table (if it doesn't already exist)
    def create_sub_ledger_table():
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sub_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                main_ledger TEXT NOT NULL,
                name TEXT NOT NULL,
                ob_rate_receipt REAL DEFAULT 0.0,
                ob_rate_issue REAL DEFAULT 0.0,
                ob_balance_receipt REAL DEFAULT 0.0,
                ob_balance_issue REAL DEFAULT 0.0,
                entry_date TEXT NOT NULL
            );
        """)
        conn.commit()

    create_sub_ledger_table()

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
    operation_variable_1 = tk.StringVar()  # For OB Rate (Receipt/Issue)
    operation_variable_2 = tk.StringVar()  # For OB Balance (Receipt/Issue)

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
    ob_balance_entry = tk.Entry(main_frame, width=20, justify="center", bd=4, font=("Times", 14), textvariable=ob_balance_var)
    ob_balance_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    ob_balance_entry.bind("<Return>", focus_next_widget)

    # Radio Buttons for "Receipt/Issue" - OB Balance
    tk.Radiobutton(main_frame, text="Receipt", variable=operation_variable_2, value="Receipt", bg="lightblue", font=("Times", 15)).grid(row=4, column=2, padx=20, pady=10, sticky="w")
    tk.Radiobutton(main_frame, text="Issue", variable=operation_variable_2, value="Issue", bg="lightblue", font=("Times", 15)).grid(row=4, column=3, padx=20, pady=10, sticky="w")

    # Save Entry (insert into database)
    def save_entry():
        if main_ledger_var.get() and name_var.get():
            try:
                # Prepare data for receipt/issue (rupees and metal)
                entry_data = {
                    "ob_rate_receipt": ob_rate_var.get() if operation_variable_1.get() == "Receipt" else 0.0,
                    "ob_rate_issue": ob_rate_var.get() if operation_variable_1.get() == "Issue" else 0.0,
                    "ob_balance_receipt": ob_balance_var.get() if operation_variable_2.get() == "Receipt" else 0.0,
                    "ob_balance_issue": ob_balance_var.get() if operation_variable_2.get() == "Issue" else 0.0,
                    "entry_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Check if the customer and the operation already exists
                cursor.execute("""
                    SELECT * FROM sub_ledger WHERE main_ledger = ? AND name = ?
                """, (main_ledger_var.get(), name_var.get()))
                existing_entry = cursor.fetchone()

                if existing_entry:
                    # If exists, update the respective columns based on Receipt/Issue operation
                    cursor.execute("""
                        UPDATE sub_ledger 
                        SET ob_rate_receipt = ?, ob_rate_issue = ?, 
                            ob_balance_receipt = ?, ob_balance_issue = ?, 
                            entry_date = ?
                        WHERE id = ?
                    """, (entry_data["ob_rate_receipt"], entry_data["ob_rate_issue"],
                          entry_data["ob_balance_receipt"], entry_data["ob_balance_issue"],
                          entry_data["entry_date"], existing_entry[0]))
                else:
                    # If no existing entry, insert a new one
                    cursor.execute("""
                        INSERT INTO sub_ledger (main_ledger, name, 
                                                ob_rate_receipt, ob_rate_issue, 
                                                ob_balance_receipt, ob_balance_issue, 
                                                entry_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (main_ledger_var.get(), name_var.get(), 
                          entry_data["ob_rate_receipt"], entry_data["ob_rate_issue"],
                          entry_data["ob_balance_receipt"], entry_data["ob_balance_issue"],
                          entry_data["entry_date"]))

                conn.commit()
                messagebox.showinfo("Saved", "Details Saved Successfully!")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error saving data: {e}")
        else:
            messagebox.showwarning("Missing Fields", "Please fill all the fields!")

    # Button Frame for actions
    button_frame = tk.Frame(main_frame, bg="lightblue")
    button_frame.grid(row=6, column=0, columnspan=5, pady=20)

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

    # Report Generation Function
    def generate_report():
        try:
            cursor.execute("""
                SELECT name, ob_rate_receipt, ob_rate_issue, ob_balance_receipt, ob_balance_issue
                FROM sub_ledger
            """)
            result = cursor.fetchall()

            # Create a new Toplevel window to display the report
            report_window = Toplevel(sub_ledger_window)
            report_window.title("Sub Ledger Report")

            # Add a Text widget to display the report
            report_text = Text(report_window, wrap="word", width=100, height=30, font=("Arial", 12))
            report_text.pack(padx=10, pady=10)

            # Add report header
            report_text.insert(tk.END, f"{'Customer Name':<20}{'Receipt - Rs':<20}{'Receipt - Metal':<20}{'Issue - Rs':<20}{'Issue - Metal':<20}\n")
            report_text.insert(tk.END, "="*100 + "\n")

            # Add data for each customer
            for row in result:
                name, ob_rate_receipt, ob_rate_issue, ob_balance_receipt, ob_balance_issue = row
                report_text.insert(tk.END, f"{name:<20}{ob_rate_receipt:<20}{ob_balance_receipt:<20}{ob_rate_issue:<20}{ob_balance_issue:<20}\n")

            # Disable the text widget so the user can't edit it
            report_text.config(state=tk.DISABLED)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching data: {e}")

    # Generate Report Button
    report_button = tk.Button(
        button_frame,
        text="Generate Report",
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=15,
        command=generate_report
    )
    report_button.grid(row=0, column=4, pady=20, padx=10)

