import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
from main_ledger import open_main_ledger
from sub_ledger import open_sub_ledger
from main_product import open_main_product
from sub_product import open_sub_product
from opening_balance import opening_balance
from opening_stock import opening_stock
from party_balance import party_balance
from party_ledger import party_ledger
from receipt_issue import recepit_issue
from day_book import day_book


# Database connection
conn = sqlite3.connect('stock.db')
cursor = conn.cursor()

# def exit_program(root):
#     root.destroy()

#this function is using Enter button cliking move the next column
def focus_next_widget(event):
    """Move the focus to the next widget."""
    event.widget.tk_focusNext().focus()
    return "break"

# Function to handle exit menu action
def exit_program():
    root.quit()

#### fetch main_product value for main_product
def fetch_main_product():
    try:
        cursor.execute("SELECT UPPER(name) FROM main_product")
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.OperationalError as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return []



#### fetch sub_product value for sub_product
def fetch_sub_product(selected_main_product):
    try:
        cursor.execute("SELECT UPPER(name) FROM sub_product WHERE UPPER(main_product) = ?", (selected_main_product.upper(),))

        return [row[0] for row in cursor.fetchall()]
    except sqlite3.OperationalError as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return []

def update_sub_products(event):
    selected_main_product = main_product_combo.get()
    print(f"Selected Main Product: {selected_main_product}")
    if selected_main_product:
        sub_products = fetch_sub_product(selected_main_product)
        print(f"Sub Products: {sub_products}")
        sub_product_combo['values'] = sub_products
        sub_product_combo.set("")  # Clear the current selection
    else:
        sub_product_combo['values'] = []
        sub_product_combo.set("")

# Transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        name TEXT,
        "transaction" TEXT,
        main_product TEXT NOT NULL,
        sub_product TEXT NOT NULL,
        gross_wt REAL NOT NULL,
        stones INTEGER,
        touch REAL,
        net_wt REAL NOT NULL,
        mc_at REAL,
        mc REAL,
        rate REAL NOT NULL,
        amount REAL NOT NULL,
        narration TEXT
    )
    """)


# Function to calculate Net Weight
def calculate_net_wt(event=None):  # 'event' is needed for binding
    try:
        # Fetch input values
        gross_wt = float(gross_wt_entry.get()) if gross_wt_entry.get() else 0.0
        stones = float(stones_entry.get()) if stones_entry.get() else 0.0
        touch = float(touch_entry.get()) if touch_entry.get() else 0.0
        
        # Perform the calculation
        adjusted_wt = gross_wt - stones
        net_wt = adjusted_wt * (touch / 100)
        
        # Insert the calculated value into net_wt_entry
        net_wt_entry.delete(0, tk.END)  # Clear existing value
        net_wt_entry.insert(0, f"{net_wt:.2f}")  # Insert new value with 2 decimal places

        focus_next_widget(event)
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for Gross Wt, Stones, and Touch.")
# Bind the Enter key to the Touch entry field


def calculate_mc(event=None):
    try:
        # Get the net weight and mc_at values
        net_wt = float(net_wt_entry.get()) if net_wt_entry.get() else 0.0  # Default to 0.0 if empty
        mc_at = float(mc_at_entry.get()) if mc_at_entry.get() else 0.0  # Default to 0.0 if empty

        # MC calculation: multiply net weight with mc_at
        mc = net_wt * mc_at

        # Display the result in mc_entry with 2 decimal places
        mc_entry.delete(0, tk.END)
        mc_entry.insert(0, f"{mc:.2f}")

        # Optionally, move focus to the next widget
        focus_next_widget(event)

    except ValueError:
        # Show error message if invalid input is provided
        messagebox.showerror("Input Error", "Please enter valid numbers for MC@ and Net Wt.")



def display_mc_at_value(event=None):
    # Check if mc_at_entry is empty before fetching from the database
    if not mc_at_entry.get():  # Only fetch if the field is empty
        main_product = main_product_combo.get()
        sub_product = sub_product_combo.get()

        # Fetch mc_at value from the database
        cursor.execute("SELECT mc_at FROM opening_stock WHERE main_product=? AND sub_product=?", 
                       (main_product, sub_product))
        result = cursor.fetchone()

        if result:
            mc_at = result[0]  # Extract mc_at value from the result
        else:
            mc_at = 0.0  # Default value if no result is found

        # Display mc_at value in mc_at_entry with 1 decimal place
        mc_at_entry.delete(0, tk.END)  # Clear any existing value
        mc_at_entry.insert(0, f"{mc_at:.1f}")

    # Optionally, move focus to the next widget
    focus_next_widget(event)
    # Get selected values from combo boxes
   
def fetch_rate_value(event=None):
    if not rate_entry.get():
        main_product=main_product_combo.get()
        sub_product=sub_product_combo.get()

        cursor.execute("SELECT rate FROM opening_stock WHERE main_product=? AND sub_product=?",
                       (main_product, sub_product))
        result=cursor.fetchone()

        if result:
            rate=result[0]
        else:
            rate=0.0

        rate_entry.delete(0, tk.END)
        rate_entry.insert(0, f"{rate:.2f}")

    focus_next_widget(event)

# Function to calculate Amount 
def calculate_amount(event=None):
    
    rate=float(rate_entry.get()) if rate_entry.get() else 0.0
    net_wt=float(net_wt_entry.get()) if net_wt_entry.get() else 0.0
    mc=float(mc_entry.get()) if mc_entry.get() else 0.0

    amount=(net_wt*rate)+mc # final amount calculation 

    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, f"{amount:.2f}")

    focus_next_widget(event)
    ############################################################

###########################################################################################

def fetch_rate(main_product, sub_product):
    # Fetch the rate from the database based on main_product and sub_product
    
    cursor.execute("SELECT rate FROM opening_stock WHERE main_product=? AND sub_product=?", (main_product, sub_product))
    result = cursor.fetchone()  # Fetch one result
    conn.commit()
    
    if result:
        return result[0]  # Return the rate from the first column
    else:
        return 0.0  # Default rate if no result is found

def update_rate_entry(event=None):
    # Get the selected main_product and sub_product
    main_product = main_product_combo.get()
    sub_product = sub_product_combo.get()
    
    # Fetch the rate from the database based on the selected products
    cursor.execute("SELECT rate from opening_stock WHERE main_product=? AND sub_product=?", (main_product, sub_product))
    result=cursor.fetchone()

    if result:
        rate=result[0]
    else:
        rate = 0
    
    # Populate the rate_entry with the fetched rate
    rate_entry.delete(0, tk.END)
    rate_entry.insert(0, f"{rate:.2f}") 

    focus_next_widget(event)

###############################################################################

# Functionality for buttons
def add_item(event=None):
    # print("add_ item function triggered")
    cursor.execute("select max(ID) from saved_data")
    max_id = cursor.fetchone()[0]
    sl_no = (max_id+1) if max_id else 1
    date = date_entry.get()
    name = party_entry.get()
    transaction = transaction_combo.get()
    main_product = main_product_combo.get()
    sub_product = sub_product_combo.get()
    gross_wt = float(gross_wt_entry.get())
    stones = float(stones_entry.get())
    touch = float(touch_entry.get())

    mc_at = mc_at_entry.get()
    mc = mc_entry.get()
    rate = float(rate_entry.get())
    
    narration = narration_entry.get()

    if not gross_wt and touch:
        messagebox.error("Input Error", "Please enter Gross Wt and Touch")
        return 
    
    adjusted_wt=gross_wt-stones
    net_wt=adjusted_wt*(touch/100)

    if not rate:
        messagebox.error("Input Error", "Please enter Rate")
        return 
    amount=(net_wt*rate)+float(mc)
    amount=float(f"{amount:.2f}")

    if name and transaction :
        tree.insert("", "end", values=(sl_no, date, name, main_product, sub_product, transaction, gross_wt, stones, touch,net_wt, mc_at, mc, rate, amount, narration))
        clear_fields()

    else:
        messagebox.showerror("Input Error", "Please fill all required fields.")

    try:
        amount = float(f"{amount:.2f}")
        
        cursor.execute("""
        INSERT INTO saved_data (date, "transaction", name, main_product, sub_product, gross_wt, stones, touch, net_wt, mc_at, mc, rate, amount, narration)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (date,transaction,name, main_product, sub_product, gross_wt, stones, touch, net_wt, mc_at, mc, rate, amount,narration))
        conn.commit()
        messagebox.showinfo("Success", 
                f"Date : {date},\nTransaction : {transaction}, \nCustomer Name : {name}, \nMain Product : {main_product}, \nSub Product : {sub_product}, \nGross Wt : {gross_wt}, \nStones : {stones}, \nTouch : {touch}, \nNetWt : {net_wt}, \nMC@ : {mc_at}, \nMC : {mc}, \nRate : {rate}, \nAmount : {amount}, \nNarration : {narration}\n"
                    "Receipt saved successfully!")
        
        
        # Clear input fields
        
        party_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        main_product_combo.set("")
        sub_product_combo.set("")
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number!")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")


    # if transaction=="Metal Receipt":
    #     Metaling_Label=tk.Label(root, text="Melting", font=("Arial", 12, "bold"), bg="lightpink")
    #     Metaling_Label.grid(row=4, column=2, height=20, width=40)
    #     Metaling_Entry=tk.Entry(root, padx=10, width=8, font=("Arial", 12, "bold"))
    #     Metaling_Entry.grid(stciky="w", row=4, column=3)

#         if True:
#             cursor.execute("""
#             UPDATE SET saved_data date=?, name=? WHERE id=?,(date,name, id)
# """)
    
#     elif transaction=="Metal Issue":
#         Metaling_issue_Label=tk.Label(root, text="Melting", font=("Arial", 12, "bold"), bg="lightpink")
#         Metaling_issue_Label.grid(row=4, column=2, height=20, width=40)
#         Metaling_issue_Entry=tk.Entry(root, padx=10, width=8, font=("Arial", 12, "bold"))
#         Metaling_issue_Entry.grid(stciky="w", row=4, column=3)

#         if True:
#             cursor.execute("""

#             UPDATE SET saved_data date=?, name=? WHERE id=?,(date,name,id)
# """)
    
#     elif transaction=="Cash Receipt":
#         Cash_Receipt=tk.Label(root, text="cash Receipt", font=("Arial", 12, "Strong"), bg="lightblue")
    #     Cash_Receipt.grid(row=4, column=5, width=10)
    #     Cash_Receipt_Entry=tk.Label(root, width=8, bd=2)
    #     Cash_Receipt_Entry.grid(row=4, column=5)

    #     if True:
    #         cursor.execute("""
    #             UPDATE SET customer_summary amount=amount-? WHERE id=?,(amount, id,)    """)
            
    # elif transaction=="Cash Payment":
    #     Cash_Payment=tk.Label(root, text="cash payment")
    #     Cash_Payment.grid(row=4, column=7)
    #     Cash_Payment_Entry=tk.Entry(root, width=8, bd=3)
    #     Cash_Payment_Entry.grid(row=3, column=8)

    #     if True:
    #         cursor.execute("""UPDATE SET customer_summary amount=amount+? WHERE""")

#########################################################################################################################
# Function to delete an item from the treeview and database
def delete_item():
    selected_item = tree.selection()  # Get the selected item from TreeView
    if selected_item:
        # Get the 'id' from the selected item
        item_values = tree.item(selected_item, 'values')
        record_id = item_values[0]

        try:
            # Delete from database
            cursor.execute("DELETE FROM saved_data WHERE id=?", (record_id,))
            conn.commit()

            # Delete from TreeView
            tree.delete(selected_item)
            messagebox.showinfo("Success", "Item deleted successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Selection Error", "Select an item to delete.")

# Correction Or Update an item for tree view and database
def correction_item():
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a record to modify.")
        return
    
    tree_item_id=selected_item[0]
    record= tree.item(tree_item_id,"values")

    global selected_tree_item
    global selected_id 

    # Save Treeview item ID for updates
    selected_tree_item = tree_item_id
    # Save the database ID for the update query
    selected_id = record[0]  # Assuming the first column is the database ID and This SLNO

    
    # Populate fields with the selected record's data
    date_entry.delete(0, tk.END)
    date_entry.insert(0, record[1])  # Date
    party_entry.delete(0, tk.END)
    party_entry.insert(0, record[2])  # Party Name
    main_product_combo.set(record[3])  # Main Product
    sub_product_combo.set(record[4])  # Sub Product
    transaction_combo.set(record[5])  # Transaction
    gross_wt_entry.delete(0, tk.END)
    gross_wt_entry.insert(0, record[6])  # Gross Weight
    stones_entry.delete(0, tk.END)
    stones_entry.insert(0, record[7])  # Stones
    touch_entry.delete(0, tk.END)
    touch_entry.insert(0, record[8])  # Touch
    net_wt_entry.delete(0, tk.END)
    net_wt_entry.insert(0, record[9])  # Net Weight
    mc_at_entry.delete(0, tk.END)
    mc_at_entry.insert(0, record[10])  # MC@
    mc_entry.delete(0, tk.END)
    mc_entry.insert(0, record[11])  # MC
    rate_entry.delete(0, tk.END)
    rate_entry.insert(0, record[12])  # Rate
    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, record[13])  # Amount
    narration_entry.delete(0, tk.END)
    narration_entry.insert(0, record[14])  # Narration

    correction_button.config(text="Update", command=update_item)


    
    # save the selected item's ID for further updates

def update_item():
    # Fetch updated values from entry fields
    updated_values=(
        date_entry.get(),
        party_entry.get(),
        main_product_combo.get(),
        sub_product_combo.get(),
        transaction_combo.get(),
        gross_wt_entry.get(),
        stones_entry.get(),
        touch_entry.get(),
        net_wt_entry.get(),
        mc_at_entry.get(),
        mc_entry.get(),
        rate_entry.get(),
        amount_entry.get(),
        narration_entry.get()
        
    )  

    try:
        conn=sqlite3.connect('stock.db')
        cursor=conn.cursor()
        cursor.execute(
            """
                UPDATE saved_data SET date=?, name=?,  
                main_product=?, sub_product=?, "transaction"=?, gross_wt=?, stones=?, 
                touch=?, net_wt=?, mc_at=?, mc=?, rate=?, amount=?, 
                narration=?
                WHERE id=?
            """, updated_values+(selected_id,)
        )
        conn.commit() 

        # Update the tree view item 
        tree.item(selected_tree_item, values=(selected_id,)+updated_values)

        messagebox.showinfo("Success", "Record updated successfully.")

        #Reset the button text to 'Correction'
        correction_button.config(text='Correction', command=correction_item)
    except Exception as e:
        messagebox.showerror('Error',f'Failed to update record: {e}')
    finally:
        conn.close()
        clear_fields()


# Completed the Update Data or correction_item function as Ended
def clear_fields():
    party_entry.delete(0, tk.END)
    gross_wt_entry.delete(0, tk.END)
    stones_entry.delete(0, tk.END)
    touch_entry.delete(0, tk.END)
    net_wt_entry.delete(0, tk.END)
    mc_at_entry.delete(0, tk.END)
    mc_entry.delete(0, tk.END)
    rate_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    narration_entry.delete(0, tk.END)


def save_items():
    items = tree.get_children()
    if items:
        with open("jewelry_data.csv", "w") as file:
            file.write("SLNo,Date,Name,Main Product, Sub Product,Transaction,Gross,Stones,Touch,Net Weight,MC@,MC,Rate,Amount,Narration\n")
            for item in items:
                values = tree.item(item, "values")
                file.write(",".join(values) + "\n")
        messagebox.showinfo("Save Success", "Data saved to jewelry_data.csv")
    else:
        messagebox.showerror("Save Error", "No data to save.")



root = tk.Tk()
root.title("Jewelry Management System")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")
root.configure(bg="lightpink")

# Create menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

master_menu = tk.Menu(menu_bar, tearoff=0)
transaction_menu = tk.Menu(menu_bar, tearoff=0)
report_menu = tk.Menu(menu_bar, tearoff=0)
utility_menu = tk.Menu(menu_bar, tearoff=0)
exit_menu = tk.Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label="Master", menu=master_menu)
menu_bar.add_cascade(label="Transaction", menu=transaction_menu)
menu_bar.add_cascade(label="Report", menu=report_menu)
menu_bar.add_cascade(label="Exit", menu=exit_menu)

#Master #### Adding submenu of master menu
master_menu.add_command(label="Main Ledger", command=lambda:open_main_ledger(root))
master_menu.add_command(label="Sub Ledger", command=lambda:open_sub_ledger(root))
master_menu.add_command(label="Main Product", command=lambda:open_main_product(root))
master_menu.add_command(label="Sub Product", command=lambda:open_sub_product(root))
master_menu.add_command(label="Opening Stock", command=lambda:opening_stock(root)) #######
master_menu.add_command(label="Party Opening Balance", command=lambda:opening_balance(root)) #####

#Transaction
# Adding submenu items to the Trasaction menu
transaction_menu.add_command(label="Recepit & Issue", command=lambda:recepit_issue(root))

#Report
# Adding submenu items to the Report menu
report_menu.add_command(label="DayBook", command=lambda:day_book(root))
report_menu.add_command(label="PartyLedger", command=lambda:party_ledger(root))
report_menu.add_command(label="Party Balance", command=lambda:party_balance(root))

#Exit
exit_menu.add_command(label="Exit", command=exit_program)

cash_receipt_label = tk.Label(root, text="Cash Receipt", font=("Times", 25, "bold"), bg="lightpink", fg="Green")
cash_receipt_label.pack(pady=10)
#############################################################################################################################


# Top Frame - Row 1: Basic Details
# Top Frame - Line 1: Date, Transaction, Party Name
top_frame = tk.Frame(root, bg="lightpink")
top_frame.pack(pady=10)

# Row 1
tk.Label(top_frame, text="Date", bg="lightpink", font=("Times", 15), anchor="w").grid(row=0, column=0, padx=5)
date_entry = tk.Entry(top_frame, width=15, justify="center", font=("Times",14), bd=4)
date_entry.insert(0, datetime.now().strftime("%d-%m-%Y"))
date_entry.grid(row=1, column=0, padx=5, sticky="w")
date_entry.bind("<Return>", focus_next_widget)

tk.Label(top_frame, text="Transaction", bg="lightpink", font=("Times", 15)).grid(row=0, column=1, padx=5)
transaction_combo = ttk.Combobox(top_frame, values=["Cash Receipt", "Cash Payment", "Purchase", "Purchase Return", "Sales", "Sales Return", "Metal Receipt", "Metal Issue", "Rate Cut Sales", "Rate Cut Purchase", "Achari Receipt", "Achari Issue", "Approval Issue", "Approval Receipt"], width=15, justify="center", font=("Times",14))
transaction_combo.grid(row=1, column=1, padx=5, sticky="w")
transaction_combo.bind("<Return>", focus_next_widget)

# Function to update the label when a value is selected
def update_label(event):
    selected_transaction = transaction_combo.get()  # Get selected value
    cash_receipt_label.config(text=selected_transaction)  # Update label text

# Bind the selection event to the function
transaction_combo.bind("<<ComboboxSelected>>", update_label)

tk.Label(top_frame, text="Party Name", bg="lightpink", font=("Times", 15)).grid(row=0, column=2, padx=5)
party_entry = tk.Entry(top_frame, width=20, justify="center", font=("Times",14), bd=4)
party_entry.grid(row=1, column=2, padx=5, sticky="w")
party_entry.bind("<Return>", focus_next_widget)

# Middle Frame - Line 2: Main Product, Sub Product, Gross Wt, Stones, Touch, Net Wt, MC@, MC
middle_frame = tk.Frame(root, bg="lightpink")
middle_frame.pack(pady=10)

tk.Label(middle_frame, text="Main Product", bg="lightpink", font=("Times", 15)).grid(row=0, column=0, padx=5)
main_product_combo = ttk.Combobox(middle_frame, values=fetch_main_product(), state="readonly", width=20, justify="center", font=("Times",14))
main_product_combo.grid(row=1, column=0, padx=5, sticky="w")
main_product_combo.bind('<<ComboboxSelected>>',update_sub_products)
main_product_combo.bind("<Return>", focus_next_widget)

tk.Label(middle_frame, text="Design", bg="lightpink", font=("Times", 15)).grid(row=0, column=1, padx=5)
sub_product_combo = ttk.Combobox(middle_frame, state="readonly", width=20, justify="center", font=("Times",14))
sub_product_combo.grid(row=1, column=1, padx=5, sticky="w")
sub_product_combo.bind("<Return>", focus_next_widget)

tk.Label(middle_frame, text="Gross Wt", bg="lightpink", font=("Times", 15)).grid(row=0, column=2, padx=5)
gross_wt_entry = tk.Entry(middle_frame, width=8, justify="center", font=("Times",14), bd=4)
gross_wt_entry.grid(row=1, column=2, padx=5, sticky="w")
gross_wt_entry.bind("<Return>", focus_next_widget)

tk.Label(middle_frame, text="Cover", bg="lightpink", font=("Times", 15)).grid(row=0, column=3, padx=5)
stones_entry = tk.Entry(middle_frame, width=7, justify="center", font=("Times",14), bd=4)
stones_entry.grid(row=1, column=3, padx=5, sticky="w")
stones_entry.bind("<Return>", focus_next_widget)

tk.Label(middle_frame, text="Touch", bg="lightpink", font=("Times", 15)).grid(row=0, column=4, padx=5)
touch_entry = tk.Entry(middle_frame, width=8, justify="center", font=("Times",14), bd=4)
touch_entry.grid(row=1, column=4, padx=5, sticky="w")
touch_entry.bind("<Return>", calculate_net_wt)


tk.Label(middle_frame, text="Net Wt", bg="lightpink", font=("Times", 15)).grid(row=0, column=5, padx=5)
net_wt_entry = tk.Entry(middle_frame, width=10, justify="center", font=("Times",14), bd=4)
net_wt_entry.grid(row=1, column=5, padx=5, sticky="w")
net_wt_entry.bind("<Return>", focus_next_widget)


tk.Label(middle_frame, text="MC@", bg="lightpink", font=("Times", 15)).grid(row=0, column=6, padx=5)
mc_at_entry = tk.Entry(middle_frame, width=7, justify="center", font=("Times",14), bd=4)
mc_at_entry.grid(row=1, column=6, padx=5, sticky="w")
mc_at_entry.bind("<Return>", display_mc_at_value)


tk.Label(middle_frame, text="MC", bg="lightpink", font=("Times", 15)).grid(row=0, column=7, padx=5)
mc_entry = tk.Entry(middle_frame, width=8, justify="center", font=("Times",14), bd=4)
mc_entry.grid(row=1, column=7, padx=5, sticky="w")
mc_entry.bind("<Return>", calculate_mc)

# Bottom Frame - Line 3: Rate, Amount, Narration
bottom_frame = tk.Frame(root, bg="lightpink")
bottom_frame.pack(pady=10)

tk.Label(bottom_frame, text="Rate", bg="lightpink", font=("Times", 15)).grid(row=0, column=0, padx=5)
rate_entry = tk.Entry(bottom_frame, width=10, justify="center", font=("Times",14), bd=4)
rate_entry.grid(row=1, column=0, padx=5, sticky="w")
rate_entry.bind("<Return>", fetch_rate_value)

tk.Label(bottom_frame, text="Amount", bg="lightpink", font=("Times", 15)).grid(row=0, column=1, padx=5)
amount_entry = tk.Entry(bottom_frame, width=11, justify="center", font=("Times",14), bd=4)
amount_entry.grid(row=1, column=1, padx=5, sticky="w")
amount_entry.bind("<Return>", calculate_amount)

########## the Metal Value or label and entry show or hide ###########
# amount_value=amount_entry.get()

# if amount_value== "" or 0 or 0.0:
#     tk.Label(bottom_frame, text="Metal", bg="lightpink", font=("Times", 15)).grid(row=0, column=2, padx=5)
#     metal_entry = tk.Entry(bottom_frame, width=11, justify="center", font=("Times",14), bd=4)
#     metal_entry.grid(row=1, column=2, padx=5, sticky="w")
#     metal_entry.bind("<Return>", focus_next_widget)

tk.Label(bottom_frame, text="Narration", bg="lightpink", font=("Times", 15)).grid(row=0, column=3, columnspan=3,padx=5)
narration_entry = tk.Entry(bottom_frame, width=30, justify="center", font=("Times",14), bd=4)
narration_entry.grid(row=1, column=3, padx=5, columnspan=3, sticky="w")
narration_entry.bind("<Return>", add_item)


# Frame for the Treeview and Scrollbars
tree_frame = tk.Frame(root, bg="lightpink", width=300, height=800)
tree_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its content
tree_frame.pack(pady=10)

# Create the Treeview widget
columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#12", "#13", "#14", "#15")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)

# Set headings for each column
tree.heading("#1", text="SLNo")
tree.heading("#2", text="Date")
tree.heading("#3", text="Name")
tree.heading("#4", text="Main Product")
tree.heading("#5", text="Design")
tree.heading("#6", text="Transaction")
tree.heading("#7", text="Gross")
tree.heading("#8", text="Stones")
tree.heading("#9", text="Touch")
tree.heading("#10", text="Net Wt")
tree.heading("#11", text="MC@")
tree.heading("#12", text="MC")
tree.heading("#13", text="Rate")
tree.heading("#14", text="Amount")
tree.heading("#15", text="Narration")

# Set column width and alignment
tree.column("#1", width=30, anchor=tk.CENTER)
tree.column("#2", width=60, anchor=tk.CENTER)
tree.column("#3", width=120, anchor=tk.W)
tree.column("#4", width=120, anchor=tk.W)
tree.column("#5", width=80, anchor=tk.W)
tree.column("#6", width=100, anchor=tk.W)
tree.column("#7", width=40, anchor=tk.CENTER)
tree.column("#8", width=40, anchor=tk.CENTER)
tree.column("#9", width=40, anchor=tk.CENTER)
tree.column("#10", width=70, anchor=tk.CENTER)
tree.column("#11", width=50, anchor=tk.CENTER)
tree.column("#12", width=40, anchor=tk.CENTER)
tree.column("#13", width=70, anchor=tk.CENTER)
tree.column("#14", width=90, anchor=tk.CENTER)
tree.column("#15", width=180, anchor=tk.W)

# Add horizontal and vertical scrollbars
x_scrollbar = tk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
y_scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)

# Configure the Treeview to use the scrollbars
tree.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

# Pack the Treeview and scrollbars
tree.grid(row=0, column=0, sticky="nsew")
y_scrollbar.grid(row=0, column=1, sticky="ns")
x_scrollbar.grid(row=1, column=0, sticky="ew")

# Configure the grid to make the Treeview expand with the frame
tree_frame.grid_rowconfigure(0, weight=1)
tree_frame.grid_columnconfigure(0, weight=1)

# Footer Frame - Buttons
footer_frame = tk.Frame(root, bg="lightpink")
footer_frame.pack(pady=20)

# tk.Button(footer_frame, text="Add", width=12, bg="green", fg="white").grid(row=0, column=0, padx=10)
tk.Button(footer_frame, text="Delete", width=12, bg="red", fg="white", command=delete_item).grid(row=0, column=1, padx=10)
tk.Button(footer_frame, text="Save", width=12, bg="blue", fg="white", command=save_items).grid(row=0, column=2, padx=10)
correction_button=tk.Button(footer_frame, text="Correction", width=12, bg="purple", fg="white", command=correction_item)
correction_button.grid(row=0,column=3, padx=10)
tk.Button(footer_frame, text="Exit", width=12, bg="orange", fg="white", command=root.destroy).grid(row=0, column=4, padx=10)

# Run the application
root.mainloop()
