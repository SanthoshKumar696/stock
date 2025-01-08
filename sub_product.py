import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database connection
conn = sqlite3.connect('stock.db')
cursor = conn.cursor()

# Create the sub_product table again
cursor.execute("""
CREATE TABLE IF NOT EXISTS sub_product(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    main_product TEXT,
    name TEXT,
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
    name_var = tk.StringVar()

    # Variables to track the selected item for correction
    selected_item_id = None

    # Outer frame for the entire window
    outer_frame = tk.Frame(sub_product_window, bg="lightblue")
    outer_frame.grid(row=0, column=1, padx=250, pady=20, sticky="nsew")

    # Title label
    tk.Label(outer_frame, text="Sub Product", font=("Times", 25, "bold"), fg="green", bg="lightblue").grid(row=0, column=0, columnspan=3, padx=10, pady=20)

    # Main Ledger Dropdown (First row)
    tk.Label(outer_frame, text="Main Ledger:", font=("Arial", 12), bg="lightblue").grid(row=1, column=0, sticky="e", padx=10, pady=10)
    main_product_dropdown = ttk.Combobox(outer_frame, textvariable=main_product_var, values=fetch_main_products(), state="readonly", width=30)
    main_product_dropdown.grid(row=1, column=1, padx=10, pady=10)

    # Name (Second row)
    tk.Label(outer_frame, text="Name:", font=("Arial", 12), bg="lightblue").grid(row=2, column=0, sticky="e", padx=10, pady=10)
    name_entry = tk.Entry(outer_frame, textvariable=name_var, font=("Arial", 12), width=30)
    name_entry.grid(row=2, column=1, padx=10, pady=10)

    # Frame for TreeView to show entered data (directly below 'Sub Product' label)
    details_frame = tk.Frame(outer_frame, bg="lightblue")
    details_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    # Define the columns, with Name first and Main Product second
    columns = ("Main Product", "Name")  # Swapped these columns for the desired order
    stored_details_tree = ttk.Treeview(details_frame, columns=columns, show="headings", height=10)
    stored_details_tree.heading("Main Product", text="Main Product")
    stored_details_tree.heading("Name", text="Name")  # Correct header for "Name"
      # Correct header for "Main Product"
    stored_details_tree.column("Name", width=100, anchor="center")
    stored_details_tree.column("Main Product", width=100, anchor="center")
    stored_details_tree.pack(fill="both", expand=True, padx=20)

    # Save Entry function
    def save_entry():
        main_product = main_product_var.get()
        name = name_var.get().strip()

        if not main_product or not name:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            cursor.execute(
                "INSERT INTO sub_product (main_product, name) VALUES (?, ?)",
                (main_product, name)
            )
            conn.commit()
            messagebox.showinfo("Success", "Sub-product saved successfully!")
            name_entry.delete(0, tk.END)
            load_data(main_product)  # Automatically load data after saving
        except sqlite3.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    # Update Entry function (for when the Correction button is clicked after selecting a record)
    def update_entry():
        nonlocal selected_item_id  # Use the selected item ID from the outer scope

        if selected_item_id is None:
            messagebox.showwarning("Selection Error", "Please select an item to update.")
            return

        main_product = main_product_var.get()
        name = name_var.get().strip()

        if not main_product or not name:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            cursor.execute(
                "UPDATE sub_product SET main_product = ?, name = ? WHERE Id = ?",
                (main_product, name, selected_item_id)
            )
            conn.commit()
            messagebox.showinfo("Success", "Sub-product updated successfully!")
            load_data(main_product)  # Reload the data after update
            correction_button.config(text="Correction")  # Change button text back to "Correction"
            selected_item_id = None  # Reset the selected item
        except sqlite3.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    
    def cancel_entry():
        name_var.set("")

        #Reset the correction button text to 
        correction_button.config(text="Correction")

        nonlocal selected_item_id
        selected_item_id=None
        

    # Delete Entry function (for deleting a selected row)
    def delete_entry():
        nonlocal selected_item_id  # Use the selected item ID from the outer scope

        if selected_item_id is None:
            messagebox.showwarning("Selection Error", "Please select an item to delete.")
            return

        try:
            # First, delete from the database using the selected ID
            cursor.execute("DELETE FROM sub_product WHERE Id = ?", (selected_item_id,))
            conn.commit()

            # Then remove the item from the Treeview
            selected_item = stored_details_tree.selection()  # Get selected item in Treeview
            if selected_item:
                stored_details_tree.delete(selected_item)  # Delete the selected row from the Treeview

            messagebox.showinfo("Success", "Sub-product deleted successfully!")

            # Reset selected item ID and button text
            selected_item_id = None
            correction_button.config(text="Correction")  # Reset button text to "Correction"

        except sqlite3.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    # Load data function (runs immediately when a main product is selected)
    def load_data(main_product):
        for item in stored_details_tree.get_children():
            stored_details_tree.delete(item)

        try:
            cursor.execute(
                "SELECT Id, UPPER(name), main_product FROM sub_product WHERE main_product = ?",
                (main_product,)
            )
            filtered_results = cursor.fetchall()

            if not filtered_results:
                messagebox.showinfo("No Results", f"No sub-products found under '{main_product}'.")
            else:
                for row in filtered_results:
                    # Swapped the order of the columns for insertion
                    stored_details_tree.insert("", "end", values=(row[2], row[1], row[0]))  # Displaying 'name' first, then 'main_product'
        except sqlite3.DatabaseError as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    # Automatically load data when a main product is selected
    def on_main_product_selected(event):
        main_product = main_product_var.get()
        if main_product:
            load_data(main_product)

    main_product_dropdown.bind("<<ComboboxSelected>>", on_main_product_selected)

    # Handle row selection in the TreeView
    def on_row_select(event):
        nonlocal selected_item_id  # Use the selected item ID from the outer scope
        selected_item = stored_details_tree.selection()

        if not selected_item:
            return

        item = stored_details_tree.item(selected_item)
        selected_item_id = item['values'][2]  # This should be the ID value from the database
        main_product_var.set(item['values'][1])
        name_var.set(item['values'][0])

        # Change the button text to "Update" when a row is selected
        correction_button.config(text="Update")

    stored_details_tree.bind("<ButtonRelease-1>", on_row_select)

    # Buttons
    button_frame = tk.Frame(outer_frame, bg="lightblue")
    button_frame.grid(row=4, column=0, columnspan=3, pady=20, sticky="nsew")

    save_button = tk.Button(button_frame, text="Save", bg="green", fg="white", width=10, command=save_entry)
    save_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    correction_button = tk.Button(button_frame, text="Correction", bg="orange", fg="white", width=10, command=update_entry)
    correction_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    delete_button = tk.Button(button_frame, text="Delete", bg="red", fg="white", width=10, command=delete_entry)
    delete_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    cancel_button = tk.Button(button_frame, text="Cancel", bg="gray", fg="white", width=10, command=cancel_entry)
    cancel_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

    exit_button = tk.Button(button_frame, text="Exit", bg="red", fg="white", width=10, command=sub_product_window.destroy)
    exit_button.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

    # Make the button frame expand evenly
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)
    button_frame.grid_columnconfigure(3, weight=1)
    button_frame.grid_columnconfigure(4, weight=1)

    # Center the button frame
    outer_frame.grid_rowconfigure(4, weight=1)

