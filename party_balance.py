import tkinter as tk
from tkinter import ttk, messagebox

def party_balance(root): #### party balance page start
    # Function to generate the report
    def generate_report():
        messagebox.showinfo("Report", "Generating report...")

    # Function to exit the application
    def exit_app():
        root.quit()

    # Create the main window for Party Balance
    party_balance_window = tk.Toplevel()
    party_balance_window.title("Party Balance")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    party_balance_window.geometry(f"{screen_width}x{screen_height}")
    party_balance_window.configure(bg="lightblue")

    # Variables for input fields
    ledger_var = tk.StringVar(value="all")  # Default radio button selection
    currency_var = tk.StringVar(value="Rs")
    balance_var = tk.StringVar(value="opening")
    columns_var = tk.StringVar(value="two")
    message_box_var = tk.StringVar()

    # First Line: Title
    tk.Label(
        party_balance_window,
        text="PARTY BALANCE",
        font=("Arial", 16, "bold"),
        bg="lightblue"
    ).grid(row=0, column=0, columnspan=4, pady=20)

    # Second Line: Radio Buttons for Ledger Selection
    tk.Label(
        party_balance_window,
        text="Select Ledger:",
        font=("Arial", 12, "bold"),
        bg="lightblue"
    ).grid(row=1, column=0, sticky="w", padx=10, pady=10)

    ledger_options = ["All Ledger", "Individual Ledger"]
    for i, option in enumerate(ledger_options):
        tk.Radiobutton(
            party_balance_window,
            text=option,
            variable=ledger_var,
            value=option,
            font=("Arial", 10),
            bg="lightblue"
        ).grid(row=1, column=i + 1, padx=10)

    # Third Line: Radio Buttons for Currency Selection
    tk.Label(
        party_balance_window,
        text="Select Currency:",
        font=("Arial", 12, "bold"),
        bg="lightblue"
    ).grid(row=2, column=0, sticky="w", padx=10, pady=10)

    currency_options = ["Rs", "Metal", "Rs & Metal"]
    for i, option in enumerate(currency_options):
        tk.Radiobutton(
            party_balance_window,
            text=option,
            variable=currency_var,
            value=option,
            font=("Arial", 10),
            bg="lightblue"
        ).grid(row=2, column=i + 1, padx=10)

    # Fourth Line: Radio Buttons for Balance Type
    tk.Label(
        party_balance_window,
        text="Select Balance Type:",
        font=("Arial", 12, "bold"),
        bg="lightblue"
    ).grid(row=3, column=0, sticky="w", padx=10, pady=10)

    balance_options = ["Opening Bal", "Closing Bal"]
    for i, option in enumerate(balance_options):
        tk.Radiobutton(
            party_balance_window,
            text=option,
            variable=balance_var,
            value=option,
            font=("Arial", 10),
            bg="lightblue"
        ).grid(row=3, column=i + 1, padx=10)

    # Fifth Line: Message Box
    tk.Label(
        party_balance_window,
        text="Enter Message:",
        font=("Arial", 12, "bold"),
        bg="lightblue"
    ).grid(row=4, column=0, sticky="w", padx=10, pady=10)

    message_box = tk.Text(
        party_balance_window,
        height=3,
        width=50,
        wrap=tk.WORD
    )
    message_box.grid(row=4, column=1, columnspan=3, padx=10, pady=10)

    # Sixth Line: Radio Buttons for Column Selection
    tk.Label(
        party_balance_window,
        text="Select Columns:",
        font=("Arial", 12, "bold"),
        bg="lightblue"
    ).grid(row=5, column=0, sticky="w", padx=10, pady=10)

    columns_options = ["Two Columns", "Three Columns"]
    for i, option in enumerate(columns_options):
        tk.Radiobutton(
            party_balance_window,
            text=option,
            variable=columns_var,
            value=option,
            font=("Arial", 10),
            bg="lightblue"
        ).grid(row=5, column=i + 1, padx=10)

    # Buttons for Report and Exit
    buttons_frame = tk.Frame(party_balance_window, bg="lightblue")
    buttons_frame.grid(row=6, column=0, columnspan=4, pady=20)

    report_button = tk.Button(
        buttons_frame,
        text="Report",
        font=("Arial", 12),
        command=generate_report
    )
    report_button.grid(row=0, column=0, padx=10)

    exit_button = tk.Button(
        buttons_frame,
        text="Exit",
        font=("Arial", 12),
        command=exit_app
    )
    exit_button.grid(row=0, column=1, padx=10)
    party_balance_window.mainloop()
#### party balance page start