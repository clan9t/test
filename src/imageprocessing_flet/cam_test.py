import flet as ft
import cv2
import threading
import numpy as np
import base64

def main(page: ft.Page):

    def update_frames():
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            # Original frame
            _, buffer = cv2.imencode('.jpg', frame)
            original_frame = base64.b64encode(buffer).decode()
            page.controls[0].src_base64 = f'{original_frame}'

            # Grayscale frame
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, buffer = cv2.imencode('.jpg', gray_frame)
            grayscale_frame = base64.b64encode(buffer).decode()
            page.controls[1].src_base64 = f'{grayscale_frame}'

            page.update()

    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open video device")
        return

    # Set video frame width and height
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Add two image controls to the page
    img1 = ft.Image(width=640, height=480)
    img2 = ft.Image(width=640, height=480)
    page.add(img1)
    page.add(img2)

    # Start a thread to update frames
    threading.Thread(target=update_frames, daemon=True).start()

    page.update()

ft.app(target=main)
