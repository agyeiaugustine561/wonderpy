import tkinter as tk
from tkinter import messagebox

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

# Define form fields
entries = {}
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

# Create form entries dynamically
for field, row, col in fields:
    label = tk.Label(form_frame, text=field, bg='#d0eaf4', font=('Arial', 12))
    label.grid(row=row + 1, column=col, padx=10, pady=5, sticky='e')
    entry = tk.Entry(form_frame)
    entry.grid(row=row + 1, column=col + 1, padx=10, pady=5)
    entries[field.lower().replace(" ", "_")] = entry

# Create button to submit form
submit_button = tk.Button(form_frame, text="Create", bg='#007acc', fg='white', font=('Arial', 12, 'bold'),
                          command=lambda: add_medicine(entries, table_frame))
submit_button.grid(row=4, column=0, columnspan=4, pady=10)

# Medicine List Table
def create_table(parent_frame):
    table_frame = tk.Frame(parent_frame, bg="white")
    table_frame.pack(fill='both', expand=True)

    # Table headers
    table_title = tk.Label(table_frame, text="Inventory Records", font=("Arial", 16), bg="white")
    table_title.grid(row=0, column=0, columnspan=12, pady=10)

    headers = ["#", "Medicine Name", "Generic", "Presentation", "Supplier", "Available Qty", "Unit Price", "Total", "Selling Price", "Paid", "Due", "Expiry"]
    for i, header in enumerate(headers):
        label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"), bg="#f7f7f7", padx=10, pady=5, borderwidth=1, relief="groove")
        label.grid(row=1, column=i, sticky=tk.W + tk.E)

    return table_frame

# Function to add new medicine record
def add_medicine(entries, table_frame):
    new_record = [
        len(table_frame.grid_slaves()) // 12,  # ID number (based on current number of rows)
        entries["medicine_name"].get(),
        entries["generic"].get(),
        entries["presentation"].get(),
        entries["supplier_company"].get(),
        entries["total_quantity"].get(),
        entries["unit_price"].get(),
        entries["total_amount"].get(),
        entries["selling_price"].get(),
        entries["volume"].get(),
        entries["purchase_paid"].get(),
        entries["purchase_due"].get(),
        entries["expire_date"].get()
    ]
    
    # Validation: Ensure no fields are empty
    if any(not field for field in new_record[1:]):
        messagebox.showerror("Error", "Please fill all fields.")
        return
    
    # Add the new record to the table
    row_num = len(table_frame.grid_slaves()) // 12 + 2
    for i, value in enumerate(new_record):
        label = tk.Label(table_frame, text=value, padx=10, pady=5, borderwidth=2, relief="groove", bg="white")
        label.grid(row=row_num, column=i, sticky=tk.W + tk.E)

# Medicine List Table Frame
table_frame = create_table(content_frame)

root.mainloop()
