import os
import sys
import subprocess
import streamlit as st
from PIL import Image
import fitz  # PyMuPDF

# Function to install missing libraries
def install_libraries():
    try:
        import pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "PyMuPDF", "--quiet"])
    except Exception as e:
        st.error(f"Failed to install libraries: {e}")
        sys.exit()

# Try to import Pillow, install it if not found
try:
    from PIL import Image
except ImportError:
    install_libraries()
    from PIL import Image

# Function to handle the PDF to Image conversion using PyMuPDF (fitz)
def convert_and_split_pdf(pdf_path, filename):
    doc = fitz.open(pdf_path)

    # Get the first page
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=300)  # Get a pixmap of the page with 300 dpi

    # Create output directory
    temp_folder = "outputs"
    os.makedirs(temp_folder, exist_ok=True)

    front_image_path = os.path.join(temp_folder, f'{filename}_front.jpg')
    back_image_path = os.path.join(temp_folder, f'{filename}_back.jpg')

    # Save the image of the first page (front)
    pix.save(front_image_path)
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

# Streamlit file uploader and processing
def upload_pdf_and_process():
    st.title("PDF to 3D Card Converter")

    # Upload PDF file using Streamlit's file uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("uploaded.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        filename = os.path.splitext(uploaded_file.name)[0]
        try:
            front_image_path, back_image_path = convert_and_split_pdf("uploaded.pdf", filename)

            st.image(front_image_path, caption="Front of the Card", use_column_width=True)
            st.image(back_image_path, caption="Back of the Card", use_column_width=True)

            st.success(f"PDF processed successfully. Images saved as {front_image_path} and {back_image_path}")

        except Exception as e:
            st.error(f"Error: {e}")

# Main function to run the app
if __name__ == "__main__":
    upload_pdf_and_process()