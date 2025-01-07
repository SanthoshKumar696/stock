import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

conn = sqlite3.connect('stock.db')
cursor = conn.cursor()


def opening_balance(root):  # Start the opening balance
    opening_balance_window = tk.Toplevel()
    opening_balance_window.title("Party Opening Balance")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    opening_balance_window.geometry(f"{screen_width}x{screen_height}")
    opening_balance_window.configure(bg="lightblue")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_summary(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            DATE TEXT NOT NULL,
            MAIN_LEDGER_NAME TEXT NOT NULL,
            SUB_LEDGER_NAME TEXT NOT NULL,
            WEIGHT REAL NULL,
            AMOUNT REAL NULL)
    """)

    def focus_next_widget(event):
        """Move the focus to the next widget"""
        event.widget.tk_focusNext().focus()
        return "break"

    def save_entry():
        date = date_entry.get()
        main_ledger = main_ledger_combo.get()
        sub_ledger = sub_ledger_combo.get()
        weight = weight_entry.get()
        amount = amount_entry.get()

        cursor.execute("""INSERT INTO customer_summary (DATE, MAIN_LEDGER_NAME, SUB_LEDGER_NAME, WEIGHT, AMOUNT)
                          VALUES (?, ?, ?, ?, ?)""",
                       (date, main_ledger, sub_ledger, weight, amount))
        conn.commit()
        messagebox.showinfo("Success", "Stock saved successfully")
        cancel_entry()

    def correction_entry():
        main_ledger = main_ledger_combo.get()
        sub_ledger = sub_ledger_combo.get()

        cursor.execute("SELECT * FROM customer_summary WHERE MAIN_LEDGER_NAME = ? AND SUB_LEDGER_NAME = ?",
                       (main_ledger, sub_ledger))
        entry = cursor.fetchone()

        if entry:
            # Populate the fields with the fetched data
            date_entry.delete(0, tk.END)
            date_entry.insert(0, entry[1])
            weight_entry.delete(0, tk.END)
            weight_entry.insert(0, entry[4])
            amount_entry.delete(0, tk.END)
            amount_entry.insert(0, entry[5])

            correction_button.config(text="Update", command=lambda: update_entry(entry[0]))
        else:
            messagebox.showinfo("No Data", "No data found for the selected main and sub ledger.")

    def update_entry(entry_id):
        date = date_entry.get()
        main_ledger = main_ledger_combo.get()
        sub_ledger = sub_ledger_combo.get()
        weight = weight_entry.get()
        amount = amount_entry.get()

        cursor.execute("""UPDATE customer_summary SET DATE=?, MAIN_LEDGER_NAME=?, SUB_LEDGER_NAME=?, WEIGHT=?, AMOUNT=?
                          WHERE id=?""",
                       (date, main_ledger, sub_ledger, weight, amount, entry_id))
        conn.commit()
        messagebox.showinfo("Success", "Stock updated successfully")
        cancel_entry()

    def cancel_entry():
        main_ledger_combo.set("")
        sub_ledger_combo.set("")
        weight_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)

        correction_button.config(text="Correction", command=correction_entry)

    def fetch_main_ledger():
        try:
            cursor.execute("SELECT UPPER(name) FROM main_ledger")
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def fetch_sub_ledger(selected_main_ledger):
        try:
            cursor.execute("SELECT UPPER(name) FROM sub_ledger WHERE UPPER(main_ledger)=?", (selected_main_ledger.upper(),))
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return []

    def update_sub_ledger(event):
        selected_main_ledger = main_ledger_combo.get()
        if selected_main_ledger:
            sub_ledger = fetch_sub_ledger(selected_main_ledger)
            sub_ledger_combo['values'] = sub_ledger
            sub_ledger_combo.set("")  # Clear the current selection
        else:
            sub_ledger_combo['values'] = []
            sub_ledger_combo.set("")

    # Variables for input fields
    tk.Label(opening_balance_window, text="Opening Balance", font=("Times", 25, "bold"), bg="lightblue", fg="green").pack(pady=10)

    # Top frame for date, main_ledger, sub_ledger
    top_frame = tk.Frame(opening_balance_window, bg="lightblue")
    top_frame.pack(pady=20)

    # Date entry
    tk.Label(top_frame, text="Date", font=("Times", 15), bg="lightblue").grid(row=0, column=0, padx=10)
    date_entry = tk.Entry(top_frame, font=("Times", 15), width=10, bd=4)
    date_entry.insert(0, datetime.now().strftime('%d-%m-%Y'))
    date_entry.grid(row=1, column=0, padx=10, pady=5)
    date_entry.bind('<Return>', focus_next_widget)

    # Main Ledger
    tk.Label(top_frame, text="Main Ledger", font=("Times", 15), bg="lightblue").grid(row=0, column=1, padx=10)
    main_ledger_combo = ttk.Combobox(top_frame, values=fetch_main_ledger(), state="readonly", width=25, font=("Times", 14))
    main_ledger_combo.grid(row=1, column=1, padx=10)
    main_ledger_combo.bind('<<ComboboxSelected>>', update_sub_ledger)
    main_ledger_combo.bind('<Return>', focus_next_widget)

    # Sub Ledger
    tk.Label(top_frame, text="Sub Ledger Name", font=("Times", 15), bg="lightblue").grid(row=0, column=2, padx=10)
    sub_ledger_combo = ttk.Combobox(top_frame, state="readonly", width=25, font=("Times", 14))
    sub_ledger_combo.grid(row=1, column=2, padx=10)
    sub_ledger_combo.bind('<Return>', focus_next_widget)

    middle_frame = tk.Frame(opening_balance_window, bg="lightblue")
    middle_frame.pack(pady=10)

    # Middle frame with radio buttons and weight/amount fields
    tk.Radiobutton(middle_frame, text="Receipt", font=("Times", 15), bg="lightblue").grid(row=1, column=0, padx=5)
    tk.Radiobutton(middle_frame, text="Issue", font=("Times", 15), bg="lightblue").grid(row=1, column=1, padx=10)

    tk.Label(middle_frame, text="Weight", font=("Times", 15), bg="lightblue").grid(row=0, column=2, padx=10)
    weight_entry = tk.Entry(middle_frame, bd=4, font=("Times", 15))
    weight_entry.grid(row=1, column=2, padx=10)
    weight_entry.bind('<Return>', focus_next_widget)

    tk.Label(middle_frame, text="Amount", font=("Times", 15), bg="lightblue").grid(row=0, column=3, padx=10)
    amount_entry = tk.Entry(middle_frame, bd=4, font=("Times", 15))
    amount_entry.grid(row=1, column=3, padx=10)
    amount_entry.bind('<Return>', focus_next_widget)

    button_frame = tk.Frame(opening_balance_window, bg="lightblue")
    button_frame.pack(pady=10)

    # Buttons for save, correction, cancel, and exit
    tk.Button(button_frame, text="Save", command=save_entry, width=15, bg="purple").grid(row=0, column=0, padx=10)
    correction_button = tk.Button(button_frame, text="Correction", command=correction_entry, width=15, bg="blue")
    correction_button.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Button(button_frame, text="Cancel", command=cancel_entry, width=15, bg="green").grid(row=0, column=2, padx=10)
    tk.Button(button_frame, text="Exit", bg="red", width=15, command=opening_balance_window.destroy).grid(row=0, column=3, padx=10)



