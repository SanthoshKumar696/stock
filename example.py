import tkinter as tk
from tkinter import ttk

def create_treeview_with_lines():
    # Create root window
    root = tk.Tk()
    root.geometry("800x400")

    # Create a canvas for vertical lines
    canvas = tk.Canvas(root, height=400, width=800)
    canvas.pack(side="top", fill="both", expand=True)

    # Create a Treeview widget
    tree = ttk.Treeview(canvas, columns=("ID", "Name", "Age"))
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")

    tree.column("ID", width=100, anchor="center")
    tree.column("Name", width=200, anchor="center")
    tree.column("Age", width=100, anchor="center")

    # Insert some example data
    tree.insert("", "end", values=("1", "John", "25"))
    tree.insert("", "end", values=("2", "Jane", "30"))

    # Pack the treeview widget
    tree.place(x=0, y=0)

    # Draw vertical lines between columns on the canvas
    canvas.create_line(100, 0, 100, 400, fill="black")  # Line after first column
    canvas.create_line(300, 0, 300, 400, fill="black")  # Line after second column

    # Start the Tkinter main loop
    root.mainloop()

create_treeview_with_lines()
