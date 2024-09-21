# PDF Split To Image

This project provides a GUI application for converting PDF files into images.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Requirements
- Python 3.x
- Required packages: `tkinter`, `pdf2image`, `Pillow`, `trimesh`, `numpy`

## Installation
1. Clone this repository or download the code files.
2. Navigate to the project directory where `greeting_card_gui.py` is located:
   ```bash
   cd path/to/PDF Split To Image
   ```
3. Run the following command in your terminal to install the required packages:
   ```bash
   python3 greeting_card_gui.py
   ```
   The script will check for the required packages and install any missing ones automatically.

## Usage
1. Launch the application by running `greeting_card_gui.py`:
   ```bash
   python3 greeting_card_gui.py
   ```
2. Click the "Upload PDF(s)" button to select your PDF files.
3. The application will convert the first page of each selected PDF into front and back images, and display the paths of the processed images.
4. **Note:** The code for generating 3D models is currently commented out. You can uncomment the relevant sections in the script if you wish to enable this feature in the future.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the Unlicense license. See the [Unlicense](#unlicense) section for more details.

### Unlicense
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>