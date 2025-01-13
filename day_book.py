import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Function to connect to the database
def connect_database():
    conn = sqlite3.connect('stock.db')
    cursor = conn.cursor()
    return conn, cursor

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()

# Function to fetch transactions from the database
def fetch_transactions(cursor, from_date, to_date):
    try:
        # Check if the dates are in the correct format (DD-MM-YYYY)
        datetime.strptime(from_date, "%d-%m-%Y")  # Check format of from_date
        datetime.strptime(to_date, "%d-%m-%Y")    # Check format of to_date
         # Convert from_date and to_date to YYYY-MM-DD format
        from_date = datetime.strptime(from_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%d-%m-%Y").strftime("%Y-%m-%d")

        cursor.execute(
            "SELECT * FROM saved_data WHERE date BETWEEN ? AND ? ORDER BY date",
            (from_date, to_date)
        )
        rows = cursor.fetchall()
        return rows
    except ValueError as e:
        messagebox.showerror("Date Error", f"Invalid date format! Use DD-MM-YYYY. Error: {e}")
        return []

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

    def show_report():
        from_date = from_date_entry.get()
        to_date = to_date_entry.get()

        if not from_date or not to_date:
            messagebox.showerror("Input Error", "Both dates are required!")
            return

        transactions = fetch_transactions(cursor, from_date, to_date)
        if transactions:
            update_treeview(transactions)
        else:
            messagebox.showinfo("No Data", "No transactions found for the given date range.")

    def update_treeview(transactions):
        # Clear existing rows in the Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Insert the fetched data into the Treeview with different row colors
        for index, row in enumerate(transactions):
            # Apply alternate row colors (light gray for even, white for odd)
            if index % 2 == 0:
                row_color = "#f0f0f0"  # Light gray for even rows
            else:
                row_color = "white"  # White for odd rows

            tree.insert("", "end", values=row, tags=("row_color",))
            tree.tag_configure("row_color", background=row_color)

            # Apply specific styling for the 'Transaction' column based on its value
            if "Sale" in row[3]:  # Assuming the 'Transaction' column is at index 3
                tree.item(tree.get_children()[-1], tags=("transaction_sale",))
                tree.tag_configure("transaction_sale", foreground="green")
            elif "Purchase" in row[3]:
                tree.item(tree.get_children()[-1], tags=("transaction_purchase",))
                tree.tag_configure("transaction_purchase", foreground="red")

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

    tk.Button(button_frame, text="Generate Report", bg="green", fg="white", font=("Arial", 12), command=show_report).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Clear", bg="orange", fg="white", font=("Arial", 12),
              command=lambda: [from_date_entry.delete(0, tk.END), to_date_entry.delete(0, tk.END)]).grid(row=0, column=1, padx=10)
    tk.Button(button_frame, text="Exit", bg="red", fg="white", font=("Arial", 12), command=day_book_window.destroy).grid(row=0, column=2, padx=10)

    # Frame for Treeview and Scrollbar
    frame = tk.Frame(day_book_window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Treeview for displaying transactions
    columns = ("ID", "Date", "Party Name", "Transaction", "Main Product", "Sub Product", "Gross Wt", "Stones", 
               "Touch", "Net Wt", "MC@", "MC", "Rate", "Amount", "Narration")
    tree = ttk.Treeview(frame, columns=columns, show="headings")

    # Create a unique style for this Treeview widget
    style = ttk.Style()
    style.configure("custom.Treeview.Heading",
                    font=("Times", 13, "bold"),  # Font for the headings with larger size
                    background="yellow",  # Green background for headings
                    foreground="black", relief="flat")  # White text color for headings

    style.configure("custom.Treeview",
                    font=("Times", 12),  # Font size for the rows
                    rowheight=30)  # Increase row height to accommodate larger text

    # Apply the unique style to the Treeview
    tree.tag_configure("row_color", background="white")
    tree.configure(style="custom.Treeview")

    # Style columns
    tree.heading("ID", text="ID", anchor="center")
    tree.column("ID", width=70, anchor="center")  # Reduced width for ID
    tree.heading("Date", text="Date", anchor="center")
    tree.column("Date", width=100, anchor="w")  # Reduced width for Date
    tree.heading("Party Name", text="Party Name", anchor="center")
    tree.column("Party Name", width=150, anchor="w")
    tree.heading("Transaction", text="Transaction", anchor="center")
    tree.column("Transaction", width=120, anchor="center")
    tree.heading("Main Product", text="Main Product", anchor="center")
    tree.column("Main Product", width=150, anchor="center")
    tree.heading("Sub Product", text="Sub Product", anchor="center")
    tree.column("Sub Product", width=150, anchor="center")
    tree.heading("Gross Wt", text="Gross Wt", anchor="center")
    tree.column("Gross Wt", width=100, anchor="center")
    tree.heading("Stones", text="Stones", anchor="center")
    tree.column("Stones", width=80, anchor="w")  # Reduced width for Stones
    tree.heading("Touch", text="Touch", anchor="center")
    tree.column("Touch", width=80, anchor="center")  # Reduced width for Touch
    tree.heading("Net Wt", text="Net Wt", anchor="center")
    tree.column("Net Wt", width=100, anchor="center")
    tree.heading("MC@", text="MC@", anchor="center")
    tree.column("MC@", width=80, anchor="w")  # Reduced width for MC@
    tree.heading("MC", text="MC", anchor="center")
    tree.column("MC", width=80, anchor="w")  # Reduced width for MC
    tree.heading("Rate", text="Rate", anchor="center")
    tree.column("Rate", width=100, anchor="center")
    tree.heading("Amount", text="Amount", anchor="center")
    tree.column("Amount", width=100, anchor="center")
    tree.heading("Narration", text="Narration", anchor="center")
    tree.column("Narration", width=200, anchor="w")

    tree.grid(row=0, column=0, sticky="nsew")

    # Adding a horizontal scrollbar
    x_scroll = tk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    x_scroll.grid(row=1, column=0, sticky="ew")
    tree.configure(xscrollcommand=x_scroll.set)

    # Configure row and column weights for resizing
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

# Main window for starting the application