import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database connection
conn = sqlite3.connect('stock.db')
cursor = conn.cursor()

# Create sub_product table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sub_product(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    main_product TEXT,
    code TEXT,
    name TEXT,
    credit_period_days INTEGER,
    FOREIGN KEY (main_product) REFERENCES main_product(name))
""")
conn.commit()

# Fetch main products from the main_product table
def fetch_main_products():
    cursor.execute("SELECT name FROM main_product")
    return [row[0] for row in cursor.fetchall()]

def open_sub_product(root):  # Start the Sub Ledger page

    # Create a new window for Sub Ledger
    sub_product_window = tk.Toplevel(root)
    sub_product_window.title("Sub Product")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    sub_product_window.geometry(f"{screen_width}x{screen_height}")
    sub_product_window.configure(bg="lightblue")

    # Variables for input fields
    main_product_var = tk.StringVar()  # Dropdown selection
    code_var = tk.StringVar()
    name_var = tk.StringVar()
    credit_period_var = tk.StringVar()
    last_name_var = tk.StringVar()

    #
    tk.Label(sub_product_window, text="Sub Product", font=("Times", 25 , "bold"), fg="green", bg="lightblue").grid(row=0, column=0,padx=10, pady=20)


    # Second Line: Main Ledger Dropdown
    tk.Label(
        sub_product_window,
        text="Main Ledger:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=1, column=1, sticky="w", padx=10, pady=10)

    main_product_dropdown = ttk.Combobox(
        sub_product_window,
        textvariable=main_product_var,
        values=fetch_main_products(),
        state="readonly",
        width=30
    )
    main_product_dropdown.grid(row=1, column=2, columnspan=3, padx=10, pady=10)

    # Third Line: Code
    tk.Label(
        sub_product_window,
        text="Code:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=2, column=1, sticky="w", padx=10, pady=10)

    code_entry = tk.Entry(
        sub_product_window,
        textvariable=code_var,
        font=("Arial", 12),
        width=30
    )
    code_entry.grid(row=2, column=2, columnspan=3, padx=10, pady=10)

    # Fourth Line: Name
    tk.Label(
        sub_product_window,
        text="Name:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=3, column=1, sticky="w", padx=10, pady=10)

    name_entry = tk.Entry(
        sub_product_window,
        textvariable=name_var,
        font=("Arial", 12),
        width=30
    )
    name_entry.grid(row=3, column=2, columnspan=3, padx=10, pady=10)

    # Fifth Line: Credit Period
    tk.Label(
        sub_product_window,
        text="Credit Period (Days):",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=4, column=1, sticky="w", padx=10, pady=10)

    credit_period_entry = tk.Entry(
        sub_product_window,
        textvariable=credit_period_var,
        font=("Arial", 12),
        width=30
    )
    credit_period_entry.grid(row=4, column=2, columnspan=3, padx=10, pady=10)

    

    # Right-side Frame to Show Entered Details
    details_frame = tk.Frame(sub_product_window, bg="lightgray", width=400, height=300)
    details_frame.grid(row=0, column=5, rowspan=7, padx=20, pady=10)
    # View Entries Function
    columns = ("Code", "Name")
    stored_details_tree = ttk.Treeview(details_frame, columns=columns, show="headings", height=10)  # Reduced height
    stored_details_tree.heading("Code", text="Code")
    stored_details_tree.heading("Name", text="Name")
    stored_details_tree.column("Code", width=100, anchor="center")  # Adjusted width
    stored_details_tree.column("Name", width=200, anchor="center")  # Increased width
    stored_details_tree.pack(fill="both", expand=True, padx=20)

    def save_entry():
    # Get values from input fields
        main_product = main_product_var.get()
        code = code_var.get().strip()
        name = name_var.get().strip()
        credit_period = credit_period_var.get().strip()

        # Validate required fields
        if not main_product or not code or not name or not credit_period:
            messagebox.showwarning("Input Error", "All fields except 'Last Name' are required.")
            return

        # Validate if credit_period is an integer
        if not credit_period.isdigit():
            messagebox.showerror("Input Error", "Credit Period must be a valid integer.")
            return

        try:
            # Insert data into sub_product table
            cursor.execute(
                "INSERT INTO sub_product (main_product, code, name, credit_period_days) VALUES (?, ?, ?, ?)",
                (main_product, code, name, int(credit_period))
            )
            conn.commit()

            # Clear input fields after saving
            main_product_var.set("")
            code_var.set("")
            name_var.set("")
            credit_period_var.set("")
            last_name_var.set("")

            messagebox.showinfo("Success", "Sub-product saved successfully!")

            # Optionally, update the details frame to reflect new data
            view_entries()

        except sqlite3.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error: {e}")


    def view_entries():
        selected_main_product = main_product_var.get()
        if not selected_main_product:
            messagebox.showwarning("No Selection", "Please select a Main Ledger to view related sub-products.")
            return

        # Clear the treeview before displaying filtered results
        for item in stored_details_tree.get_children():
            stored_details_tree.delete(item)

        try:
            # Fetch and display filtered sub-ledger details
            cursor.execute(
                "SELECT main_product, name FROM sub_product WHERE main_product = ?",
                (selected_main_product,)
            )
            filtered_results = cursor.fetchall()

            if not filtered_results:
                messagebox.showinfo("No Results", f"No sub-products found under '{selected_main_product}'.")
            else:
                for row in filtered_results:
                    stored_details_tree.insert("", "end", values=row)

        except sqlite3.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error: {e}")


    # Function to open a new window with filtered data
    
    # Buttons
    tk.Button(
        sub_product_window,
        text="View",
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=10,
        command=view_entries
    ).grid(row=6, column=4, pady=20)

    tk.Button(
    sub_product_window,
    text="Save",
    font=("Arial", 12),
    bg="green",
    fg="white",
    width=10,
    command=save_entry
    ).grid(row=6, column=1, pady=20)


    tk.Button(
        sub_product_window,
        text="Cancel",
        font=("Arial", 12),
        bg="orange",
        fg="white",
        width=10,
        command=lambda: messagebox.showinfo("Cancel Button", "Cancel functionality pending")
    ).grid(row=6, column=2, pady=20)

    tk.Button(
        sub_product_window,
        text="Exit",
        font=("Arial", 12),
        bg="red",
        fg="white",
        width=10,
        command=sub_product_window.destroy
    ).grid(row=6, column=3, pady=20)


