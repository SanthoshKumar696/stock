import tkinter as tk
from tkinter import ttk, messagebox

def party_ledger(root):   #### party ledger page start
    party_ledger_window = tk.Toplevel()
    party_ledger_window.title("Party Ledger")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    party_ledger_window.geometry(f"{screen_width}x{screen_height}")
    party_ledger_window.configure(bg="lightblue")

    tk.Label(
        party_ledger_window, text="Party Ledger",
        font=("Arial", 16, "bold"), bg="lightblue"
    ).grid(row=0, column=0, columnspan=5, pady=20)

    # Frame to group all options with a border
    options_frame = tk.Frame(party_ledger_window, bg="lightblue", bd=2, relief="groove")
    options_frame.grid(row=1, column=0, columnspan=5, padx=20, pady=20, sticky="nsew")

    # Balance options
    tk.Label(
        options_frame, text="Select Ledger:", font=("Arial", 12, "bold"), bg="lightblue"
    ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

    balance_var = tk.StringVar(value="Nil Bal")
    balance_options = ["Nil Bal", "Only Bal", "Both"]
    for i, option in enumerate(balance_options):
        tk.Radiobutton(
            options_frame, text=option, value=option,
            variable=balance_var, font=("Arial", 10), bg="lightblue"
        ).grid(row=0, column=i + 1, padx=10)

    # Account options
    tk.Label(
        options_frame, text="Select Account:", font=("Arial", 12, "bold"), bg="lightblue"
    ).grid(row=1, column=0, sticky="w", padx=10, pady=10)

    account_var = tk.StringVar(value="All A/C")
    account_options = ["All A/C", "Individual"]
    for i, option in enumerate(account_options):
        tk.Radiobutton(
            options_frame, text=option, value=option,
            variable=account_var, font=("Arial", 10), bg="lightblue"
        ).grid(row=1, column=i + 1, padx=10)

    # Stone options
    tk.Label(
        options_frame, text="Select Stone:", font=("Arial", 12, "bold"), bg="lightblue"
    ).grid(row=2, column=0, sticky="w", padx=10, pady=10)

    stone_var = tk.StringVar(value="Without St")
    stone_options = ["Without St", "With Stones", "Pcs/WO Touch", "Running"]
    for i, option in enumerate(stone_options):
        tk.Radiobutton(
            options_frame, text=option, value=option,
            variable=stone_var, font=("Arial", 10), bg="lightblue"
        ).grid(row=2, column=i + 1, padx=10)

    # Balance type options
    tk.Label(
        options_frame, text="Select Balance:", font=("Arial", 12, "bold"), bg="lightblue"
    ).grid(row=3, column=0, sticky="w", padx=10, pady=10)

    bal_var = tk.StringVar(value="With Opening Balance")
    bal_options = ["With Opening Balance", "Without Opening Balance"]
    for i, option in enumerate(bal_options):
        tk.Radiobutton(
            options_frame, text=option, value=option,
            variable=bal_var, font=("Arial", 10), bg="lightblue"
        ).grid(row=3, column=i + 1, padx=10)

    # Date options
    tk.Label(
        options_frame, text="Select Date:", font=("Arial", 12, "bold"), bg="lightblue"
    ).grid(row=4, column=0, sticky="w", padx=10, pady=10)

    date_var = tk.StringVar(value="Monthly")
    date_options = ["Monthly", "Date Wise", "BillWise"]
    for i, option in enumerate(date_options):
        tk.Radiobutton(
            options_frame, text=option, value=option,
            variable=date_var, font=("Arial", 10), bg="lightblue"
        ).grid(row=4, column=i + 1, padx=10)

    # Date Inputs
    tk.Label(party_ledger_window, text="From Date:", font=("Arial", 14), bg="lightblue").grid(row=2, column=0, padx=10, pady=10)
    from_date_entry = tk.Entry(party_ledger_window, font=("Arial", 14), width=20)
    from_date_entry.grid(row=2, column=1)

    tk.Label(party_ledger_window, text="To Date:", font=("Arial", 14), bg="lightblue").grid(row=3, column=0, padx=10, pady=10)
    to_date_entry = tk.Entry(party_ledger_window, font=("Arial", 14), width=20)
    to_date_entry.grid(row=3, column=1)

    # Buttons
    tk.Button(
        party_ledger_window, text="Report", font=("Arial", 12), bg="green", fg="white",
        width=10, command=lambda: print(f"Generating report from {from_date_entry.get()} to {to_date_entry.get()}")
    ).grid(row=4, column=0, padx=10, pady=10)

    tk.Button(
        party_ledger_window, text="Cancel", font=("Arial", 12), bg="orange", fg="white",
        width=10, command=lambda: [from_date_entry.delete(0, tk.END), to_date_entry.delete(0, tk.END)]
    ).grid(row=4, column=1, padx=10, pady=10)

    tk.Button(
        party_ledger_window, text="Exit", font=("Arial", 12), bg="red", fg="white",
        width=10, command=party_ledger_window.destroy
    ).grid(row=4, column=2, padx=10, pady=10)
###  party ledger page ended