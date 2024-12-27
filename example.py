import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# Create a table for demonstration purposes
cursor.execute("""
CREATE TABLE IF NOT EXISTS saved_data (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    "transaction" TEXT,
    name TEXT,
    main_product TEXT,
    sub_product TEXT,
    gross_wt REAL,
    stones REAL,
    touch REAL,
    net_wt REAL,
    mc_at TEXT,
    mc TEXT,
    rate REAL,
    amount REAL,
    narration TEXT
)
""")
conn.commit()

# Initialize the main application window
root = tk.Tk()
root.title("Operation Application")
root.geometry("800x600")

# Screen width for layout
screen_width = 400

# Left container for operations
left_container = tk.Frame(root, bg="lightpink", width=screen_width)
left_container.pack(side="left", fill="y", padx=10, pady=10)

# Add a frame for the radio buttons
radio_frame = tk.Frame(left_container, bg="lightpink", bd=2, relief="solid", padx=10, pady=5)
radio_frame.pack(pady=5)

# Default operation variable
operation_var = tk.StringVar(value="Add")

# Radio buttons for Add, Correction, Delete
tk.Radiobutton(radio_frame, text="Add", variable=operation_var, value="Add", bg="lightpink", font=("Times", 14)).pack(side="left", padx=10)
tk.Radiobutton(radio_frame, text="Correction", variable=operation_var, value="Correction", bg="lightpink", font=("Times", 14)).pack(side="left", padx=10)
tk.Radiobutton(radio_frame, text="Delete", variable=operation_var, value="Delete", bg="lightpink", font=("Times", 14)).pack(side="left", padx=10)

# Input fields
date_entry = tk.Entry(left_container, font=("Times", 14))
date_entry.pack(pady=5)
party_entry = tk.Entry(left_container, font=("Times", 14))
party_entry.pack(pady=5)

transaction_combo = ttk.Combobox(left_container, values=["Sale", "Purchase"], font=("Times", 14))
transaction_combo.pack(pady=5)

main_product_combo = ttk.Combobox(left_container, values=["Gold", "Silver"], font=("Times", 14))
main_product_combo.pack(pady=5)

sub_product_combo = ttk.Combobox(left_container, values=["Ring", "Necklace"], font=("Times", 14))
sub_product_combo.pack(pady=5)

gross_wt_entry = tk.Entry(left_container, font=("Times", 14))
gross_wt_entry.pack(pady=5)
stones_entry = tk.Entry(left_container, font=("Times", 14))
stones_entry.pack(pady=5)
touch_entry = tk.Entry(left_container, font=("Times", 14))
touch_entry.pack(pady=5)

mc_at_entry = tk.Entry(left_container, font=("Times", 14))
mc_at_entry.pack(pady=5)
mc_entry = tk.Entry(left_container, font=("Times", 14))
mc_entry.pack(pady=5)

rate_entry = tk.Entry(left_container, font=("Times", 14))
rate_entry.pack(pady=5)

narration_entry = tk.Entry(left_container, font=("Times", 14))
narration_entry.pack(pady=5)

# Treeview to display saved data
columns = ("sl_no", "date", "name", "main_product", "sub_product", "transaction", "gross_wt", "stones", "touch", "net_wt", "mc_at", "mc", "rate", "amount", "narration")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
tree.pack(side="right", fill="both", expand=True)

for col in columns:
    tree.heading(col, text=col)

# Functionality for adding items
def add_item():
    cursor.execute("SELECT MAX(ID) FROM saved_data")
    max_id = cursor.fetchone()[0]
    sl_no = (max_id + 1) if max_id else 1
    date = date_entry.get()
    name = party_entry.get()
    transaction = transaction_combo.get()
    main_product = main_product_combo.get()
    sub_product = sub_product_combo.get()
    try:
        gross_wt = float(gross_wt_entry.get())
        stones = float(stones_entry.get())
        touch = float(touch_entry.get())
        rate = float(rate_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter numeric values for weights, touch, and rate.")
        return

    mc_at = mc_at_entry.get()
    mc = mc_entry.get()
    narration = narration_entry.get()

    adjusted_wt = gross_wt - stones
    net_wt = adjusted_wt * (touch / 100)
    amount = net_wt * rate

    if name and transaction:
        tree.insert("", "end", values=(sl_no, date, name, main_product, sub_product, transaction, gross_wt, stones, touch, net_wt, mc_at, mc, rate, amount, narration))
        clear_fields()

        try:
            cursor.execute("""
            INSERT INTO saved_data (date, "transaction", name, main_product, sub_product, gross_wt, stones, touch, net_wt, mc_at, mc, rate, amount, narration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (date, transaction, name, main_product, sub_product, gross_wt, stones, touch, net_wt, mc_at, mc, rate, amount, narration))
            conn.commit()
            messagebox.showinfo("Success", "Receipt saved successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
    else:
        messagebox.showerror("Input Error", "Please fill all required fields.")

# Function to clear input fields
def clear_fields():
    date_entry.delete(0, tk.END)
    party_entry.delete(0, tk.END)
    transaction_combo.set("")
    main_product_combo.set("")
    sub_product_combo.set("")
    gross_wt_entry.delete(0, tk.END)
    stones_entry.delete(0, tk.END)
    touch_entry.delete(0, tk.END)
    mc_at_entry.delete(0, tk.END)
    mc_entry.delete(0, tk.END)
    rate_entry.delete(0, tk.END)
    narration_entry.delete(0, tk.END)

# Function to handle operations
def perform_operation():
    if operation_var.get() == "Add":
        add_item()
    else:
        messagebox.showinfo("Operation", f"{operation_var.get()} functionality is not implemented yet!")

# Button to trigger operation
action_button = tk.Button(left_container, text="Perform Operation", command=perform_operation, bg="lightblue", font=("Times", 14))
action_button.pack(pady=10)

# Start the application
root.mainloop()
