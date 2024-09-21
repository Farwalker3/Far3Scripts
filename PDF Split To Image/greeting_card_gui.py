import subprocess
import sys

# Function to check and install required packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = ["tkinter", "pdf2image", "Pillow", "trimesh", "numpy"]

# Check for each package and install if not present
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        install(package)

import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import os

class PDFTo3DCardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to 3D Card Converter")

        self.upload_button = tk.Button(root, text="Upload PDF(s)", command=self.upload_files)
        self.upload_button.pack(pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

        self.saved_images = []

    def upload_files(self):
        file_paths = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF files", "*.pdf")])
        if not file_paths:
            return

        for file_path in file_paths:
            self.process_pdf(file_path)

    def process_pdf(self, pdf_path):
        try:
            filename = os.path.splitext(os.path.basename(pdf_path))[0]
            front_image_path, back_image_path = self.convert_and_split_pdf(pdf_path, filename)

            # Uncomment the following line to create the 3D card model
            # model_path = self.create_3d_card(front_image_path, back_image_path)

            self.result_label.config(text=f"Processed: {filename}\n"
                                           f"Front: {front_image_path}\n"
                                           f"Back: {back_image_path}\n"
                                           # f"Model: {model_path}"
                                           )

            self.saved_images.append((front_image_path, back_image_path))  # Update this line if uncommenting model path

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def convert_and_split_pdf(self, pdf_path, filename):
        pages = convert_from_path(pdf_path, dpi=300)
        temp_folder = "outputs"
        os.makedirs(temp_folder, exist_ok=True)

        front_image_path = os.path.join(temp_folder, f'{filename}_front.jpg')
        back_image_path = os.path.join(temp_folder, f'{filename}_back.jpg')

        pages[0].save(front_image_path, 'JPEG')
        img = Image.open(front_image_path)
        width, height = img.size

        left_side = img.crop((0, 0, width // 2, height))
        right_side = img.crop((width // 2, 0, width, height))
        left_side.save(back_image_path)  # Back side
        right_side.save(front_image_path)  # Front side

        return front_image_path, back_image_path

    def create_3d_card(self, front_image_path, back_image_path):
        front_image = Image.open(front_image_path)
        back_image = Image.open(back_image_path)

        front_image = np.array(front_image) / 255.0
        back_image = np.array(back_image) / 255.0

        # Texture and mesh creation code commented out for now
        """
        front_texture = trimesh.visual.texture.SimpleMaterial(image=front_image)
        back_texture = trimesh.visual.texture.SimpleMaterial(image=back_image)

        front_mesh = trimesh.creation.box(extents=(2, 0.01, 3), visual=front_texture)
        back_mesh = trimesh.creation.box(extents=(2, 0.01, 3), visual=back_texture)
        back_mesh.apply_translation([0, -0.01, 0])

        combined_mesh = trimesh.util.concatenate([front_mesh, back_mesh])
        model_path = os.path.join("outputs", f'{filename}_card_model.glb')
        combined_mesh.export(model_path)
        """

if __name__ == '__main__':
    root = tk.Tk()
    app = PDFTo3DCardApp(root)
    root.geometry("400x300")
    root.mainloop()