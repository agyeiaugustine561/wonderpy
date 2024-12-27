import tkinter as tk
from PIL import Image, ImageTk  # Ensure you have Pillow installed for image handling

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Sidebar and Content Page")
    root.geometry("800x600")

    # Create a frame for the sidebar
    sidebar_frame = tk.Frame(root, width=200, bg='lightgray', height=600, padx=10, pady=10)
    sidebar_frame.pack(side="left", fill="y")

    # Create a frame for the content area
    content_frame = tk.Frame(root, bg='white', width=600, height=600)
    content_frame.pack(side="right", fill="both", expand=True)

    # Add some content to the sidebar (e.g., buttons)
    tk.Button(sidebar_frame, text="Dashboard").pack(pady=5)
    tk.Button(sidebar_frame, text="Settings").pack(pady=5)
    tk.Button(sidebar_frame, text="Reports").pack(pady=5)
    tk.Button(sidebar_frame, text="Logout").pack(pady=5)

    # Load and display the image in the content area
    image_path = "C:/Users/MOREVIM/Downloads/16853535143078 (1).jpg"
    img = Image.open(image_path)
    img = img.resize((600, 100), Image.LANCZOS)  # Use LANCZOS for high-quality resizing
    img_tk = ImageTk.PhotoImage(img)

    image_label = tk.Label(content_frame, image=img_tk)
    image_label.image = img_tk  # Keep a reference to avoid garbage collection
    image_label.pack(pady=80, side=tk.RIGHT)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
