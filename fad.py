import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect('management_system.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    amount REAL
)
''')
conn.commit()

# Function to insert a record into the database
def insert_record(name, amount):
    cursor.execute('INSERT INTO records (name, amount) VALUES (?, ?)', (name, amount))
    conn.commit()
    load_records()
    messagebox.showinfo("Success", "Record added successfully!")

# Function to load records from the database into the table
def load_records():
    cursor.execute('SELECT * FROM records')
    rows = cursor.fetchall()
    for row in table.get_children():
        table.delete(row)
    for row in rows:
        table.insert('', 'end', values=row)

# Function to handle the form submission
def submit_form():
    name = name_entry.get()
    amount = amount_entry.get()
    if name and amount:
        insert_record(name, float(amount))
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

# Tkinter main window
root = tk.Tk()
root.title("Management System with SQLite")
root.geometry("600x400")

# Input form
tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Amount").grid(row=1, column=0, padx=10, pady=10)
amount_entry = tk.Entry(root)
amount_entry.grid(row=1, column=1, padx=10, pady=10)

submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

# Data table
columns = ("ID", "Name", "Amount")
table = ttk.Treeview(root, columns=columns, show="headings", height=8)
table.heading("ID", text="ID")
table.heading("Name", text="Name")
table.heading("Amount", text="Amount")

table.grid(row=3, column=0, columnspan=2, pady=10)

# Load records when the app starts
load_records()

root.mainloop()

# Close database connection when the app is closed
conn.close()
