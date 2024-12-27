import tkinter as tk
from tkinter import ttk

# Function to handle submission
def submit_form():
    amount = spinbox.get()
    print(f"Amount submitted: ${amount}")

# Tkinter main window setup
root = tk.Tk()
root.title("Entry Form with Spinbox")
root.geometry("300x200")

# Create a frame for the form
form_frame = ttk.Frame(root, padding="10")
form_frame.pack(expand=True, fill="both")

# Label for the amount field
amount_label = ttk.Label(form_frame, text="Amount:")
amount_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Spinbox for amount entry
spinbox = tk.Spinbox(form_frame, from_=0, to=10000, increment=1, width=15)
spinbox.grid(row=0, column=1, padx=10, pady=10)

# Submit button
submit_button = ttk.Button(form_frame, text="Submit", command=submit_form)
submit_button.grid(row=1, columnspan=2, pady=20)

# Run the Tkinter event loop
root.mainloop()
