import os
import subprocess
import sys
import streamlit as st
from pdf2image import convert_from_path
from PIL import Image
import numpy as np

# Function to check and install required packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = ["pdf2image", "Pillow", "trimesh", "numpy"]

# Check for each package and install if not present
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        st.write(f"Installing {package}...")
        install(package)

# Function to process the uploaded PDF and convert it to images
def process_pdf(pdf_file):
    try:
        # Convert the uploaded PDF to images
        filename = os.path.splitext(pdf_file.name)[0]
        front_image_path, back_image_path = convert_and_split_pdf(pdf_file, filename)

        # Optionally, you can uncomment this to create the 3D model
        # model_path = create_3d_card(front_image_path, back_image_path)

        # Display the processed images
        st.image(front_image_path, caption="Front Image", use_column_width=True)
        st.image(back_image_path, caption="Back Image", use_column_width=True)

        # Update result text
        st.success(f"Processed: {filename}\n"
                   f"Front: {front_image_path}\n"
                   f"Back: {back_image_path}\n"
                   # f"Model: {model_path}"
                   )

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to convert and split PDF into front and back images
def convert_and_split_pdf(pdf_file, filename):
    pages = convert_from_path(pdf_file, dpi=300)
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

# Function to create a 3D card (optional and commented out for now)
def create_3d_card(front_image_path, back_image_path):
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
    return "3D model created"  # Placeholder for the model creation

# Streamlit UI
st.title("PDF to 3D Card Converter")

st.header("Upload PDF File")
uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_pdf:
    process_pdf(uploaded_pdf)