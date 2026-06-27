# Advanced ASCII Security Pipeline

A real-time video streaming application that converts live webcam feeds into stylized ASCII art matrix displays.

## 🚀 Features
* **Live Webcam Capture**: Streams real-time video using Python.
* **FastAPI Backend**: Uses high-performance WebSockets via Uvicorn for ultra-low latency data transfer.
* **Interactive Frontend**: Clean HTML5/CSS3 matrix interface with selectable style profiles.

## 🛠️ Tech Stack
* **Backend**: Python, FastAPI, Uvicorn, OpenCV
* **Frontend**: HTML5, CSS3, JavaScript (WebSockets)

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com
   cd ascii-video-pipeline
   ```

2. **Install required dependencies**:
   ```bash
   pip install fastapi uvicorn opencv-python
   ```

3. **Run the server**:
   ```bash
   python server.py
   ```

4. **Open the application**:
   Open `index.html` directly in your browser to view the live stream.
