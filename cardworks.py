import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from pdf2image import convert_from_path, PDFInfoNotInstalledError

# Function to install missing libraries
def install_libraries():
    try:
        import pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "--quiet"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to install libraries: {e}")
        sys.exit()

# Try to import Pillow, install it if not found
try:
    from PIL import Image
except ImportError:
    install_libraries()
    from PIL import Image

# Function to handle the PDF to Image conversion
def convert_and_split_pdf(pdf_path, filename):
    try:
        pages = convert_from_path(pdf_path, dpi=300)
    except PDFInfoNotInstalledError:
        messagebox.showerror("Poppler Error", "Poppler is not installed. Please ensure Poppler is installed and in the system PATH.")
        sys.exit()

    temp_folder = "outputs"
    os.makedirs(temp_folder, exist_ok=True)

    front_image_path = os.path.join(temp_folder, f'{filename}_front.jpg')
    back_image_path = os.path.join(temp_folder, f'{filename}_back.jpg')

    pages[0].save(front_image_path, 'JPEG')
    img = Image.open(front_image_path)
    width, height = img.size

    # Detect whether the PDF is vertical or horizontal
    if width > height:
        # Horizontal PDF, split left and right
        left_side = img.crop((0, 0, width // 2, height))
        right_side = img.crop((width // 2, 0, width, height))
        left_side.save(back_image_path)  # Back side
        right_side.save(front_image_path)  # Front side
    else:
        # Vertical PDF, split top and bottom
        top_side = img.crop((0, 0, width, height // 2))
        bottom_side = img.crop((0, height // 2, width, height))
        top_side.save(front_image_path)  # Front side
        bottom_side.save(back_image_path)  # Back side

    return front_image_path, back_image_path

# Function to process the images in the selected folder
def process_images(folder_path):
    background_color = (71, 78, 90)  # RGB color for background

    # Create an output folder if it doesn't exist
    output_folder = os.path.join(folder_path, "output")
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Process image files only (ignoring other file types)
        if filename.lower().endswith(('.png', '.webp', '.jpg', '.jpeg')):
            with Image.open(file_path) as img:
                # Get the largest dimension (width or height) to determine the new square size
                max_dimension = max(img.size)  # The largest between width and height
                
                # Create a new square image with the background color based on the largest dimension
                square_img = Image.new('RGB', (max_dimension, max_dimension), background_color)

                # Preserve aspect ratio and resize the image to fit within the square
                img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)

                # Calculate position to center the image in the new square image
                img_pos = (
                    (max_dimension - img.width) // 2,
                    (max_dimension - img.height) // 2
                )

                # Paste the resized image onto the square background
                square_img.paste(img, img_pos, img if img.mode == 'RGBA' else None)

                # Save the result in the output folder with the same file name
                output_path = os.path.join(output_folder, filename)
                square_img.save(output_path, quality=95)  # Save with high quality

    messagebox.showinfo("Success", f"Processed images saved in '{output_folder}'.")

# Function to select the folder using the GUI
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        process_images(folder_path)

# Create the GUI window
def create_gui():
    root = tk.Tk()
    root.title("Image Processor")

    label = tk.Label(root, text="Select a folder with images:")
    label.pack(pady=10)

    select_button = tk.Button(root, text="Select Folder", command=select_folder)
    select_button.pack(pady=10)

    root.geometry("300x150")
    root.mainloop()

# Main entry point for the script
if __name__ == "__main__":
    create_gui()