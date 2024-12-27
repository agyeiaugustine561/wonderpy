import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os

# Function to open file dialog and select a file
def upload_file():
    # Open file dialog and select file
    filetypes = [("All Files", "*.*"), 
                 ("Image Files", "*.png;*.jpg;*.jpeg;*.gif"), 
                 ("PDF Files", "*.pdf"), 
                 ("Word Files", "*.docx;*.doc")]
    file_path = filedialog.askopenfilename(filetypes=filetypes)
    
    if file_path:
        file_name = os.path.basename(file_path)
        # Display file name in table
        add_to_table(file_name, file_path)

# Function to add file info to the data table
def add_to_table(file_name, file_path):
    table.insert("", "end", values=(file_name, file_path))
    messagebox.showinfo("Success", f"File '{file_name}' uploaded successfully!")

# Tkinter main window setup
root = tk.Tk()
root.title("File Upload to Data Table")
root.geometry("600x400")

# Button to upload file
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack(pady=20)

# Data table setup using Treeview widget
columns = ("File Name", "File Path")
table = ttk.Treeview(root, columns=columns, show="headings", height=8)
table.heading("File Name", text="File Name")
table.heading("File Path", text="File Path")

# Adding a scrollbar to the table
scrollbar = ttk.Scrollbar(root, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)

table.pack(pady=10)
scrollbar.pack(side="right", fill="y")

# Run the Tkinter event loop
root.mainloop()
