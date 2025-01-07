import tkinter as tk
from tkinter import messagebox

def report_action():
    print("Report Button Clicked")

def cancel_action():
    print("Cancel Button Clicked")

def exit_action(root):
    root.quit()

def party_balance(root):  # Party Balance Page Start
    # Create a new Toplevel window (this will open a new window)
    party_balance_window = tk.Toplevel()
    party_balance_window.title("Party Balance")
    
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Make the window full-screen
    party_balance_window.geometry(f"{screen_width}x{screen_height}")
    party_balance_window.configure(bg="lightblue")

    # Create a frame to hold all content
    content_frame = tk.Frame(party_balance_window, bg="lightblue", padx=20)
    content_frame.pack(pady=20)  # Centering the content frame at the top with padding

    # Title Label (Top Label)
    title_frame = tk.Frame(content_frame, bg="lightblue")
    title_frame.pack(pady=20)
    party_balance_label = tk.Label(title_frame, text="Party Balance", font=("Times", 25, "bold"), bg="lightblue", fg="green")
    party_balance_label.pack()

    # Select Ledger (Row 1)
    row1_frame = tk.Frame(content_frame, bg="lightblue")
    row1_frame.pack(fill='x', pady=10)
    tk.Label(row1_frame, text="Select Ledger:", font=("Times", 15), bg="lightblue").pack(side="left", padx=10)
    ledger_selection = tk.StringVar(value="All Ledger")
    tk.Radiobutton(row1_frame, text="All Ledger", variable=ledger_selection, value="All Ledger", bg="lightblue", font=("Times", 15)).pack(side="left", padx=5)
    tk.Radiobutton(row1_frame, text="Individual Ledger", variable=ledger_selection, value="Individual Ledger", bg="lightblue", font=("Times", 15)).pack(side="left", padx=5)

    # Select Payment Type (Row 2)
    row2_frame = tk.Frame(content_frame, bg="lightblue")
    row2_frame.pack(fill='x', pady=10)
    tk.Label(row2_frame, text="Select Payment Type:", font=("Times", 15), bg="lightblue").pack(side="left", padx=10)
    payment_type = tk.StringVar(value="Rs")
    tk.Radiobutton(row2_frame, text="Rs", variable=payment_type, value="Rs", bg="lightblue", font=("Times", 15)).pack(side="left", padx=5)
    tk.Radiobutton(row2_frame, text="Metal", variable=payment_type, value="Metal", bg="lightblue", font=("Times", 15)).pack(side="left", padx=5)
    tk.Radiobutton(row2_frame, text="Rs & Metal", variable=payment_type, value="Rs & Metal", bg="lightblue", font=("Times", 15)).pack(side="left", padx=5)

    # From Date (Row 3)
    row3_frame = tk.Frame(content_frame, bg="lightblue")
    row3_frame.pack(fill='x', pady=10)
    tk.Label(row3_frame, text="From Date:", font=("Times", 15), bg="lightblue").pack(side="left", padx=10)
    from_date_entry = tk.Entry(row3_frame, font=("Times", 15), width=20)
    from_date_entry.pack(side="left", padx=10)

    # To Date (Row 4)
    row4_frame = tk.Frame(content_frame, bg="lightblue")
    row4_frame.pack(fill='x', pady=10)
    tk.Label(row4_frame, text="To Date:", font=("Times", 15), bg="lightblue").pack(side="left", padx=10)
    to_date_entry = tk.Entry(row4_frame, font=("Times", 15), width=20)
    to_date_entry.pack(side="left", padx=10)

    # Buttons (Row 5)
    row5_frame = tk.Frame(content_frame, bg="lightblue")
    row5_frame.pack(fill='x', pady=20)

    tk.Button(row5_frame, text="Report", font=("Times", 13), bg="green", fg="white", width=10,
              command=lambda: print(f"Generating report from {from_date_entry.get()} to {to_date_entry.get()}")).pack(side="left", padx=10)
    
    tk.Button(row5_frame, text="Cancel", font=("Times", 13), bg="orange", fg="white", width=10,
              command=lambda: [from_date_entry.delete(0, tk.END), to_date_entry.delete(0, tk.END)]).pack(side="left", padx=10)
    
    tk.Button(row5_frame, text="Exit", font=("Times", 13), bg="red", fg="white", width=10,
              command=party_balance_window.destroy).pack(side="left", padx=10)


