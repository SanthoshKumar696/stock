import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("Wholesale Jewelry Inventory Management")
root.geometry("900x400")  # Fixed small screen size

# Style for the Treeview widget
style = ttk.Style()
style.theme_use("clam")  # Use 'clam' for more customization options

# Customizing the heading
style.configure("Treeview.Heading", 
                font=("Arial", 10, "bold"), 
                foreground="white", 
                background="teal", 
                borderwidth=1, 
                relief="solid")

# Customizing the Treeview rows
style.configure("Treeview", 
                rowheight=25,  # Row height
                font=("Arial", 9))  # Font for rows

# Alternating row colors (striped pattern)
style.map("Treeview", 
          background=[("selected", "lightblue")],
          foreground=[("selected", "black")])

# Frame for the Treeview and Scrollbars
tree_frame = tk.Frame(root, bg="lightseagreen")
tree_frame.pack(pady=5, fill=tk.BOTH, expand=True)

# Scrollbars
scroll_y = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

# Create the Treeview widget
columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#12", "#13", "#14", "#15")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12,
                    yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

# Set headings for each column
headings = ["SLNo", "Date", "Name", "Main Product", "Design", "Transaction", "Gross", 
            "Stones", "Touch", "Net Wt", "MC@", "MC", "Rate", "Amount", "Narration"]

for i, heading in enumerate(headings, start=1):
    tree.heading(f"#{i}", text=heading)

# Set column width and alignment
column_settings = [
    (30, tk.CENTER), (70, tk.CENTER), (120, tk.W), (120, tk.W), (80, tk.W), (100, tk.W),
    (50, tk.CENTER), (50, tk.CENTER), (50, tk.CENTER), (70, tk.CENTER), (50, tk.CENTER),
    (40, tk.CENTER), (70, tk.CENTER), (90, tk.CENTER), (180, tk.W)
]

for i, (width, anchor) in enumerate(column_settings, start=1):
    tree.column(f"#{i}", width=width, anchor=anchor)

# Pack the Treeview
tree.grid(row=0, column=0, sticky="nsew")

# Configure scrollbars
scroll_y.config(command=tree.yview)
scroll_x.config(command=tree.xview)
scroll_y.grid(row=0, column=1, sticky="ns")
scroll_x.grid(row=1, column=0, sticky="ew")

# Configure the grid to make the Treeview expand with the frame
tree_frame.grid_rowconfigure(0, weight=1)
tree_frame.grid_columnconfigure(0, weight=1)

# Add sample data with alternating row colors
data = [
    (1, "2025-01-14", "John Doe", "Ring", "Modern", "Purchase", 12.5, 3, "22K", 9.5, 500, 250, 6000, 7200, "New customer"),
    (2, "2025-01-15", "Jane Smith", "Necklace", "Classic", "Sale", 25.0, 5, "24K", 20.0, 1000, 500, 8000, 20000, "Gift order"),
    # Add more rows as needed...
]

for idx, row in enumerate(data):
    tag = "oddrow" if idx % 2 == 0 else "evenrow"
    tree.insert("", "end", values=row, tags=(tag,))

# Add striped row colors
tree.tag_configure("oddrow", background="white")
tree.tag_configure("evenrow", background="lightgrey")

# Start the Tkinter event loop
root.mainloop()

