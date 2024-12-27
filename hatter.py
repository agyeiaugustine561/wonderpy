import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("Pharmacy Management System")
root.geometry("1200x700")
root.configure(bg='#f0f0f0')

# Header
header = tk.Frame(root, bg='#007acc', height=50)
header.pack(fill='x')

title = tk.Label(header, text="Pharmacy Management System", bg='#007acc', fg='white', font=('Arial', 20, 'bold'))
title.pack(pady=10)

# Sidebar for Navigation
sidebar = tk.Frame(root, bg='#2e6e99', width=200)
sidebar.pack(side='left', fill='y')

sidebar_title = tk.Label(sidebar, text="Inventory", bg='#2e6e99', fg='white', font=('Arial', 14, 'bold'))
sidebar_title.pack(pady=10)

insert_medicine_btn = tk.Button(sidebar, text="Insert Medicine Info", bg='#357ca5', fg='white', bd=0, font=('Arial', 12), pady=10)
insert_medicine_btn.pack(fill='x')

purchase_statement_btn = tk.Button(sidebar, text="Purchase Statement", bg='#2e6e99', fg='white', bd=0, font=('Arial', 12), pady=10)
purchase_statement_btn.pack(fill='x')

supplier_payment_btn = tk.Button(sidebar, text="Supplier Payment", bg='#2e6e99', fg='white', bd=0, font=('Arial', 12), pady=10)
supplier_payment_btn.pack(fill='x')

# Main Content Frame
content_frame = tk.Frame(root, bg='white', padx=10, pady=10)
content_frame.pack(side='right', fill='both', expand=True)

# Medicine Purchase Form
form_frame = tk.Frame(content_frame, bg='#d0eaf4', padx=10, pady=10)
form_frame.pack(fill='x', pady=10)

form_title = tk.Label(form_frame, text="Insert Medicine Purchase Information", bg='#d0eaf4', font=('Arial', 14, 'bold'))
form_title.grid(row=0, column=0, columnspan=4, pady=10)

# Create the form fields
fields = [
    ("Medicine Name", 0, 0),
    ("Generic", 0, 1),
    ("Presentation", 0, 2),
    ("Supplier Company", 0, 3),
    ("Total Quantity", 1, 0),
    ("Unit Price", 1, 1),
    ("Total Amount", 1, 2),
    ("Selling Price", 1, 3),
    ("Volume", 2, 0),
    ("Purchase Paid", 2, 1),
    ("Purchase Due", 2, 2),
    ("Expire Date", 2, 3)
]

for field, row, col in fields:
    label = tk.Label(form_frame, text=field, bg='#d0eaf4', font=('Arial', 12))
    label.grid(row=row + 1, column=col, padx=10, pady=5, sticky='e')
    entry = tk.Entry(form_frame)
    entry.grid(row=row + 1, column=col + 1, padx=10, pady=5)

# Create button to submit form
submit_button = tk.Button(form_frame, text="Create", bg='#007acc', fg='white', font=('Arial', 12, 'bold'))
submit_button.grid(row=4, column=0, columnspan=4, pady=10)

# Medicine List Table
table_frame = tk.Frame(content_frame)
table_frame.pack(fill='both', expand=True)

columns = ("#", "Details", "Supplier", "Available Qty", "Unit Price", "Total Amount", "Selling Price", "Paid", "Due", "Expiry", "Action")
tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)

# Define headings and column width
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(fill='both', expand=True)

# Sample data for the table
data = [
    (1, "Medicine: Ace Plus\nGeneric: Paracetamol\nPresentation: Tablet", "Square Pharmaceuticals Ltd.", 190, "$2.52", "$504", "$3", "$350", "$154", "2021-01-01", ""),
    (2, "Medicine: Napa Extra\nGeneric: Paracetamol\nPresentation: Tablet", "Beximco Pharmaceuticals Ltd.", 170, "$2.50", "$500", "$3", "$300", "$200", "2020-01-01", "")
]

# Insert sample data into the table
for item in data:
    tree.insert('', 'end', values=item)

root.mainloop()
