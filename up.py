import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os
import fitz  # PyMuPDF for PDF files
import docx  # For Word files

# List to store file paths for opening later
file_paths = []

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
        # Add file name and path to the table
        file_paths.append(file_path)
        table.insert("", "end", values=(file_name,))
        message_label.config(text=f"File '{file_name}' added to the table.")

# Function to open a file when clicked
def open_selected_file(event):
    selected_item = table.selection()
    if selected_item:
        item_index = table.index(selected_item[0])
        file_path = file_paths[item_index]
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
root.geometry("600x600")

# Button to upload file
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack(pady=20)

# Message label
message_label = tk.Label(root, text="")
message_label.pack(pady=5)

# Data table setup using Treeview widget
columns = ("File Name",)
table = ttk.Treeview(root, columns=columns, show="headings", height=6)
table.heading("File Name", text="File Name")
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
