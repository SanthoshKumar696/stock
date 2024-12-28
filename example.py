import sqlite3
import tkinter as tk

# Step 1: Fetch data from the database
def fetch_data():
    try:
        # Connect to the database
        conn = sqlite3.connect('stock.db')  # Make sure this path is correct
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM saved_data")  # Replace with your actual table name
        data = cursor.fetchall()  # Fetch all data from the table
        columns = [description[0] for description in cursor.description]  # Get column names
        conn.close()
        return columns, data
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return [], []

# Step 2: Function to display data in a table-like format in Tkinter with borders
def display_table():
    columns, data = fetch_data()

    if not columns or not data:  # If no data or columns, show an error
        print("No data available or error fetching data.")
        return

    # Step 3: Create Tkinter window
    root = tk.Tk()
    root.title("Client Data Table")
    root.geometry("800x600")  # Set the window size

    # Step 4: Create header row (column names)
    for col_num, column in enumerate(columns):
        header_label = tk.Label(root, text=column, font=("Arial", 12, "bold"), relief="solid", width=20, anchor="w", bg="#f2f2f2")
        header_label.grid(row=0, column=col_num, padx=5, pady=5, sticky="nsew")

    # Step 5: Create data rows with borders
    for row_num, row in enumerate(data, start=1):
        for col_num, item in enumerate(row):
            row_label = tk.Label(root, text=item, font=("Arial", 12), relief="solid", width=20, anchor="w")
            # Alternate row colors
            if row_num % 2 == 0:
                row_label.config(bg="#f9f9f9")
            row_label.grid(row=row_num, column=col_num, padx=5, pady=5, sticky="nsew")

    # Adjust window resizing behavior
    for col_num in range(len(columns)):
        root.grid_columnconfigure(col_num, weight=1)

    # Make rows and columns resize with the window
    for row_num in range(len(data) + 1):  # Add 1 for the header row
        root.grid_rowconfigure(row_num, weight=1)

    # Start the Tkinter event loop
    root.mainloop()

# Step 7: Execute the table display function
display_table()
