import cv2
import numpy as np
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Browser connected!")
    
    camera = cv2.VideoCapture(0)
    prev_frame = None  # Used to store the last frame for motion detection
    current_theme = "matrix"  # Default theme
    
    try:
        while True:
            # 1. Listen for any messages from the webpage (like a theme change request)
            try:
                # We check for new messages without blocking our video loop
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.001)
                if data.startswith("THEME:"):
                    current_theme = data.split(":")[1]
                    print(f"Theme changed to: {current_theme}")
            except asyncio.TimeoutError:
                pass  # No new theme message, continue streaming video

            success, frame = camera.read()
            if not success:
                break
                
            # 2. CORE MOTION DETECTION ALGORITHM
            # Convert frame to grayscale and blur it slightly to remove camera noise
            gray_motion = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_motion = cv2.GaussianBlur(gray_motion, (21, 21), 0)
            
            motion_detected = "false"
            if prev_frame is not None:
                # Calculate absolute difference between current frame and previous frame
                frame_delta = cv2.absdiff(prev_frame, gray_motion)
                # If a pixel changed by more than 25 brightness levels, flag it
                thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
                # If more than 2% of the pixels changed, movement happened!
                if np.sum(thresh == 255) > (thresh.size * 0.02):
                    motion_detected = "true"
            
            prev_frame = gray_motion  # Update our baseline for the next frame
            
            # 3. ASCII MATRIX CONVERSIONS
            small_frame = cv2.resize(frame, (100, 50))
            gray_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            pixel_indices = (gray_frame / 255 * (len(ASCII_CHARS) - 1)).astype(int)
            
            ascii_lines = []
            for row in pixel_indices:
                line = "".join([ASCII_CHARS[value] for value in row])
                ascii_lines.append(line)
                
            full_ascii_text = "\n".join(ascii_lines)
            
            # 4. PACKET PACKAGING
            # We send a single string separated by '|' characters containing:
            # Motion Status | Selected Theme | Raw ASCII Text Art
            payload = f"{motion_detected}|{current_theme}|{full_ascii_text}"
            
            await websocket.send_text(payload)
            await asyncio.sleep(0.033)
            
    except Exception as e:
        print(f"Connection closed: {e}")
    finally:
        camera.release()
        print("Server parked cleanly.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
