import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("Pharmacy Management System - Sales Statement")
root.geometry("900x500")
root.configure(bg='#f0f0f0')

# Top header
header = tk.Frame(root, bg="#87CEEB", height=50)
header.pack(fill=tk.X)

header_label = tk.Label(header, text="Pharmacy Management System", font=("Arial", 18), bg="#87CEEB", fg="white")
header_label.pack(pady=10)

# Sales Statement Form Frame
form_frame = tk.Frame(root, bg="white", bd=1, relief="solid")
form_frame.place(x=50, y=80, width=800, height=100)

# Date From Label and Entry
date_from_label = tk.Label(form_frame, text="Date From:", font=("Arial", 12), bg="white")
date_from_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
date_from_entry = tk.Entry(form_frame, font=("Arial", 12))
date_from_entry.grid(row=0, column=1, padx=10, pady=10)

# Date To Label and Entry
date_to_label = tk.Label(form_frame, text="Date To:", font=("Arial", 12), bg="white")
date_to_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
date_to_entry = tk.Entry(form_frame, font=("Arial", 12))
date_to_entry.grid(row=0, column=3, padx=10, pady=10)

# Search Button
search_button = tk.Button(form_frame, text="Search", font=("Arial", 12), bg="#4682B4", fg="white", padx=10, pady=5)
search_button.grid(row=0, column=4, padx=10, pady=10)

# Data Table Frame
table_frame = tk.Frame(root, bg="white", bd=1, relief="solid")
table_frame.place(x=50, y=200, width=800, height=200)

# Data Table (Treeview)
columns = ("Date", "Invoice", "Medicine", "Unit Price", "Quantity", "Total Price", "Amount", "Discount", "Total Amount")

data_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
data_table.pack(fill=tk.BOTH, expand=True)

# Define headings
for col in columns:
    data_table.heading(col, text=col)
    data_table.column(col, width=100)

# Sample Data
data_table.insert("", "end", values=("10/06/22", "8", "Med 101", "$35", "2", "$70", "$70", "$0", "$70"))
data_table.insert("", "end", values=("10/06/22", "9", "Med 101", "$35", "5", "$175", "$175", "$0", "$175"))

# Footer
footer = tk.Label(root, text="© CI Pharmacy Sales and Inventory System, 2022", font=("Arial", 10), bg="#87CEEB", fg="white")
footer.pack(side=tk.BOTTOM, fill=tk.X)

# Run the application
root.mainloop()
