import tkinter as tk
from tkinter import messagebox
import os
import subprocess

def create_header(root):
    header_frame = tk.Frame(root, bg="lightblue", padx=10, pady=10)
    header_frame.pack(fill=tk.X)

    title_label = tk.Label(header_frame, text="Pharmacy Management System", bg="#428bca", fg="white", font=("Arial", 18))
    title_label.pack(side=tk.LEFT)

    user_section = tk.Frame(header_frame, bg="#428bca")
    user_section.pack(side=tk.RIGHT)

    staff_label = tk.Label(user_section, text="STAFF", bg="#428bca", fg="white")
    staff_label.pack(side=tk.LEFT, padx=10)

    logout_button = tk.Button(user_section, text="Logout", bg="white", fg="black")
    logout_button.pack(side=tk.LEFT)

def create_form(main_frame, table_frame):
    # Create a white frame to hold the form and table
    form_container = tk.Frame(main_frame, bg="white", padx=160, pady=30, relief="groove", borderwidth=2)
    form_container.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=10, pady=10)

    # Create the form inside the white frame
    form_frame = tk.Frame(form_container, padx=20, pady=20, bg="white")
    form_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

    form_title = tk.Label(form_frame, text="Sales Medicine", font=("Arial", 16), bg="white")
    form_title.grid(row=0, column=0, columnspan=3, pady=10, sticky=tk.W+tk.E)

    # Arrange entries with 2-3 per row and 1 per column
    entries = {}
    entries['date'] = create_form_entry(form_frame, "Date", 1, 0)
    entries['customer_mail'] = create_form_entry(form_frame, "Customer Mail", 1, 1, entry_type="email")
    entries['medicine_name'] = create_form_entry(form_frame, "Medicine Name", 1, 2, entry_type="dropdown")
    
    entries['quantity'] = create_form_entry(form_frame, "Quantity", 2, 0, entry_type="number")
    entries['selling_price'] = create_form_entry(form_frame, "Selling Price", 2, 1)
    
    total_amount_label = tk.Label(form_frame, text="Total Amount", bg="white")
    total_amount_label.grid(row=3, column=0, pady=10, sticky=tk.W)
    entries['total_amount'] = tk.Entry(form_frame, state="readonly")
    entries['total_amount'].grid(row=3, column=1, columnspan=2, pady=10, sticky=tk.W+tk.E)

    add_button = tk.Button(form_frame, text="ADD", bg="#5cb85c", fg="white", command=lambda: add_medicine(entries, table_frame), width=5)
    add_button.grid(row=4, column=0, columnspan=3, pady=5)

    # Add Print button
    print_button = tk.Button(form_frame, text="Print", bg="#428bca", fg="white", command=lambda: print_sales_data(table_frame), width=5)
    print_button.grid(row=5, column=0, columnspan=3, pady=10)

    return entries, form_container

def create_form_entry(form_frame, label_text, row, col, entry_type="text"):
    label = tk.Label(form_frame, text=label_text, bg="white")
    label.grid(row=row, column=col*2, pady=5, sticky=tk.W, padx=5)

    if entry_type == "text":
        entry = tk.Entry(form_frame)
    elif entry_type == "email":
        entry = tk.Entry(form_frame)
    elif entry_type == "number":
        entry = tk.Entry(form_frame)
    elif entry_type == "dropdown":
        var = tk.StringVar()
        entry = tk.OptionMenu(form_frame, var, "-- Select --", "Medicine A", "Medicine B", "Medicine C")
        entry.var = var  # Attach the StringVar to the OptionMenu for later use
    else:
        entry = tk.Entry(form_frame)

    entry.grid(row=row, column=col*2+1, pady=5, sticky=tk.W+tk.E)
    return entry

def create_table(main_frame):
    # Create a canvas and a scrollbar for the table
    canvas = tk.Canvas(main_frame, bg="white")
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the table
    table_frame = tk.Frame(canvas, bg="white")

    # Create a window inside the canvas for the table frame
    canvas.create_window((0, 0), window=table_frame, anchor="nw")

    # Pack the canvas and scrollbar
    canvas.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
    scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S)

    # Configure scrolling region
    table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Table headers
    table_title = tk.Label(table_frame, text="Sales Medicine", font=("Arial", 16), bg="white")
    table_title.grid(row=0, column=0, columnspan=6, pady=10)

    headers = ["Date", "Medicine Name", "Quantity", "Selling Price", "Total", "Action"]
    for i, header in enumerate(headers):
        label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"), bg="#f7f7f7", padx=40, pady=5, borderwidth=1, relief="groove")
        label.grid(row=1, column=i, sticky=tk.W+tk.E)

    return table_frame

def add_medicine(entries, table_frame):
    date = entries['date'].get()
    customer_mail = entries['customer_mail'].get()
    medicine_name = entries['medicine_name'].var.get()  # Get value from StringVar
    quantity = entries['quantity'].get()
    selling_price = entries['selling_price'].get()

    if not date or not medicine_name or not quantity or not selling_price:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    total_amount = float(quantity) * float(selling_price)
    # Insert the new record in the table
    add_row(table_frame, date, medicine_name, quantity, selling_price, total_amount)

    # Clear the entries for the next input
    entries['date'].delete(0, tk.END)
    entries['customer_mail'].delete(0, tk.END)
    entries['medicine_name'].var.set("-- Select --")  # Reset dropdown
    entries['quantity'].delete(0, tk.END)
    entries['selling_price'].delete(0, tk.END)

    # Reset focus to the first entry
    entries['date'].focus_set()

    update_totals(table_frame)

def add_row(table_frame, date, medicine_name, quantity, selling_price, total_amount):
    row = len(table_frame.grid_slaves()) // 6 + 2  # Calculate the new row index
    entries = [date, medicine_name, quantity, selling_price, f"{total_amount:.2f}"]

    for i, entry in enumerate(entries):
        label = tk.Label(table_frame, text=entry, padx=10, pady=5, borderwidth=2, relief="groove", bg="white")
        label.grid(row=row, column=i, sticky=tk.W+tk.E)

    add_action_buttons(table_frame, row)

def add_action_buttons(table_frame, row):
    edit_button = tk.Button(table_frame, text="Edit", bg="#f0ad4e", fg="white", command=lambda: edit_medicine(row))
    edit_button.grid(row=row, column=5, padx=5, pady=5)

    delete_button = tk.Button(table_frame, text="Delete", bg="#d9534f", fg="white", command=lambda: delete_medicine(table_frame, row))
    delete_button.grid(row=row, column=6, padx=5, pady=5)

def edit_medicine(row):
    messagebox.showinfo("Edit", f"Edit medicine at row {row}")

def delete_medicine(table_frame, row):
    for widget in table_frame.grid_slaves(row=row):
        widget.destroy()

    update_totals(table_frame)

def update_totals(table_frame):
    total = 0
    for widget in table_frame.grid_slaves():
        if widget.grid_info()["column"] == 4:  # Total column
            total += float(widget.cget("text"))
    print(f"Total sales: {total}")

def print_sales_data(table_frame, layout="four_column"):
    """Function to print sales data with various layouts."""
    sales_data = []
    for row in range(2, len(table_frame.grid_slaves()) // 6 + 2):  # Skip header row
        row_data = []
        for col in range(6):
            widget = table_frame.grid_slaves(row=row, column=col)
            if widget:
                row_data.append(widget[0].cget("text"))
        sales_data.append(row_data)

    # Format the data based on the selected layout
    formatted_data = format_data(sales_data, layout)

    # Save the data to a file
    with open("sales_report.txt", "w") as f:
        f.write(formatted_data)

    # Print the file using the default system print
    if os.name == 'nt':  # Windows
        os.startfile("sales_report.txt", "print")
    else:  # macOS and Linux
        subprocess.run(["lpr", "sales_report.txt"])
def format_data(data, layout):
    """Format the sales data according to the specified layout."""
    if layout == "three_column":
        headers = ["Date", "Medicine Name", "Total"]
        col_widths = [20, 30, 15]
    elif layout == "four_column":
        headers = ["Date", "Medicine Name", "Quantity", "Total"]
        col_widths = [20, 30, 15, 15]
    else:
        headers = ["Date", "Medicine Name", "Quantity", "Selling Price", "Total", "Action"]
        col_widths = [20, 30, 15, 15, 15, 15]

    # Create a string buffer for formatted data
    formatted = "\t".join(headers) + "\n"

    for row in data:
        # Ensure row length matches col_widths length
        if len(row) > len(col_widths):
            row = row[:len(col_widths)]
        formatted += "\t".join(f"{cell:<{col_widths[i]}}" for i, cell in enumerate(row)) + "\n"
    
    return formatted


def main():
    root = tk.Tk()
    root.title("Pharmacy Management System")

    # Create the main content frame
    main_frame = tk.Frame(root, bg="#f7f7f7", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    create_header(root)

    # Create table and form
    table_frame = create_table(main_frame)
    entries, form_container = create_form(main_frame, table_frame)

    root.mainloop()

if __name__ == "__main__":
    main()