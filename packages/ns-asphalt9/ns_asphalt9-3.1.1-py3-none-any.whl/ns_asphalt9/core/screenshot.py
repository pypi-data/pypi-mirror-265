import cv2
from PIL import Image


def screenshot(resize=False):
    from . import globals

    frame = globals.frame_queue.tail()
    if resize:
        frame = cv2.resize(frame, (640, 360))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb_frame)
    return img


if __name__ == "__main__":
    screenshot()
