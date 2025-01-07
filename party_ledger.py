import tkinter as tk
from tkinter import ttk

def party_ledger(root):   #### party ledger page start
    party_ledger_window = tk.Toplevel()
    party_ledger_window.title("Party Ledger")
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Set the window size to cover the full screen
    party_ledger_window.geometry(f"{screen_width}x{screen_height}")  
    party_ledger_window.configure(bg="lightblue")

    # Create a frame to hold all content, making it top-center-aligned
    content_frame = tk.Frame(party_ledger_window, bg="lightblue")
    content_frame.place(relx=0.5, rely=0, anchor="n")  # Top-center alignment

    # Title Label (Top Label)
    title_frame = tk.Frame(content_frame, bg="lightblue")
    title_frame.pack(pady=20)
    party_ledger_label = tk.Label(title_frame, text="Party Ledger", font=("Times", 25, "bold"), bg="lightblue", fg="green")
    party_ledger_label.pack()

    # Select Ledger (Row 1)
    row1_frame = tk.Frame(content_frame, bg="lightblue")
    row1_frame.pack(fill='x', pady=10)
    tk.Label(row1_frame, text="Select Ledger:", font=("Times", 15), bg="lightblue").pack(side="left", padx=10)
    tk.Radiobutton(row1_frame, text="Nil Bal", bg="lightblue", font=("Times", 15)).pack(side="left", padx=5)
    tk.Radiobutton(row1_frame, text="Only Bal", bg="lightblue", font=("Times", 15)).pack(side="left", padx=5)
    tk.Radiobutton(row1_frame, text="Both", bg="lightblue", font=("Times", 15)).pack(side="left", padx=5)

    # Select Account (Row 2)
    row2_frame = tk.Frame(content_frame, bg="lightblue")
    row2_frame.pack(fill='x', pady=10)
    tk.Label(row2_frame, text="Select Account:", font=("Times", 15), bg="lightblue").pack(side="left", padx=10)
    tk.Radiobutton(row2_frame, text="All A/C", bg="lightblue", font=("Times", 15)).pack(side="left", padx=5)
    tk.Radiobutton(row2_frame, text="Individual", bg="lightblue", font=("Times", 15)).pack(side="left", padx=5)

    # Main Ledger Combobox (Row 3)
    row3_frame = tk.Frame(content_frame, bg="lightblue")
    row3_frame.pack(fill='x', pady=10)
    tk.Label(row3_frame, text="Main Ledger:", font=("Times", 15), bg="lightblue").pack(side="left", padx=10)
    main_ledger_combobox = ttk.Combobox(row3_frame, font=("Times", 15), width=20)
    main_ledger_combobox.pack(side="left", padx=10)

    # Sub Ledger Combobox (Row 4)
    row4_frame = tk.Frame(content_frame, bg="lightblue")
    row4_frame.pack(fill='x', pady=10)
    tk.Label(row4_frame, text="Sub Ledger:", font=("Times", 15), bg="lightblue").pack(side="left", padx=10)
    sub_ledger_combobox = ttk.Combobox(row4_frame, font=("Times", 15), width=20)
    sub_ledger_combobox.pack(side="left", padx=10)

    # From Date (Row 5)
    row5_frame = tk.Frame(content_frame, bg="lightblue")
    row5_frame.pack(fill='x', pady=10)
    tk.Label(row5_frame, text="From Date:", font=("Times", 15), bg="lightblue").pack(side="left", padx=10)
    from_date_entry = tk.Entry(row5_frame, font=("Times", 15), width=20)
    from_date_entry.pack(side="left", padx=10)

    # To Date (Row 6)
    row6_frame = tk.Frame(content_frame, bg="lightblue")
    row6_frame.pack(fill='x', pady=10)
    tk.Label(row6_frame, text="To Date:", font=("Times", 15), bg="lightblue").pack(side="left", padx=10)
    to_date_entry = tk.Entry(row6_frame, font=("Times", 15), width=20)
    to_date_entry.pack(side="left", padx=10)

    # Buttons (Row 7)
    row7_frame = tk.Frame(content_frame, bg="lightblue")
    row7_frame.pack(fill='x', pady=20)
    
    tk.Button(row7_frame, text="Report", font=("Times", 15), bg="green", fg="white", width=10,
              command=lambda: print(f"Generating report from {from_date_entry.get()} to {to_date_entry.get()}")).pack(side="left", padx=10)
    
    tk.Button(row7_frame, text="Cancel", font=("Times", 15), bg="orange", fg="white", width=10,
              command=lambda: [from_date_entry.delete(0, tk.END), to_date_entry.delete(0, tk.END)]).pack(side="left", padx=10)
    
    tk.Button(row7_frame, text="Exit", font=("Times", 15), bg="red", fg="white", width=10,
              command=party_ledger_window.destroy).pack(side="left", padx=10)

### party ledger page ended
