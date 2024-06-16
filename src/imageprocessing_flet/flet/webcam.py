import base64
import threading
from time import sleep

import cv2
import flet as ft


def get_available_cameras(max_devices = 10):
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

    def did_mount(self):
        self.running = True
        self.thread = threading.Thread(target=self.update_frame, args=(), daemon=True)
        self.thread.start()

    def will_unmount(self):
        self.running = False

    def update_frame(self):
        while self.capture.isOpened() and self.running:
            # TODO retvalのチェックとハンドリングを実装
            retval, frame = self.capture.read()
            retval, frame = cv2.imencode(".png", frame)
            data = base64.b64encode(frame)
            self.image_control.src_base64 = data.decode()
            self.update()
            sleep(self.latency)

    def build(self):
        self.image_control = ft.Image(
            width=self.capture.get(cv2.CAP_PROP_FRAME_WIDTH),
            height=self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT),
            fit=ft.ImageFit.FIT_WIDTH,
        )
        return self.image_control

def main(page: ft.Page):
    page.add(CameraCaptureControl())

ft.app(target=main)