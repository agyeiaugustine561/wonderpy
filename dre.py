import tkinter as tk
from tkinter import messagebox

def medicine_sales_page(parent):
    form_frame = tk.Frame(parent, padx=320, pady=40, bg="white")
    form_frame.grid(row=0, column=0, sticky=tk.W+tk.E)
    table_frame = create_table(parent)
    
    form_title = tk.Label(form_frame, text="Medicine Sales", font=("Arial", 16))
    form_title.grid(row=0, column=0, columnspan=4, pady=5)

    # Creating entries for all fields
    entries = {}
    entries['medicine_name'] = create_form_entry(form_frame, "Medicine Name", 1, 0)
    entries['generic'] = create_form_entry(form_frame, "Generic", 1, 1)
    entries['presentation'] = create_form_entry(form_frame, "Presentation", 1, 2)
    
    entries['supplier_company'] = create_form_entry(form_frame, "Supplier Company", 2, 0)
    entries['total_quantity'] = create_form_entry(form_frame, "Total Quantity", 2, 1, entry_type="number")
    entries['unit_price'] = create_form_entry(form_frame, "Unit Price", 2, 2, entry_type="number")
    
    entries['total_amount'] = create_form_entry(form_frame, "Total Amount", 3, 0, entry_type="number", readonly=True)
    entries['selling_price'] = create_form_entry(form_frame, "Selling Price", 3, 1, entry_type="number")
    entries['volume'] = create_form_entry(form_frame, "Volume", 3, 2, entry_type="text")
    
    entries['purchase_paid'] = create_form_entry(form_frame, "Purchase Paid", 4, 0, entry_type="number")
    entries['purchase_due'] = create_form_entry(form_frame, "Purchase Due", 4, 1, entry_type="number")
    entries['expire_date'] = create_form_entry(form_frame, "Expire Date", 4, 2)

    add_button = tk.Button(form_frame, text="ADD", bg="#5cb85c", fg="white", command=lambda: add_medicine(entries, table_frame), width=5)
    add_button.grid(row=5, column=0, columnspan=3, pady=5)

    return entries, form_frame

def create_form_entry(form_frame, label_text, row, col, entry_type="text", readonly=False):
    label = tk.Label(form_frame, text=label_text, bg="white")
    label.grid(row=row, column=col*2, pady=5, sticky=tk.W, padx=5)

    if entry_type == "text":
        entry = tk.Entry(form_frame)
    elif entry_type == "number":
        entry = tk.Entry(form_frame)
    elif entry_type == "dropdown":
        var = tk.StringVar()
        entry = tk.OptionMenu(form_frame, var, "-- Select --", "Option A", "Option B")
        entry.var = var
    else:
        entry = tk.Entry(form_frame)

    if readonly:
        entry.config(state="readonly")

    entry.grid(row=row, column=col*2+1, pady=5, sticky=tk.W+tk.E)
    return entry

def create_table(main_frame):
    canvas = tk.Canvas(main_frame, bg="white")
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scrollbar.set)

    table_frame = tk.Frame(canvas, bg="white", pady=20)
    canvas.create_window((0, 0), window=table_frame, anchor="nw")

    canvas.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
    scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S)

    table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    table_title = tk.Label(table_frame, text="Sales Medicine", font=("Arial", 16), bg="white")
    table_title.grid(row=0, column=0, columnspan=6, pady=10)

    headers = ["Medicine Name", "Generic", "Presentation", "Quantity", "Unit Price", "Total Amount", "Action"]
    for i, header in enumerate(headers):
        label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"), bg="#f7f7f7", padx=40, pady=5, borderwidth=1, relief="groove")
        label.grid(row=1, column=i, sticky=tk.W+tk.E)

    return table_frame

def add_medicine(entries, table_frame):
    medicine_name = entries['medicine_name'].get()
    generic = entries['generic'].get()
    presentation = entries['presentation'].get()
    quantity = entries['total_quantity'].get()
    unit_price = entries['unit_price'].get()

    if not medicine_name or not generic or not presentation or not quantity or not unit_price:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    total_amount = float(quantity) * float(unit_price)
    add_row(table_frame, medicine_name, generic, presentation, quantity, unit_price, total_amount)

    entries['medicine_name'].delete(0, tk.END)
    entries['generic'].delete(0, tk.END)
    entries['presentation'].delete(0, tk.END)
    entries['total_quantity'].delete(0, tk.END)
    entries['unit_price'].delete(0, tk.END)

    entries['medicine_name'].focus_set()

def add_row(table_frame, medicine_name, generic, presentation, quantity, unit_price, total_amount):
    row = len(table_frame.grid_slaves()) // 6 + 2
    entries = [medicine_name, generic, presentation, quantity, unit_price, f"{total_amount:.2f}"]

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

# Example Usage
root = tk.Tk()
root.title("Medicine Sales Page")
medicine_sales_page(root)
root.mainloop()
