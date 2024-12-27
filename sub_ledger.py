import tkinter as tk
from tkinter import ttk, messagebox

def open_sub_ledger(root):  #### start the sub product 
    # Create a new window for Main Ledger
    sub_ledger_window = tk.Toplevel()
    sub_ledger_window.title("Main Product Master")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    sub_ledger_window.geometry(f"{screen_width}x{screen_height}")
    sub_ledger_window.configure(bg="lightblue")

    # Variables for input fields
    operation_var = tk.StringVar(value="Addition")  # Default radio button selection
    main_ledger_var = tk.StringVar()  # Dropdown selection
    code_var = tk.StringVar()
    name_var = tk.StringVar()
    

    # First Line: Radio Buttons for Operations
    tk.Label(
        sub_ledger_window,
        text="Select Operation:",
        font=("Arial", 12, "bold"),
        bg="lightblue"
    ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

    operations = ["Addition", "Correction", "Deletion", "View"]
    for i, operation in enumerate(operations):
        tk.Radiobutton(
            sub_ledger_window,
            text=operation,
            variable=operation_var,
            value=operation,
            font=("Arial", 10),
            bg="lightblue"
        ).grid(row=0, column=i + 1, padx=10)

    # Second Line: Main Ledger Dropdown
    tk.Label(
        sub_ledger_window,
        text="Main Ledger:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=1, column=0, sticky="w", padx=10, pady=10)

    main_ledger_options = ["Ledger 1", "Ledger 2", "Ledger 3"]  # Example options
    main_ledger_dropdown = ttk.Combobox(
        sub_ledger_window,
        textvariable=main_ledger_var,
        values=main_ledger_options,
        state="readonly",
        width=30
    )
    main_ledger_dropdown.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

    # Third Line: Code
    tk.Label(
        sub_ledger_window,
        text="Code:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=2, column=0, sticky="w", padx=10, pady=10)

    code_entry = tk.Entry(
        sub_ledger_window,
        textvariable=code_var,
        font=("Arial", 12),
        width=30
    )
    code_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

    # Fourth Line: Name
    tk.Label(
        sub_ledger_window,
        text="Name:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=3, column=0, sticky="w", padx=10, pady=10)

    name_entry = tk.Entry(
        sub_ledger_window,
        textvariable=name_var,
        font=("Arial", 12),
        width=30
    )
    name_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=10)


    # Right-side Frame to Show Entered Details
    details_frame = tk.Frame(sub_ledger_window, bg="lightgray", width=400, height=300)
    details_frame.grid(row=0, column=4, rowspan=7, padx=20, pady=10)

    # Function to update and display entered details in the right-side box
    def display_entered_details():
        # Get the entered values
        operation = operation_var.get()
        main_ledger = main_ledger_var.get()
        code = code_var.get()
        name = name_var.get()
        

        # Clear previous details
        for widget in details_frame.winfo_children():
            widget.destroy()

        # Display the new details in a label
        details_label = tk.Label(
            details_frame,
            text=f"Operation: {operation}\n"
                 f"Main Ledger: {main_ledger}\n"
                 f"Code: {code}\n"
                 f"Name: {name}\n",
            font=("Arial", 12),
            bg="lightgray",
            justify="left"
        )
        details_label.pack(padx=10, pady=10)

    # Button Actions
    def save_entry():
        if (
            operation_var.get() and
            main_ledger_var.get() and
            code_var.get() and
            name_var.get() 
        ):
            messagebox.showinfo("Saved", "Details Saved Successfully!")
            display_entered_details()
        else:
            messagebox.showwarning("Missing Fields", "Please fill all the fields!")

    def cancel_entry():
        # Clear all fields
        operation_var.set("Addition")
        main_ledger_var.set("")
        code_var.set("")
        name_var.set("")
        

    # Buttons
    tk.Button(
        sub_ledger_window,
        text="Save",
        font=("Arial", 12),
        bg="green",
        fg="white",
        width=10,
        command=save_entry
    ).grid(row=6, column=0, pady=20)

    tk.Button(
        sub_ledger_window,
        text="Cancel",
        font=("Arial", 12),
        bg="orange",
        fg="white",
        width=10,
        command=cancel_entry
    ).grid(row=6, column=1, pady=20)

    tk.Button(
        sub_ledger_window,
        text="Exit",
        font=("Arial", 12),
        bg="red",
        fg="white",
        width=10,
        command=sub_ledger_window.destroy
    ).grid(row=6, column=2, pady=20)

    tk.Button(
        sub_ledger_window,
        text="Name List",
        font=("Arial", 12),
        bg="blue",
        fg="white",
        width=10,
        command=lambda: messagebox.showinfo("Name List", "Display the name list logic here.")
    ).grid(row=6, column=3, pady=20)
    ##### end the sub product ended 
### sub product master page ended