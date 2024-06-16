import base64
import threading
from time import sleep, time

import cv2
import flet as ft


def get_available_cameras(max_devices=10):
    available_devices = []
    for i in range(max_devices):
        cap = cv2.VideoCapture(i)
        if cap is None or not cap.isOpened():
            print('警告: ビデオソースを開けません: ', i)
        else:
            print('成功: ビデオソースを見つけました: ', i)
            available_devices.append(i)
        cap.release()
    return available_devices

class CameraCaptureControl(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.capture = cv2.VideoCapture(1)
        self.latency = 1 / self.capture.get(cv2.CAP_PROP_FPS)
        self.fps = 0
        self.last_time = time()

    def did_mount(self):
        self.running = True
        self.thread = threading.Thread(target=self.update_frame, args=(), daemon=True)
        self.thread.start()

    def will_unmount(self):
        self.running = False

    def update_frame(self):
        frame_count = 0
        while self.capture.isOpened() and self.running:
            retval, frame = self.capture.read()
            if not retval:
                continue
            retval, frame = cv2.imencode(".png", frame)
            data = base64.b64encode(frame)
            self.image_control.src_base64 = data.decode()
            
            # Calculate FPS
            frame_count += 1
            current_time = time()
            if current_time - self.last_time >= 1.0:
                self.fps = frame_count
                frame_count = 0
                self.last_time = current_time
            
            # Update FPS display
            self.fps_text.value = f"FPS: {self.fps}"
            self.update()
            
            sleep(self.latency)

    def build(self):
        self.image_control = ft.Image(
            width=self.capture.get(cv2.CAP_PROP_FRAME_WIDTH),
            height=self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT),
            fit=ft.ImageFit.FIT_WIDTH,
        )
        self.fps_text = ft.Text(value="FPS: 0")
        return ft.Column([self.image_control, self.fps_text])

def main(page: ft.Page):
    page.add(CameraCaptureControl())

ft.app(target=main)
