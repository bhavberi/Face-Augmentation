import cv2 as cv
import os
from copy import copy
from enum import Enum
import numpy as np

class data_and_events:
    drawing_status = Enum("drawing_status", ["NONE", "DRAWING", "DONE", "FGBRUSH", "BGBRUSH"])

    def __init__(self, image_path) -> None:
        self.start_point = (-1, -1)
        self.end_point = (-1, -1)
        path = image_path
        img = cv.imread(path)
        self.drawing = self.drawing_status.NONE
        self.img = copy(img)
        self.img_copy = copy(img)
        self.mask = np.zeros(self.img_copy.shape[:2], dtype=np.uint8)
    
    def getbbox(self):
        return self.start_point, self.end_point

    def mouse_callback(self, event, x, y, flags, param) -> None:
        if self.drawing == self.drawing_status.DONE:
            return
        if event == cv.EVENT_LBUTTONDOWN:
            self.drawing = self.drawing_status.DRAWING
            self.start_point = (x, y)

        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing == self.drawing_status.DRAWING:
                self.img = copy(self.img_copy)
                cv.rectangle(self.img, self.start_point, (x, y), (0, 255, 0), 2)
        elif event == cv.EVENT_LBUTTONUP:
            self.drawing = self.drawing_status.NONE
            cv.rectangle(self.img, self.start_point, (x, y), (0, 255, 0), 2)
            self.end_point = (x, y)

    def line_mouse_callback(self, event, x, y, flags, param) -> None:
        if self.drawing == self.drawing_status.DONE:
            return
        if event == cv.EVENT_LBUTTONDOWN: #fg start
            self.drawing = self.drawing_status.FGBRUSH
            cv.circle(self.img, (x, y), 3, [255,255,255], -1)
            cv.circle(self.mask, (x, y), 3, 1, -1)

        elif event == cv.EVENT_RBUTTONDOWN:  # bg start
            self.drawing = self.drawing_status.BGBRUSH
            cv.circle(self.img, (x, y), 3, [255,0,0], -1)
            cv.circle(self.mask, (x, y), 3, 0, -1)

        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing == self.drawing_status.FGBRUSH:
                cv.circle(self.img, (x, y), 3, [255,255,255], -1)
                cv.circle(self.mask, (x, y), 3, 1, -1)
            elif self.drawing == self.drawing_status.BGBRUSH:
                cv.circle(self.img, (x, y), 3, [255,0,0], -1)
                cv.circle(self.mask, (x, y), 3, 0, -1)
        
        elif event == cv.EVENT_LBUTTONUP:
            self.drawing = self.drawing_status.NONE
            cv.circle(self.img, (x, y), 3, [255, 255, 255], -1)
            cv.circle(self.mask, (x, y), 3, 1, -1)
        elif event == cv.EVENT_RBUTTONUP:
            self.drawing = self.drawing_status.NONE
            cv.circle(self.img, (x, y), 3, [255, 0, 0], -1)
            cv.circle(self.mask, (x, y), 3, 0, -1)


    def get_image(self):
        return self.img
    def get_mask(self):
        return self.mask
    def keyboard_handler(self):
        key_press = cv.waitKey(1) & 0xFF
        if key_press == 27:  # esc key
            return -1
        elif key_press == ord("r"):  # reset image
            self.img = copy(self.img_copy)
            self.drawing = False
        elif key_press == 13:
            self.drawing = self.drawing_status.DONE
        return 0
