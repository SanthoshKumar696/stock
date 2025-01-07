import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Jewelry Inventory Management System")

# Create a frame for the Treeview and Scrollbar with a specific size (fix width and height)
frame = tk.Frame(root, width=800, height=400)  # Fixed size for the frame
frame.pack_propagate(False)  # Prevent the frame from resizing to fit its content
frame.pack(padx=10, pady=10)

# Create the Treeview widget with many columns
columns = ("ID", "Name", "Price", "Quantity", "Category", "Material", "Color", "Size", "Weight", "Supplier")
tree = ttk.Treeview(frame, columns=columns, show="headings")

# Set column headings
for col in columns:
    tree.heading(col, text=col)

# Set column widths (you can adjust these based on your data)
tree.column("ID", width=50)
tree.column("Name", width=150)
tree.column("Price", width=100)
tree.column("Quantity", width=100)
tree.column("Category", width=120)
tree.column("Material", width=120)
tree.column("Color", width=80)
tree.column("Size", width=80)
tree.column("Weight", width=100)
tree.column("Supplier", width=150)

# Insert some example items (you can add your actual inventory data here)
tree.insert("", "end", values=("1", "Ring", "$100", "5", "Jewelry", "Gold", "Gold", "Medium", "50g", "Supplier A"))
tree.insert("", "end", values=("2", "Necklace", "$200", "3", "Jewelry", "Silver", "Silver", "Large", "80g", "Supplier B"))
tree.insert("", "end", values=("3", "Earrings", "$50", "8", "Jewelry", "Platinum", "Platinum", "Small", "30g", "Supplier C"))
tree.insert("", "end", values=("4", "Bracelet", "$150", "2", "Jewelry", "Leather", "Brown", "Medium", "60g", "Supplier D"))

# Create a horizontal scrollbar linked to the Treeview
h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
tree.configure(xscrollcommand=h_scrollbar.set)
h_scrollbar.pack(side="bottom", fill="x")

# Pack the Treeview widget inside the frame (do not expand to fill)
tree.pack(fill="both", expand=False)

# Start the Tkinter event loop
root.mainloop()
