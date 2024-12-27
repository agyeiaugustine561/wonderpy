import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import json
import os

# Sample data to be managed
data = [
    {"Name": "John Doe", "Age": 30, "Email": "john@example.com"},
    {"Name": "Jane Smith", "Age": 25, "Email": "jane@example.com"}
]

# Function to populate the Treeview with sample data
def populate_treeview():
    for item in treeview.get_children():
        treeview.delete(item)
    
    for entry in data:
        treeview.insert("", "end", values=(entry["Name"], entry["Age"], entry["Email"]))

# Function to export data to CSV
def export_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Export Successful", "Data exported to CSV successfully!")

# Function to export data to JSON
def export_json():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        messagebox.showinfo("Export Successful", "Data exported to JSON successfully!")

# Function to export data to Excel
def export_excel():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Export Successful", "Data exported to Excel successfully!")

# Function to import data from CSV
def import_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        global data
        data = df.to_dict(orient="records")
        populate_treeview()
        messagebox.showinfo("Import Successful", "Data imported from CSV successfully!")

# Function to import data from JSON
def import_json():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, 'r') as json_file:
            global data
            data = json.load(json_file)
        populate_treeview()
        messagebox.showinfo("Import Successful", "Data imported from JSON successfully!")

# Function to import data from Excel
def import_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        df = pd.read_excel(file_path)
        global data
        data = df.to_dict(orient="records")
        populate_treeview()
        messagebox.showinfo("Import Successful", "Data imported from Excel successfully!")

# Tkinter main window setup
root = tk.Tk()
root.title("Data Export/Import Example")
root.geometry("600x400")

# Treeview setup
columns = ("Name", "Age", "Email")
treeview = ttk.Treeview(root, columns=columns, show="headings")
treeview.heading("Name", text="Name")
treeview.heading("Age", text="Age")
treeview.heading("Email", text="Email")
treeview.pack(pady=20, fill=tk.BOTH, expand=True)

# Buttons for exporting and importing data
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Export to CSV", command=export_csv).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Export to JSON", command=export_json).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Export to Excel", command=export_excel).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Import from CSV", command=import_csv).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Import from JSON", command=import_json).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Import from Excel", command=import_excel).pack(side=tk.LEFT, padx=5)

# Initial population of Treeview
populate_treeview()

# Run the Tkinter event loop
root.mainloop()
