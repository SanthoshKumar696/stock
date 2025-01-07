import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database Connection
conn = sqlite3.connect("stock.db")
cursor = conn.cursor()



# Ensure the tables exist
cursor.execute('''CREATE TABLE IF NOT EXISTS opening_stock (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    main_product TEXT, 
                    sub_product TEXT,
                    pcs INTEGER,
                    gross_wt REAL,
                    melting REAL, 
                    net_wt REAL,
                    rate REAL,
                    mc_at REAL)''')

# Create the main GUI window
def opening_stock(root):
    # Create the Toplevel window
    opening_stock_window = tk.Toplevel(root)
    opening_stock_window.title("Opening Stock")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    opening_stock_window.geometry(f"{screen_width}x{screen_height}")  # Set to screen size
    opening_stock_window.configure(bg="lightblue")

    # focus_next_widget move to another target
    def focus_next_widget(event):
        """ Move to next focus widget """
        event.widget.tk_focusNext().focus()
        return "break"
    

    # Function to fetch main products (in uppercase)
    def fetch_main_products():
        try:
            cursor.execute("SELECT UPPER(name) FROM main_product")
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return []
        
    def fetch_sub_product(selected_main_product):
        try:
            cursor.execute("SELECT UPPER(name) FROM sub_product WHERE UPPER(main_product) = ?", (selected_main_product.upper(),))
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return []

    def update_sub_products(event):
        selected_main_product = main_product_combo.get()
        if selected_main_product:
            sub_products = fetch_sub_product(selected_main_product)
            sub_product_combo['values'] = sub_products
            sub_product_combo.set("")  # Clear the current selection
        else:
            sub_product_combo['values'] = []
            sub_product_combo.set("")  # Clear the selection if no main product is chosen

    # Save entry to database
    def save_entry():
        main_product = main_product_var.get()
        sub_product = sub_product_var.get()
        pcs = pcs_entry.get()
        gross_wt = gross_wt_entry.get()
        melting = melting_entry.get()
        net_wt = net_wt_entry.get()
        rate = rate_entry.get()
        mc_at = mc_at_entry.get()

        # Ensure all fields are filled
        if not all([main_product, sub_product, pcs, gross_wt, melting, net_wt, rate, mc_at]):
            messagebox.showwarning("Input Error", "All fields must be filled")
            return

        # Insert the data into the opening_stock table
        cursor.execute("""INSERT INTO opening_stock (main_product, sub_product, pcs, gross_wt, melting, net_wt, rate, mc_at) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                        (main_product, sub_product, pcs, gross_wt, melting, net_wt, rate, mc_at))
        conn.commit()
        messagebox.showinfo("Success", "Stock saved successfully!")
        cancel_entry()

    # Correction to update the entry
    def correction_entry():
        main_product = main_product_var.get()
        sub_product = sub_product_var.get()

        if not main_product or not sub_product:
            messagebox.showwarning("Selection Error", "Please select both main and sub product to edit.")
            return

        cursor.execute("SELECT * FROM opening_stock WHERE main_product = ? AND sub_product = ?", (main_product, sub_product))
        entry = cursor.fetchone()

        if entry:
            # Populate the fields with the fetched data
            pcs_entry.delete(0, tk.END)
            pcs_entry.insert(0, entry[3])
            gross_wt_entry.delete(0, tk.END)
            gross_wt_entry.insert(0, entry[4])
            melting_entry.delete(0, tk.END)
            melting_entry.insert(0, entry[5])
            net_wt_entry.delete(0, tk.END)
            net_wt_entry.insert(0, entry[6])
            rate_entry.delete(0, tk.END)
            rate_entry.insert(0, entry[7])
            mc_at_entry.delete(0, tk.END)
            mc_at_entry.insert(0, entry[8])

            # Change the correction button text to "Update"
            correction_button.config(text="Update", command=lambda: update_entry(entry[0]))
        else:
            messagebox.showinfo("No Data", "No data found for the selected main and sub product.")

    # Update the existing entry in database
    def update_entry(entry_id):
        main_product = main_product_var.get()
        sub_product = sub_product_var.get()
        pcs = pcs_entry.get()
        gross_wt = gross_wt_entry.get()
        melting = melting_entry.get()
        net_wt = net_wt_entry.get()
        rate = rate_entry.get()
        mc_at = mc_at_entry.get()

        cursor.execute("""UPDATE opening_stock SET pcs = ?, gross_wt = ?, melting = ?, net_wt = ?, rate = ?, mc_at = ? 
                        WHERE id = ?""", 
                        (pcs, gross_wt, melting, net_wt, rate, mc_at, entry_id))
        conn.commit()
        messagebox.showinfo("Success", "Stock updated successfully!")

    # Cancel changes (clear the form and reset button to 'Correction')
    def cancel_entry():
        main_product_combo.delete(0, tk.END)
        sub_product_combo.delete(0, tk.END)
        pcs_entry.delete(0, tk.END)
        gross_wt_entry.delete(0, tk.END)
        melting_entry.delete(0, tk.END)
        net_wt_entry.delete(0, tk.END)
        rate_entry.delete(0, tk.END)
        mc_at_entry.delete(0, tk.END)

        # Reset correction button text to "Correction"
        correction_button.config(text="Correction", command=correction_entry)

    # Variables for input fields
    main_product_var = tk.StringVar()
    sub_product_var = tk.StringVar()

    # Dropdown options
    main_product_options = fetch_main_products()

    ### Opening Stock heading or Title ###
    tk.Label(opening_stock_window, text="Opening Stock", font=("Times", 25, "bold"), bg="lightblue", fg="green").pack(pady=10)

    # Create Frames for layout

    # Top frame for Main Product and Sub Product
    top_frame = tk.Frame(opening_stock_window, bg="lightblue")
    top_frame.pack(pady=20)

    # Main Product Dropdown
    tk.Label(top_frame, text="Main Product:", font=("Arial", 12), bg="lightblue").grid(row=0, column=0, sticky="w", padx=10)
    main_product_combo = ttk.Combobox(top_frame, textvariable=main_product_var, values=fetch_main_products(), state="readonly", width=25)
    main_product_combo.grid(row=0, column=1, padx=10)
    main_product_combo.bind('<<ComboboxSelected>>', update_sub_products)
    main_product_combo.bind('<Return>', focus_next_widget)

    # Sub Product Dropdown
    tk.Label(top_frame, text="Sub Product:", font=("Arial", 12), bg="lightblue").grid(row=1, column=0, sticky="w", padx=10)
    sub_product_combo = ttk.Combobox(top_frame, textvariable=sub_product_var, state="readonly", width=25)
    sub_product_combo.grid(row=1, column=1, padx=10)
    sub_product_combo.bind('<Return>', focus_next_widget)

    # Middle frame for stock details
    middle_frame = tk.Frame(opening_stock_window, bg="lightblue")
    middle_frame.pack(pady=20)

    # Input fields for stock details
    tk.Label(middle_frame, text="Pcs", font=("Times", 15), bg="lightblue").grid(row=0, column=0, padx=10, pady=5)
    pcs_entry = tk.Entry(middle_frame, font=("Times", 15), width=10, bd=4)
    pcs_entry.grid(row=1, column=0, padx=10, pady=5)
    pcs_entry.bind('<Return>', focus_next_widget)

    tk.Label(middle_frame, text="Gross Wt", font=("Times", 15), bg="lightblue").grid(row=0, column=1, padx=10, pady=5)
    gross_wt_entry = tk.Entry(middle_frame, font=("Times", 15), width=10, bd=4)
    gross_wt_entry.grid(row=1, column=1, padx=10, pady=5)
    gross_wt_entry.bind('<Return>', focus_next_widget)

    tk.Label(middle_frame, text="Melting", font=("Times", 15), bg="lightblue").grid(row=0, column=2, padx=10, pady=5)
    melting_entry = tk.Entry(middle_frame, font=("Times", 15), width=10, bd=4)
    melting_entry.grid(row=1, column=2, padx=10, pady=5)
    melting_entry.bind('<Return>', focus_next_widget)

    tk.Label(middle_frame, text="Net Wt", font=("Times", 15), bg="lightblue").grid(row=0, column=3, padx=10, pady=5)
    net_wt_entry = tk.Entry(middle_frame, font=("Times", 15), width=10, bd=4)
    net_wt_entry.grid(row=1, column=3, padx=10, pady=5)
    net_wt_entry.bind('<Return>', focus_next_widget)

    tk.Label(middle_frame, text="Rate", font=("Times", 15), bg="lightblue").grid(row=0, column=4, padx=10, pady=5)
    rate_entry = tk.Entry(middle_frame, font=("Times", 15), width=10, bd=4)
    rate_entry.grid(row=1, column=4, padx=10, pady=5)

    rate_entry.bind('<Return>', focus_next_widget)

    tk.Label(middle_frame, text="MC@", font=("Times", 15), bg="lightblue").grid(row=0, column=5, padx=10, pady=5)
    mc_at_entry = tk.Entry(middle_frame, font=("Times", 15), width=10, bd=4)
    mc_at_entry.grid(row=1, column=5, padx=10, pady=5)
    mc_at_entry.bind('<Return>', focus_next_widget)

    # Bottom frame for buttons
    bottom_frame = tk.Frame(opening_stock_window, bg="lightblue")
    bottom_frame.pack(pady=20)

    # Buttons in bottom frame
    tk.Button(bottom_frame, text="Save", command=save_entry, width=15, bg="purple").grid(row=0, column=0, padx=10, pady=10)
    correction_button = tk.Button(bottom_frame, text="Correction", command=correction_entry, width=15, bg="blue")
    correction_button.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(bottom_frame, text="Cancel", command=cancel_entry, width=15, bg="green").grid(row=0, column=2, padx=10, pady=10)
    tk.Button(bottom_frame, text="Exit", command=opening_stock_window.destroy, width=15, bg="red").grid(row=0, column=3, padx=10, pady=10)


