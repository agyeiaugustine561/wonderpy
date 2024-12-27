import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os
import fitz  # PyMuPDF for PDF files
import docx  # For Word files

# List to store file paths and their corresponding image previews
file_data = []

# Function to upload a file
def upload_file():
    filetypes = [
        ("Image Files", "*.png;*.jpg;*.jpeg"),
        ("PDF Files", "*.pdf"),
        ("Word Files", "*.docx;*.doc"),
    ]
    file_path = filedialog.askopenfilename(filetypes=filetypes)
    
    if file_path:
        file_name = os.path.basename(file_path)
        preview_image = generate_preview(file_path)
        file_data.append((file_path, preview_image))
        table.insert("", "end", values=(file_name,), image=preview_image)
        message_label.config(text=f"File '{file_name}' added to the table.")

# Function to generate a preview image for a file
def generate_preview(file_path):
    file_ext = os.path.splitext(file_path)[1].lower()
    preview_img = None
    
    if file_ext in [".png", ".jpg", ".jpeg"]:
        img = Image.open(file_path)
        img.thumbnail((100, 100))  # Resize for preview
        preview_img = ImageTk.PhotoImage(img)
    
    elif file_ext == ".pdf":
        doc = fitz.open(file_path)
        first_page = doc.load_page(0)
        pix = first_page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.thumbnail((100, 100))
        preview_img = ImageTk.PhotoImage(img)
    
    return preview_img

# Function to submit the form along with the uploaded file
def submit_form():
    name = name_entry.get()
    age = age_entry.get()
    
    if not name or not age:
        message_label.config(text="Please enter both Name and Age.")
        return
    
    if not file_data:
        message_label.config(text="Please upload a file.")
        return
    
    # Example: Display submitted information in the message label
    file_name = file_data[0][0]  # Take the first file for demonstration
    message_label.config(text=f"Submitted: Name: {name}, Age: {age}, File: {file_name}")

# Function to open a file when clicked
def open_selected_file(event):
    selected_item = table.selection()
    if selected_item:
        item_index = table.index(selected_item[0])
        file_path = file_data[item_index][0]
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in [".png", ".jpg", ".jpeg"]:
            open_image(file_path)
        elif file_ext == ".pdf":
            open_pdf(file_path)
        elif file_ext in [".docx", ".doc"]:
            open_word(file_path)

# Function to open and display an image
def open_image(file_path):
    img = Image.open(file_path)
    img = img.resize((300, 300), Image.LANCZOS)  # Resize for display
    img_tk = ImageTk.PhotoImage(img)
    
    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference to avoid garbage collection
    text_box.delete(1.0, tk.END)

# Function to open and display a PDF file
def open_pdf(file_path):
    doc = fitz.open(file_path)
    first_page = doc.load_page(0)
    pix = first_page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img = img.resize((300, 300), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    
    image_label.config(image=img_tk)
    image_label.image = img_tk
    text_box.delete(1.0, tk.END)

# Function to open and display a Word document
def open_word(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, text)
    image_label.config(image="")

# Tkinter main window setup
root = tk.Tk()
root.title("File Upload and View")
root.geometry("800x600")

# Entry fields for Name and Age
name_label = tk.Label(root, text="Name:")
name_label.pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

age_label = tk.Label(root, text="Age:")
age_label.pack(pady=5)
age_entry = tk.Entry(root)
age_entry.pack(pady=5)

# Button to upload file
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack(pady=20)

# Button to submit the form
submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.pack(pady=10)

# Message label
message_label = tk.Label(root, text="")
message_label.pack(pady=5)

# Data table setup using Treeview widget
columns = ("Thumbnail", "File Name")
table = ttk.Treeview(root, columns=columns, show="headings", height=6)
table.heading("File Name", text="File Name")

# Add an explicit column for thumbnails
table.column("Thumbnail", width=100, anchor="center")
table.heading("Thumbnail", text="Preview")

# Set the column width for File Name
table.column("File Name", width=200)

table.pack(pady=10)

# Add scrollbar to the table
scrollbar = ttk.Scrollbar(root, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Bind the click event to open the selected file
table.bind("<Double-1>", open_selected_file)

# Label to display images
image_label = tk.Label(root)
image_label.pack(pady=10)

# Text box to display Word document text
text_box = tk.Text(root, height=10, width=50)
text_box.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
