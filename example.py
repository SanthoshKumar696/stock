import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Function to connect to the database
def connect_database():
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    return conn, cursor

# Focus next widget function to move to the next entry field
def focus_next_widget(event):
    """ Move to the Next Widget """
    event.widget.tk_focusNext().focus()

# Function to display the day book window
def day_book(root):
    conn, cursor = connect_database()

    # Create a new window
    day_book_window = tk.Toplevel()
    day_book_window.title("Day Book")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    day_book_window.geometry(f"{screen_width}x{screen_height}")  # Correct geometry format
    day_book_window.configure(bg="lightblue")

    def fetch_transactions(cursor, from_date, to_date):
        try:
            # Check if the dates are in the correct format (DD-MM-YYYY)
            datetime.strptime(from_date, "%d-%m-%Y")  # Check format of from_date
            datetime.strptime(to_date, "%d-%m-%Y")    # Check format of to_date

            print(f"Fetching transactions from {from_date} to {to_date}")
            

            # Execute the query using the dates as they are (DD-MM-YYYY)
            cursor.execute(
                "SELECT * FROM saved_data WHERE date BETWEEN ? AND ? ORDER BY date",
                (from_date, to_date)  # Use dates as they are in DD-MM-YYYY format
            )
            rows = cursor.fetchall()

            print(f"Transactions fetched: {rows}")

            return rows
        except ValueError as e:
            messagebox.showerror("Date Error", f"Invalid date format! Use DD-MM-YYYY. Error: {e}")
            return []

    # Function to generate and show the report
    # In the show_report function, you don't need to change the date format for display
    def show_report():
        from_date = from_date_entry.get()
        to_date = to_date_entry.get()

        if not from_date or not to_date:
            messagebox.showerror("Input Error", "Both dates are required!")
            return

        # Fetch transactions using the fetch_transactions function
        transactions = fetch_transactions(cursor, from_date, to_date)
        if transactions:
            report_window = tk.Toplevel(day_book_window)
            report_window.title("Transaction Report")
            
            report_window.configure(bg="lightblue")

            # Define TreeView columns
            columns = (
                "ID", "Date", "Party Name", "Transaction", "Main Product", "Sub Product",
                "Gross Wt", "Stones", "Touch", "Net Wt", "MC@", "MC", "Rate", "Amount", "Narration"
            )
            tree = ttk.Treeview(report_window, columns=columns, show="headings")
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=1)

            # Insert data into the TreeView, keeping the date in DD-MM-YYYY format
            for row in transactions:
                tree.insert("", tk.END, values=row)

            tree.pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showinfo("No Data", "No transactions found for the given date range.")

    # GUI layout
    tk.Label(
        day_book_window,
        text="Day Book",
        font=("Arial", 24, "bold"),
        bg="lightblue",
        fg="darkblue"
    ).pack(pady=10)

    # Input fields
    input_frame = tk.Frame(day_book_window, bg="lightblue")
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="From Date (DD-MM-YYYY):", bg="lightblue", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
    from_date_entry = tk.Entry(input_frame, font=("Arial", 14), width=15, bd=3)
    from_date_entry.grid(row=0, column=1)
    from_date_entry.bind('<Return>', focus_next_widget)

    tk.Label(input_frame, text="To Date (DD-MM-YYYY):", bg="lightblue", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5)
    to_date_entry = tk.Entry(input_frame, font=("Arial", 14), width=15, bd=3)
    to_date_entry.grid(row=1, column=1)

    # Buttons
    button_frame = tk.Frame(day_book_window, bg="lightblue")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Report", bg="green", fg="white", font=("Arial", 12), command=show_report).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Clear", bg="orange", fg="white", font=("Arial", 12),
              command=lambda: [from_date_entry.delete(0, tk.END), to_date_entry.delete(0, tk.END)]).grid(row=0, column=1, padx=10)
    tk.Button(button_frame, text="Exit", bg="red", fg="white", font=("Arial", 12), command=day_book_window.destroy).grid(row=0, column=2, padx=10)

