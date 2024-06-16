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


"""_summary_
class CameraCaptureControl(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.capture = cv2.VideoCapture(1)
        # 解像度を設定（低解像度に変更）
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.latency = 1 / self.capture.get(cv2.CAP_PROP_FPS)
        self.fps = 0
        self.last_time = time()

    def did_mount(self):
        self.running = True
        self.capture_thread = threading.Thread(target=self.capture_frames, args=(), daemon=True)
        self.encode_thread = threading.Thread(target=self.encode_frames, args=(), daemon=True)
        self.capture_thread.start()
        self.encode_thread.start()

    def will_unmount(self):
        self.running = False
        self.capture_thread.join()
        self.encode_thread.join()

    def capture_frames(self):
        while self.capture.isOpened() and self.running:
            retval, frame = self.capture.read()
            if retval:
                self.frame = frame
            sleep(self.latency / 10)  # 休止時間を短縮

    def encode_frames(self):
        frame_count = 0
        while self.running:
            if hasattr(self, 'frame'):
                # フレームごとにエンコードを行わないように設定
                if frame_count % 5 == 0:
                    retval, encoded_frame = cv2.imencode(".png", self.frame)
                    data = base64.b64encode(encoded_frame)
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

            sleep(self.latency / 10)  # 休止時間を短縮

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
"""

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
    def __init__(self, grayscale=False):
        super().__init__()
        self.capture = cv2.VideoCapture(1)  # Camera ID set to 0
        # 解像度を設定（低解像度に変更）
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.latency = 1 / self.capture.get(cv2.CAP_PROP_FPS)
        self.fps = 0
        self.last_time = time()
        self.grayscale = grayscale
        self.frame = None

    def did_mount(self):
        self.running = True
        self.capture_thread = threading.Thread(target=self.capture_frames, args=(), daemon=True)
        self.encode_thread = threading.Thread(target=self.encode_frames, args=(), daemon=True)
        self.capture_thread.start()
        self.encode_thread.start()

    def will_unmount(self):
        self.running = False
        self.capture_thread.join()
        self.encode_thread.join()

    def capture_frames(self):
        while self.capture.isOpened() and self.running:
            retval, frame = self.capture.read()
            if retval:
                self.frame = frame
            sleep(self.latency / 10)  # 休止時間を短縮

    def encode_frames(self):
        frame_count = 0
        while self.running:
            if self.frame is not None:
                # グレースケールに変換
                display_frame = self.to_grayscale(self.frame) if self.grayscale else self.frame
                # フレームごとにエンコードを行わないように設定
                if frame_count % 5 == 0:
                    retval, encoded_frame = cv2.imencode(".png", display_frame)
                    if retval:
                        data = base64.b64encode(encoded_frame)
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

            sleep(self.latency / 10)  # 休止時間を短縮

    def to_grayscale(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def build(self):
        self.image_control = ft.Image(
            width=self.capture.get(cv2.CAP_PROP_FRAME_WIDTH),
            height=self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT),
            fit=ft.ImageFit.FIT_WIDTH,
        )
        self.fps_text = ft.Text(value="FPS: 0")
        return ft.Column([self.image_control, self.fps_text])

def main(page: ft.Page):
    original_capture = CameraCaptureControl(grayscale=False)
    grayscale_capture = CameraCaptureControl(grayscale=True)
    
    page.add(ft.Column([
        original_capture,
        grayscale_capture,
    ]))

ft.app(target=main)


