import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

# Database connection
conn = sqlite3.connect('stock.db')
cursor = conn.cursor()

# Function to focus on the next widget
def focus_next_widget(event):
    """Move the focus to the next widget."""
    event.widget.tk_focusNext().focus()
    return "break"

# Function to handle exit menu action
def exit_program():
    root.quit()

# Create the main root window
root = tk.Tk()
root.title("Jewelry Management System")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.configure(bg="lightpink")

# Create menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Main layout frame
main_frame = tk.Frame(root, bg="lightpink")
main_frame.pack(fill="both", expand=True)

# Left container for widgets
left_container = tk.Frame(main_frame, bg="lightpink", width=screen_width // 2)
left_container.pack(side="left", fill="y", padx=10, pady=10)

# Add a frame for the radio buttons
radio_frame = tk.Frame(left_container, bg="lightpink", bd=2, relief="solid", padx=10, pady=5)
radio_frame.pack(pady=5)

# Radio buttons for Add, Correct, Delete
operation_var = tk.StringVar(value="Add")
tk.Radiobutton(radio_frame, text="Add", variable=operation_var, value="Add", bg="lightpink", font=("Times", 14)).pack(side="left", padx=10)
tk.Radiobutton(radio_frame, text="Correction", variable=operation_var, value="Correction", bg="lightpink", font=("Times", 14)).pack(side="left", padx=10)
tk.Radiobutton(radio_frame, text="Delete", variable=operation_var, value="Delete", bg="lightpink", font=("Times", 14)).pack(side="left", padx=10)

# Top Frame for Basic Details
top_frame = tk.Frame(left_container, bg="lightpink")
top_frame.pack(pady=10)

# Row 1: Date, Transaction, Party Name
tk.Label(top_frame, text="Date", bg="lightpink", font=("Times", 15)).grid(row=0, column=0, padx=10, sticky="e")
date_entry = tk.Entry(top_frame, width=15, justify="center", font=("Times", 14), bd=4)
date_entry.insert(0, datetime.now().strftime("%d-%m-%Y"))
date_entry.grid(row=0, column=1, padx=10)
date_entry.bind("<Return>", focus_next_widget)

tk.Label(top_frame, text="Transaction", bg="lightpink", font=("Times", 15)).grid(row=0, column=2, padx=10, sticky="e")
transaction_combo = ttk.Combobox(top_frame, values=["Cash Receipt", "Cash Payment", "Purchase", "Purchase Return", "Sales", "Sales Return"], width=20, font=("Times", 14))
transaction_combo.grid(row=0, column=3, padx=10)
transaction_combo.bind("<Return>", focus_next_widget)

tk.Label(top_frame, text="Party Name", bg="lightpink", font=("Times", 15)).grid(row=0, column=4, padx=10, sticky="e")
party_entry = tk.Entry(top_frame, width=20, font=("Times", 14), bd=4)
party_entry.grid(row=0, column=5, padx=10)
party_entry.bind("<Return>", focus_next_widget)

# Middle Frame for Product Details
middle_frame = tk.Frame(left_container, bg="lightpink")
middle_frame.pack(pady=10)

# Labels and Entries
columns = [
    ("Main Product", 20), 
    ("Design", 20), 
    ("Gross Wt", 10), 
    ("Stones", 10),
    ("Touch", 10),
    ("Net Wt", 10),
    ("MC@", 10),
    ("MC", 10)
]

for i, (label, width) in enumerate(columns):
    tk.Label(middle_frame, text=label, bg="lightpink", font=("Times", 15)).grid(row=0, column=i, padx=10, sticky="w")
    tk.Entry(middle_frame, width=width, font=("Times", 14), bd=4).grid(row=1, column=i, padx=10, pady=5)

# Frame for Treeview and Scrollbars
tree_frame = tk.Frame(left_container, bg="lightpink", width=600, height=400)
tree_frame.pack(pady=10)

# Create Treeview widget
columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#12", "#13", "#14", "#15")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)

# Set headings
for col in columns:
    tree.heading(col, text=col)

# Add scrollbars
x_scrollbar = tk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
y_scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

tree.grid(row=0, column=0, sticky="nsew")
x_scrollbar.grid(row=1, column=0, sticky="ew")
y_scrollbar.grid(row=0, column=1, sticky="ns")

# Footer Frame for Buttons
footer_frame = tk.Frame(left_container, bg="lightpink")
footer_frame.pack(pady=20)

tk.Button(footer_frame, text="Add", width=12, bg="green", fg="white").grid(row=0, column=0, padx=10)
tk.Button(footer_frame, text="Delete", width=12, bg="red", fg="white").grid(row=0, column=1, padx=10)
tk.Button(footer_frame, text="Save", width=12, bg="blue", fg="white").grid(row=0, column=2, padx=10)

# Right container for future use
right_container = tk.Frame(main_frame, bg="lightpink", width=screen_width // 2)
right_container.pack(side="right", fill="both", expand=True)

root.mainloop()
