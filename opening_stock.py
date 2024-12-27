import tkinter as tk
from tkinter import ttk, messagebox

def opening_stock(root):  ### start the opening stock   
    opening_stock_window = tk.Toplevel()
    opening_stock_window.title("Opening Stock")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    opening_stock_window.geometry(f"{screen_width}x{screen_height}")
    opening_stock_window.configure(bg="lightblue")

    # Variables for input fields
    operation_var = tk.StringVar(value="Correction")  # Default radio button selection
    main_product_var = tk.StringVar()  # Dropdown selection
    sub_product_var = tk.StringVar()  # Dropdown selection
    pcs_var = tk.StringVar()
    gross_wt_var = tk.StringVar()
    melting_var = tk.StringVar()
    net_wt_var = tk.StringVar()
    rate_var = tk.StringVar()
    mc_var = tk.StringVar()

    # First Line: Radio Buttons for Operations
    tk.Label(
        opening_stock_window,
        text="Select Operation:",
        font=("Arial", 12, "bold"),
        bg="lightblue"
    ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

    operations = ["Correction", "Deletion", "View"]
    for i, operation in enumerate(operations):
        tk.Radiobutton(
            opening_stock_window,
            text=operation,
            variable=operation_var,
            value=operation,
            font=("Arial", 10),
            bg="lightblue"
        ).grid(row=0, column=i + 1, padx=10)

    # Second Line: Main Product Dropdown
    tk.Label(
        opening_stock_window,
        text="Main Product:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=1, column=0, sticky="w", padx=10, pady=10)

    main_product_options = ["Product 1", "Product 2", "Product 3"]  # Example options
    main_product_dropdown = ttk.Combobox(
        opening_stock_window,
        textvariable=main_product_var,
        values=main_product_options,
        state="readonly",
        width=30
    )
    main_product_dropdown.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

    # Third Line: Sub Product Dropdown
    tk.Label(
        opening_stock_window,
        text="Sub Product:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=2, column=0, sticky="w", padx=10, pady=10)

    sub_product_options = ["Sub Product A", "Sub Product B", "Sub Product C"]  # Example options
    sub_product_dropdown = ttk.Combobox(
        opening_stock_window,
        textvariable=sub_product_var,
        values=sub_product_options,
        state="readonly",
        width=30
    )
    sub_product_dropdown.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

    # Fourth Line: Pcs
    tk.Label(
        opening_stock_window,
        text="Pcs:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=3, column=0, sticky="w", padx=10, pady=10)

    pcs_entry = tk.Entry(
        opening_stock_window,
        textvariable=pcs_var,
        font=("Arial", 12),
        width=30
    )
    pcs_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

    # Fifth Line: Gross Weight
    tk.Label(
        opening_stock_window,
        text="Gross Weight:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=4, column=0, sticky="w", padx=10, pady=10)

    gross_wt_entry = tk.Entry(
        opening_stock_window,
        textvariable=gross_wt_var,
        font=("Arial", 12),
        width=30
    )
    gross_wt_entry.grid(row=4, column=1, columnspan=3, padx=10, pady=10)

    # Sixth Line: Melting Weight
    tk.Label(
        opening_stock_window,
        text="Melting Weight:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=5, column=0, sticky="w", padx=10, pady=10)

    melting_entry = tk.Entry(
        opening_stock_window,
        textvariable=melting_var,
        font=("Arial", 12),
        width=30
    )
    melting_entry.grid(row=5, column=1, columnspan=3, padx=10, pady=10)

    # Seventh Line: Net Weight
    tk.Label(
        opening_stock_window,
        text="Net Weight:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=6, column=0, sticky="w", padx=10, pady=10)

    net_wt_entry = tk.Entry(
        opening_stock_window,
        textvariable=net_wt_var,
        font=("Arial", 12),
        width=30
    )
    net_wt_entry.grid(row=6, column=1, columnspan=3, padx=10, pady=10)

    # Eighth Line: Rate
    tk.Label(
        opening_stock_window,
        text="Rate:",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=7, column=0, sticky="w", padx=10, pady=10)

    rate_entry = tk.Entry(
        opening_stock_window,
        textvariable=rate_var,
        font=("Arial", 12),
        width=30
    )
    rate_entry.grid(row=7, column=1, columnspan=3, padx=10, pady=10)

    # Ninth Line: MC@
    tk.Label(
        opening_stock_window,
        text="MC@: ",
        font=("Arial", 12),
        bg="lightblue"
    ).grid(row=8, column=0, sticky="w", padx=10, pady=10)

    mc_entry = tk.Entry(
        opening_stock_window,
        textvariable=mc_var,
        font=("Arial", 12),
        width=30
    )
    mc_entry.grid(row=8, column=1, columnspan=3, padx=10, pady=10)

    # Function to save the entered details
    def save_entry():
        if (
            operation_var.get() and
            main_product_var.get() and
            sub_product_var.get() and
            pcs_var.get() and
            gross_wt_var.get() and
            melting_var.get() and
            net_wt_var.get() and
            rate_var.get() and
            mc_var.get()
        ):
            messagebox.showinfo("Saved", "Details Saved Successfully!")
        else:
            messagebox.showwarning("Missing Fields", "Please fill all the fields!")

    def cancel_entry():
        # Clear all fields
        operation_var.set("Correction")
        main_product_var.set("")
        sub_product_var.set("")
        pcs_var.set("")
        gross_wt_var.set("")
        melting_var.set("")
        net_wt_var.set("")
        rate_var.set("")
        mc_var.set("")

    # Buttons
    tk.Button(
        opening_stock_window,
        text="Save",
        font=("Arial", 12),
        bg="green",
        fg="white",
        width=10,
        command=save_entry
    ).grid(row=9, column=0, pady=20)

    tk.Button(
        opening_stock_window,
        text="Cancel",
        font=("Arial", 12),
        bg="orange",
        fg="white",
        width=10,
        command=cancel_entry
    ).grid(row=9, column=1, pady=20)

    tk.Button(
        opening_stock_window,
        text="Exit",
        font=("Arial", 12),
        bg="red",
        fg="white",
        width=10,
        command=opening_stock_window.destroy
    ).grid(row=9, column=2, pady=20)
### opening stock page ended  