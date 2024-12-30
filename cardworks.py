#!/usr/bin/env python3

import os
import subprocess
import sys
import streamlit as st
from PIL import Image
from pdf2image import convert_from_path
import numpy as np

# Function to install missing libraries
def install_libraries():
	required_packages = ["pillow", "pdf2image", "numpy", "trimesh"]
	for package in required_packages:
		try:
			__import__(package)
		except ImportError:
			subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
			
# Image Processor Functionality
def process_images(folder_path, background_color=(71, 78, 90)):
	output_folder = os.path.join(folder_path, "output")
	os.makedirs(output_folder, exist_ok=True)
	
	for filename in os.listdir(folder_path):
		file_path = os.path.join(folder_path, filename)
		if filename.lower().endswith(('.png', '.webp', '.jpg', '.jpeg')):
			with Image.open(file_path) as img:
				max_dimension = max(img.size)
				square_img = Image.new('RGB', (max_dimension, max_dimension), background_color)
				img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)
				img_pos = ((max_dimension - img.width) // 2, (max_dimension - img.height) // 2)
				square_img.paste(img, img_pos, img if img.mode == 'RGBA' else None)
				output_path = os.path.join(output_folder, filename)
				square_img.save(output_path, quality=95)
	return output_folder

# PDF to 3D Card Functionality
def convert_and_split_pdf(pdf_path, filename):
	pages = convert_from_path(pdf_path, dpi=300)
	temp_folder = "outputs"
	os.makedirs(temp_folder, exist_ok=True)
	
	front_image_path = os.path.join(temp_folder, f'{filename}_front.jpg')
	back_image_path = os.path.join(temp_folder, f'{filename}_back.jpg')
	
	pages[0].save(front_image_path, 'JPEG')
	img = Image.open(front_image_path)
	width, height = img.size
	
	if width > height:
		left_side = img.crop((0, 0, width // 2, height))
		right_side = img.crop((width // 2, 0, width, height))
		left_side.save(back_image_path)
		right_side.save(front_image_path)
	else:
		top_side = img.crop((0, 0, width, height // 2))
		bottom_side = img.crop((0, height // 2, width, height))
		top_side.save(front_image_path)
		bottom_side.save(back_image_path)
		
	return front_image_path, back_image_path

# Streamlit UI
st.title("Unified Streamlit App")

# Section 1: Image Processor
st.header("Image Processor")
folder_path = st.text_input("Enter the path to the folder containing images:")
background_color = st.color_picker("Pick a background color:", "#474E5A")
if st.button("Process Images"):
	if folder_path:
		output_folder = process_images(folder_path, tuple(int(background_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)))
		st.success(f"Images processed successfully! Check the output folder: {output_folder}")
	else:
		st.error("Please provide a valid folder path.")
		
# Section 2: PDF to 3D Card
st.header("PDF to 3D Card Converter")
uploaded_files = st.file_uploader("Upload PDFs", accept_multiple_files=True, type=["pdf"])
if st.button("Convert PDFs"):
	if uploaded_files:
		for uploaded_file in uploaded_files:
			with open(uploaded_file.name, "wb") as f:
				f.write(uploaded_file.getbuffer())
			filename = os.path.splitext(uploaded_file.name)[0]
			front_image_path, back_image_path = convert_and_split_pdf(uploaded_file.name, filename)
			st.image(front_image_path, caption="Front Side")
			st.image(back_image_path, caption="Back Side")
	else:
		st.error("Please upload at least one PDF.")