import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os

# Paths to icons
IMAGE_ICON_PATH = "icons/image_icon.png"
PDF_ICON_PATH = "icons/pdf_icon.png"
WORD_ICON_PATH = "icons/word_icon.png"

# Dictionary to map file extensions to their icons
file_icons = {
    ".png": IMAGE_ICON_PATH,
    ".jpg": IMAGE_ICON_PATH,
    ".jpeg": IMAGE_ICON_PATH,
    ".pdf": PDF_ICON_PATH,
    ".docx": WORD_ICON_PATH,
    ".doc": WORD_ICON_PATH
}

# List to store file paths for opening later
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
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Get the icon for the file type
        icon_path = file_icons.get(file_ext, None)
        if icon_path:
            icon_img = Image.open(icon_path)
            icon_img = icon_img.resize((50, 50), Image.LANCZOS)
            icon_tk = ImageTk.PhotoImage(icon_img)
        else:
            icon_tk = None
        
        # Add file path, file name, and icon to the table
        file_data.append((file_path, file_name))
        table.insert("", "end", values=(file_name,), image=icon_tk)
        
        # Keep a reference to the image to prevent garbage collection
        table.image = icon_tk
        message_label.config(text=f"File '{file_name}' added to the table.")

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
    import fitz  # PyMuPDF for PDF files
    
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
    import docx  # For Word files
    
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
columns = ("Thumbnail", "File Name")
table = ttk.Treeview(root, columns=columns, show="headings", height=6)
table.heading("File Name", text="File Name")

# Add an explicit column for thumbnails
table.column("Thumbnail", width=60, anchor="center")
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
