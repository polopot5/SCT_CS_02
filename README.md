Image Encryption & Decryption Tool (Python + Tkinter)
This project is a GUI-based image encryption and decryption tool built using Python, Tkinter, and NumPy. It allows users to apply various pixel-level transformations to encrypt and decrypt images using simple mathematical operations.
Features
- Interactive GUI built with Tkinter for ease of use
- Multiple encryption methods:
- xor: Bitwise XOR with a numeric key
- swap: Channel swapping (RGB → BGR)
- negate: Inverts pixel values
- add: Adds a numeric key to pixel values
- multiply: Multiplies pixel values by a factor
- Live preview of original and processed images
- Image upload and save functionality
- Encryption and decryption logic using reversible operations
Requirements
- Python 3.x
- Pillow (PIL)
- NumPy
