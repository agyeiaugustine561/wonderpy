import tkinter as tk
from tkinter import ttk, messagebox

# Procedural functions for UI components
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    canvas.create_oval(x1, y1, x1 + 2 * radius, y1 + 2 * radius, fill=kwargs.get('fill', 'white'), outline='')
    canvas.create_oval(x2 - 2 * radius, y1, x2, y1 + 2 * radius, fill=kwargs.get('fill', 'white'), outline='')
    canvas.create_oval(x1, y2 - 2 * radius, x1 + 2 * radius, y2, fill=kwargs.get('fill', 'white'), outline='')
    canvas.create_oval(x2 - 2 * radius, y2 - 2 * radius, x2, y2, fill=kwargs.get('fill', 'white'), outline='')
    canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=kwargs.get('fill', 'white'), outline='')
    canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=kwargs.get('fill', 'white'), outline='')

def create_dashboard_box(canvas, x, y, width, height, bg_color, content):
    create_rounded_rectangle(canvas, x, y, x + width, y + height, radius=20, fill=bg_color)
    canvas.create_text(x + width / 2, y + height / 2, text=content, font=("Arial", 14, 'bold'))
    
    
    
    

def create_table(root):
    table_frame = tk.Frame(root, padx=10, pady=10)
    table_frame.pack(fill=tk.BOTH, expand=True)

    headers = ["Date", "Medicine Name", "Quantity", "Selling Price", "Total Amount", "Edit", "Delete"]
    for col, header in enumerate(headers):
        label = tk.Label(table_frame, text=header, padx=10, pady=5, borderwidth=2, relief="groove")
        label.grid(row=0, column=col, sticky=tk.W + tk.E)

    return table_frame






def create_form(root, table_frame):
    form_frame = tk.Frame(root, padx=20, pady=20)
    form_frame.pack(fill=tk.BOTH, expand=True)

    form_title = tk.Label(form_frame, text="Sales Medicine", font=("Arial", 16))
    form_title.grid(row=0, column=0, columnspan=2, pady=10)

    entries = {}
    entries['date'] = create_form_entry(form_frame, "Date", 1)
    entries['customer_mail'] = create_form_entry(form_frame, "Customer Mail", 2, entry_type="email")
    entries['medicine_name'] = create_form_entry(form_frame, "Medicine Name", 3, entry_type="dropdown")
    entries['quantity'] = create_form_entry(form_frame, "Quantity", 4, entry_type="number")
    entries['selling_price'] = create_form_entry(form_frame, "Selling Price", 5)

    total_amount_label = tk.Label(form_frame, text="Total Amount")
    total_amount_label.grid(row=6, column=0, pady=10, sticky=tk.W)
    entries['total_amount'] = tk.Entry(form_frame, state="readonly")
    entries['total_amount'].grid(row=6, column=1, pady=10)

    add_button = tk.Button(form_frame, text="ADD", bg="#5cb85c", fg="white", command=lambda: add_medicine(entries, table_frame))
    add_button.grid(row=7, column=0, columnspan=2, pady=10)

    return form_frame

def create_form_entry(form_frame, label_text, row, entry_type="text"):
    label = tk.Label(form_frame, text=label_text)
    label.grid(row=row, column=0, pady=5, sticky=tk.W)

    if entry_type == "text":
        entry = tk.Entry(form_frame)
    elif entry_type == "email":
        entry = tk.Entry(form_frame)
    elif entry_type == "number":
        entry = tk.Entry(form_frame)
    elif entry_type == "dropdown":
        var = tk.StringVar()
        entry = tk.OptionMenu(form_frame, var, "-- Select --", "Medicine A", "Medicine B", "Medicine C")
        entry.var = var
    else:
        entry = tk.Entry(form_frame)

    entry.grid(row=row, column=1, pady=5, sticky=tk.W)
    return entry









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
    for entry in entries.values():
        if isinstance(entry, tk.Entry):
            entry.delete(0, tk.END)
        elif hasattr(entry, 'var'):
            entry.var.set("-- Select --")  # Reset dropdown

    # Reset focus to the first entry
    entries['date'].focus_set()

    # Update totals
    update_totals(table_frame)

def add_row(table_frame, date, medicine_name, quantity, selling_price, total_amount):
    row = len(table_frame.grid_slaves()) // 7 + 1
    entries = [date, medicine_name, quantity, selling_price, f"{total_amount:.2f}"]

    for i, entry in enumerate(entries):
        label = tk.Label(table_frame, text=entry, padx=10, pady=5, borderwidth=2, relief="groove")
        label.grid(row=row, column=i, sticky=tk.W + tk.E)

    add_action_buttons(table_frame, row)

def add_action_buttons(table_frame, row):
    edit_button = tk.Button(table_frame, text="Edit", command=lambda: edit_medicine(table_frame, row))
    edit_button.grid(row=row, column=6, padx=5)

    delete_button = tk.Button(table_frame, text="Delete", command=lambda: delete_medicine(table_frame, row))
    delete_button.grid(row=row, column=7, padx=5)

def edit_medicine(table_frame, row):
    # Implement edit functionality here
    pass

def delete_medicine(table_frame, row):
    for widget in table_frame.grid_slaves(row=row):
        widget.destroy()
    update_totals(table_frame)

def update_totals(table_frame):
    total = 0
    for row in table_frame.grid_slaves():
        if row.grid_info()['row'] > 0:
            total += float(row.grid_slaves(row=row.grid_info()['row'], column=4)[0].cget("text"))
    print(f"Total Sales Amount: {total:.2f}")

# Object-Oriented structure for the main application
class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("eSkooly Dashboard")
        self.root.geometry("1200x700")

        self.create_sidebar()
        self.create_header()
        self.show_dashboard()  # Default view

    def create_sidebar(self):
        self.sidebar_frame = tk.Frame(self.root, width=250, bg="#333", height=700, padx=10, pady=10)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        sidebar_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Students", self.show_students),
            ("Employees", self.show_employees),
            ("Revenue", self.show_revenue),
            ("Total Profit", self.show_total_profit),
            ("More", self.show_more),
            ("Table", self.show_table_page),
            ("Form", self.show_form_page)
        ]

        for text, command in sidebar_buttons:
            btn = tk.Button(self.sidebar_frame, text=text, command=command, width=20, bg="#444", fg="white", anchor='w')
            btn.pack(pady=5, fill=tk.X)

    def create_header(self):
        self.header_frame = tk.Frame(self.root, bg="#428bca", padx=10, pady=10)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(self.header_frame, text="Pharmacy Management System", bg="#428bca", fg="white", font=("Arial", 18))
        title_label.pack(side=tk.LEFT)

        nav_buttons = tk.Frame(self.header_frame, bg="#428bca")
        nav_buttons.pack(side=tk.LEFT, padx=20)

        table_button = tk.Button(nav_buttons, text="Show Table", bg="white", fg="black", command=self.show_table_page)
        table_button.pack(side=tk.LEFT, padx=5)

        form_button = tk.Button(nav_buttons, text="Show Form", bg="white", fg="black", command=self.show_form_page)
        form_button.pack(side=tk.LEFT, padx=5)

    def show_dashboard(self):
        self.clear_content()
        canvas = tk.Canvas(self.content_frame, bg="#f8f9fa")
        canvas.pack(fill=tk.BOTH, expand=True)

        create_dashboard_box(canvas, 50, 50, 250, 150, "#ff6b6b", "Total Sales")
        create_dashboard_box(canvas, 350, 50, 250, 150, "#5cb85c", "Total Revenue")
        create_dashboard_box(canvas, 50, 250, 250, 150, "#428bca", "Total Customers")
        create_dashboard_box(canvas, 350, 250, 250, 150, "#f0ad4e", "Total Expenses")

    def show_students(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Students Page").pack()

    def show_employees(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Employees Page").pack()

    def show_revenue(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Revenue Page").pack()

    def show_total_profit(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Total Profit Page").pack()

    def show_more(self):
        self.clear_content()
        tk.Label(self.content_frame, text="More Page").pack()
        
        

    def show_table_page(self):
        self.clear_content()
        create_table(self.content_frame)

    def show_form_page(self):
        self.clear_content()
        table_frame = create_table(self.content_frame)
        create_form(self.content_frame, table_frame)

    def clear_content(self):
        if hasattr(self, 'content_frame'):
            self.content_frame.destroy()
        self.content_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
