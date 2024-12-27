import tkinter as tk
from tkinter import messagebox

def sales_page(parent):
    # Create the form frame
    form_frame = tk.Frame(parent, padx=20, pady=20)
    form_frame.grid(row=0, column=0, sticky=tk.W + tk.E)

    # Form title
    form_title = tk.Label(form_frame, text="Sales Medicine", font=("Arial", 16))
    form_title.grid(row=0, column=0, columnspan=4, pady=10)

    # Create form entries (Generic Name and Medicine Name)
    entries = {}
    entries['generic_name'] = create_form_entry_horizontal(form_frame, "Generic Name", 1)
    entries['medicine_name'] = create_form_entry_horizontal(form_frame, "Medicine Name", 1, col_offset=2)

    # Add button
    add_button = tk.Button(form_frame, text="ADD", bg="#5cb85c", fg="white", command=lambda: add_medicine(entries, table_frame))
    add_button.grid(row=2, column=0, columnspan=4, pady=10)

    # Create table frame for the data table
    table_frame = create_table(parent)
    
    return entries, table_frame

def create_form_entry_horizontal(form_frame, label_text, row, col_offset=0, entry_type="text"):
    # Create and place the label (placed horizontally, i.e., side by side with the entry)
    label = tk.Label(form_frame, text=label_text)
    label.grid(row=row, column=col_offset, pady=5, sticky=tk.W)

    # Create the appropriate entry widget (both Generic Name and Medicine Name are now text entries)
    entry = tk.Entry(form_frame)

    # Place the entry widget right next to the label
    entry.grid(row=row, column=col_offset + 1, pady=5, sticky=tk.W)
    return entry

def create_table(parent):
    # Create a frame for the table
    table_frame = tk.Frame(parent, padx=20, pady=20)
    table_frame.grid(row=1, column=0, sticky=tk.W + tk.E)

    # Add the table headers
    headers = ["Generic Name", "Medicine Name", "Action"]
    for i, header in enumerate(headers):
        label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"), bg="#f7f7f7", padx=10, pady=5, borderwidth=1, relief="groove")
        label.grid(row=0, column=i, sticky=tk.W+tk.E)

    return table_frame

def add_medicine(entries, table_frame):
    # Get the values from the form entries
    generic_name = entries['generic_name'].get()
    medicine_name = entries['medicine_name'].get()

    # Validate input
    if not generic_name or not medicine_name:
        messagebox.showerror("Error", "Please fill out both fields.")
        return

    # Add a new row to the table with the entered data
    add_row(table_frame, generic_name, medicine_name)

    # Clear the entry fields after adding
    entries['generic_name'].delete(0, tk.END)
    entries['medicine_name'].delete(0, tk.END)
    
def add_row(table_frame, generic_name, medicine_name):
    # Calculate the current row number based on the number of widgets already in the table
    row = len(table_frame.grid_slaves()) // 3  # Each row has 3 columns (Generic Name, Medicine Name, Action)

    # Add the data as labels in the new row
    generic_label = tk.Label(table_frame, text=generic_name, padx=10, pady=5, borderwidth=2, relief="groove")
    generic_label.grid(row=row+1, column=0, sticky=tk.W+tk.E)

    medicine_label = tk.Label(table_frame, text=medicine_name, padx=10, pady=5, borderwidth=2, relief="groove")
    medicine_label.grid(row=row+1, column=1, sticky=tk.W+tk.E)

    # Add delete button for each row
    delete_button = tk.Button(table_frame, text="Delete", command=lambda: delete_row(table_frame, row+1), bg="red", fg="white")
    delete_button.grid(row=row+1, column=2, padx=5, pady=5)

def delete_row(table_frame, row):
    # Remove all widgets in the specified row
    for widget in table_frame.grid_slaves(row=row):
        widget.destroy()

# Create the main window
root = tk.Tk()
root.title("Pharmacy Management System")

# Create sales page and retrieve entries and table frame
entries, table_frame = sales_page(root)

# Start the main event loop
root.mainloop()
