# Instructions for `background.py`

This Python script processes a folder of images (e.g., `.png`, `.webp`, `.jpg`, `.jpeg`) with transparent backgrounds, resizes them to fit inside a dynamically determined square dimension based on the largest dimension of each image, and adds a custom background color (`rgb(71, 78, 90)`). The processed images are saved in an output folder within the selected directory.

## Requirements

### 1. Python

Make sure Python 3.x is installed on your machine. You can download it from Python's official website (https://www.python.org/downloads/).

### 2. Dependencies

The script requires the following Python libraries:
- Pillow (used for image processing)
- tkinter (used for the graphical user interface)

If any of these libraries are missing, the script will attempt to install them automatically.

## How to Use

### Step 1: Download and Setup the Script
1. Download or copy the `background.py` script and place it in your desired directory.
   
### Step 2: Run the Script
1. Open a terminal (or command prompt) and navigate to the directory where the script is located.
2. Run the following command to start the script:

   python background.py

   Alternatively, if you're using Python 3:

   python3 background.py

### Step 3: Select a Folder
1. A graphical user interface (GUI) window will appear.
2. Click on the **Select Folder** button.
3. In the file dialog that appears, choose the folder that contains the images you want to process.

### Step 4: Processing
1. Once the folder is selected, the script will automatically process all images in that folder.
   - It will resize each image to fit inside a square that matches the image’s largest dimension.
   - The resized image will be centered on a square background with a color of `rgb(71, 78, 90)`.
   - All processed images will be saved in a new `output` folder created within the selected folder.
   
2. A message will appear when the processing is complete, indicating that the images have been saved.

### Step 5: View the Output
1. Navigate to the `output` folder inside the folder you selected earlier.
2. The processed images will be saved with the same filename as the original image, but with the new background applied.

## Customization

### Change Background Color
To change the background color, modify the following line in the script:

background_color = (71, 78, 90)  # Change this to your desired RGB values

### Adjust the Maximum Dimensions
The maximum dimensions of each image’s background square are automatically calculated based on the largest dimension of the image (height or width). You do not need to manually adjust this, but if you want a fixed square size, you can set a `new_size` value manually, like this:

new_size = (1000, 1000)  # Fixed square size

However, note that using a fixed size will ignore the dynamic sizing based on image dimensions.

## Troubleshooting

### 1. Pillow or tkinter is missing
- If the script detects that Pillow or tkinter is missing, it will attempt to install Pillow automatically. However, tkinter comes pre-installed with most Python distributions.
- If any library fails to install, please try installing it manually:
  
  pip install pillow

  If using Python 3:

  pip3 install pillow

### 2. GUI does not appear
If the GUI window does not appear, ensure that your Python installation includes tkinter. On some systems, tkinter is installed separately. For example, on Ubuntu you can install tkinter using:

sudo apt-get install python3-tk

### 3. Processing Speed
Processing may take time if there are many images or if the images are large. Be patient while the script completes.

## License

This script is open-source and free to use. You can modify it as needed for your own projects.