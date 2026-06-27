import cv2
import numpy as np
import os

# Open the webcam (0 means your computer's built-in main camera)
camera = cv2.VideoCapture(0)

# A list of characters ordered from darkest (dense) to lightest (thin)
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

print("Starting ASCII engine... Look at your terminal below!")

while True:
    # Read a single live frame from the webcam
    success, frame = camera.read()
    if not success:
        break
        
    # 1. Shrink the frame down so it fits perfectly inside your terminal screen
    # We make it 80 characters wide and 40 characters tall
    small_frame = cv2.resize(frame, (80, 40))
    
    # 2. Turn the image into black and white (Grayscale)
    # Now every pixel is just a single brightness number from 0 (black) to 255 (white)
    gray_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    
    # 3. Use NumPy magic to map those 0-255 numbers directly onto our ASCII characters list
    pixel_indices = (gray_frame / 255 * (len(ASCII_CHARS) - 1)).astype(int)
    
    # 4. Build the text rows
    ascii_lines = []
    for row in pixel_indices:
        # Convert the numbers back to characters and join them into a line
        line = "".join([ASCII_CHARS[value] for value in row])
        ascii_lines.append(line)
        
    # 5. Clear the old terminal screen text so the new frame draws cleanly on top
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # 6. Print the entire text image block
    print("\n".join(ascii_lines))

# Clean up code if it ever exits
camera.release()
