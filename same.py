import tkinter as tk
from tkinter import messagebox
import os
from PIL import ImageGrab

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

def create_table(main_frame):
    # Create a canvas for displaying the table
    canvas = tk.Canvas(main_frame, bg="white", width=600, height=400)
    canvas.pack(side=tk.LEFT, padx=20)

    # Table headers
    headers = ["Date", "Medicine Name", "Quantity", "Selling Price", "Total"]
    for i, header in enumerate(headers):
        canvas.create_text(100 + i * 100, 50, text=header, font=("Arial", 12, "bold"))

    # Draw empty cells (as an example)
    for row in range(5):
        for col in range(5):
            x0 = 50 + col * 100
            y0 = 80 + row * 40
            x1 = x0 + 100
            y1 = y0 + 40
            canvas.create_rectangle(x0, y0, x1, y1, outline="black")

    # Save reference to the canvas
    main_frame.canvas = canvas

def add_row_to_canvas(canvas, data):
    # Add a new row to the canvas table
    row = len(canvas.find_withtag("row"))  # Count how many rows are already on the canvas
    for col, value in enumerate(data):
        x0 = 50 + col * 100
        y0 = 80 + row * 40
        x1 = x0 + 100
        y1 = y0 + 40
        # Draw the new data row on the canvas
        canvas.create_rectangle(x0, y0, x1, y1, outline="black", tags="row")
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=value, tags="row")

def add_medicine(canvas):
    # Example data entry
    row_data = ["01/09/2024", "Medicine A", "10", "50", "500"]
    add_row_to_canvas(canvas, row_data)

def print_canvas(canvas):
    # Get the canvas bounding box
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    # Grab the canvas content and save it as an image
    ImageGrab.grab().crop((x, y, x1, y1)).save("canvas_print.png")

    # Print the image (on Windows, use 'startfile' with 'print' argument)
    if os.name == 'nt':
        os.startfile("canvas_print.png", "print")
    else:
        print("Use external tools to print the image for non-Windows systems")

def main():
    root = tk.Tk()
    root.title("Pharmacy Management System")

    # Create the main content frame
    main_frame = tk.Frame(root, bg="#f7f7f7", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    create_header(root)

    # Create table and form
    create_table(main_frame)

    # Add print button
    print_button = tk.Button(main_frame, text="Print Canvas", command=lambda: print_canvas(main_frame.canvas))
    print_button.pack(side=tk.RIGHT)

    # Add a medicine row
    add_button = tk.Button(main_frame, text="Add Row", command=lambda: add_medicine(main_frame.canvas))
    add_button.pack(side=tk.RIGHT)

    root.mainloop()

if __name__ == "__main__":
    main()
