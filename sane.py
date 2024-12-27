import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
from PIL import Image, ImageDraw

def print_sales_data(table_frame):
    """Function to print sales data and provide options for saving as PDF or image."""
    sales_data = []
    for row in range(2, len(table_frame.grid_slaves()) // 6 + 2):  # Skip header row
        row_data = []
        for col in range(6):
            widget = table_frame.grid_slaves(row=row, column=col)
            if widget:
                row_data.append(widget[0].cget("text"))
        sales_data.append(row_data)

    # Ask the user where to save the file and what format they prefer
    file_types = [("PDF Files", "*.pdf"), ("Image Files", "*.png")]
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=file_types)
    
    if file_path.endswith(".pdf"):
        save_as_pdf(sales_data, file_path)
    elif file_path.endswith(".png"):
        save_as_image(sales_data, file_path)

def save_as_pdf(data, file_path):
    """Save the sales data as a PDF."""
    pdf = pdf_canvas(file_path, pagesize=letter)
    width, height = letter

    # Set initial position on the PDF page
    x_offset, y_offset = 50, height - 50
    line_height = 20

    # Write the table headers
    headers = ["Date", "Medicine Name", "Quantity", "Selling Price", "Total", "Action"]
    pdf.setFont("Helvetica-Bold", 12)
    for col_num, header in enumerate(headers):
        pdf.drawString(x_offset + col_num * 100, y_offset, header)

    # Write the sales data
    y_offset -= line_height
    pdf.setFont("Helvetica", 10)
    for row in data:
        for col_num, cell in enumerate(row):
            pdf.drawString(x_offset + col_num * 100, y_offset, cell)
        y_offset -= line_height

    # Save the PDF file
    pdf.save()
    messagebox.showinfo("Success", f"Sales data saved as PDF: {file_path}")

def save_as_image(data, file_path):
    """Save the sales data as an image."""
    # Define image size and settings
    img_width = 800
    row_height = 30
    img_height = row_height * (len(data) + 1)  # Add 1 for headers

    # Create a blank image
    img = Image.new('RGB', (img_width, img_height), color='white')
    d = ImageDraw.Draw(img)

    # Define font sizes
    font_color = (0, 0, 0)
    headers = ["Date", "Medicine Name", "Quantity", "Selling Price", "Total", "Action"]

    # Draw headers
    for col_num, header in enumerate(headers):
        d.text((col_num * 130 + 20, 0), header, fill=font_color)

    # Draw table data
    for row_num, row in enumerate(data):
        y_position = (row_num + 1) * row_height
        for col_num, cell in enumerate(row):
            d.text((col_num * 130 + 20, y_position), cell, fill=font_color)

    # Save the image
    img.save(file_path)
    messagebox.showinfo("Success", f"Sales data saved as image: {file_path}")

def create_header(root):
    """Create the header section."""
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

def create_table(parent_frame):
    """Create a sample table with headers for displaying sales data."""
    table_frame = tk.Frame(parent_frame, bg="white")
    table_frame.pack(fill=tk.BOTH, expand=True)

    headers = ["Date", "Medicine Name", "Quantity", "Selling Price", "Total", "Action"]

    for col_num, header in enumerate(headers):
        label = tk.Label(table_frame, text=header, bg="gray", fg="white", padx=5, pady=5)
        label.grid(row=0, column=col_num, sticky="nsew")

    return table_frame

def create_form(parent_frame, table_frame):
    """Create a form for adding sales data."""
    form_frame = tk.Frame(parent_frame, bg="white")
    form_frame.pack(fill=tk.BOTH, pady=10)

    fields = ["Date", "Medicine Name", "Quantity", "Selling Price", "Total"]
    entries = {}

    for i, field in enumerate(fields):
        label = tk.Label(form_frame, text=field, padx=5, pady=5)
        label.grid(row=0, column=i, sticky="e")

        entry = tk.Entry(form_frame)
        entry.grid(row=1, column=i)
        entries[field] = entry

    add_button = tk.Button(form_frame, text="Add Sale", command=lambda: add_sale(entries, table_frame))
    add_button.grid(row=1, column=len(fields))

    return entries, form_frame

def add_sale(entries, table_frame):
    """Add sale entry to the table."""
    row = len(table_frame.grid_slaves()) // 6 + 1
    for col_num, field in enumerate(entries.keys()):
        value = entries[field].get()
        label = tk.Label(table_frame, text=value, padx=5, pady=5)
        label.grid(row=row, column=col_num)

    action_button = tk.Button(table_frame, text="Delete", command=lambda: delete_row(table_frame, row))
    action_button.grid(row=row, column=len(entries))

def delete_row(table_frame, row):
    """Delete a specific row from the table."""
    for widget in table_frame.grid_slaves(row=row):
        widget.destroy()

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

    # Create the Print Button
    print_button = tk.Button(main_frame, text="Print Sales Data", command=lambda: print_sales_data(table_frame))
    print_button.pack(pady=10)  # Place it below the table and form

    root.mainloop()


if __name__ == "__main__":
    main()
