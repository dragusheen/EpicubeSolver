#!/usr/bin/python3

from rich import print

from rich.live import Live
from rich.panel import Panel

import cv2

from PIL import Image


BOX = "■"

COLORS = {
    "BLUE":     "[purple3]",
    "GREEN":    "[green3]",
    "ORANGE":   "[dark_orange3]",
    "RED":      "[red3]",
    "WHITE":    "[white]",
    "YELLOW":   "[yellow2]",
    "RESET":    "[/]"
}

BOXES = {
    "BLUE": COLORS["BLUE"]      + BOX + COLORS["RESET"],
    "GREEN": COLORS["GREEN"]    + BOX + COLORS["RESET"],
    "ORANGE": COLORS["ORANGE"]  + BOX + COLORS["RESET"],
    "RED": COLORS["RED"]        + BOX + COLORS["RESET"],
    "WHITE": COLORS["WHITE"]    + BOX + COLORS["RESET"],
    "YELLOW": COLORS["YELLOW"]  + BOX + COLORS["RESET"]
}

DISPLAY_RC = [
    [['WHITE', 'WHITE', 'WHITE'],       ['WHITE', 'WHITE', 'WHITE'],        ['WHITE', 'WHITE', 'WHITE']],
    [['ORANGE', 'ORANGE', 'ORANGE'],    ['ORANGE', 'ORANGE', 'ORANGE'],     ['ORANGE', 'ORANGE', 'ORANGE']],
    [['GREEN', 'GREEN', 'GREEN'],       ['GREEN', 'GREEN', 'GREEN'],        ['GREEN', 'GREEN', 'GREEN']],
    [['RED', 'RED', 'RED'],             ['RED', 'RED', 'RED'],              ['RED', 'RED', 'RED']],
    [['BLUE', 'BLUE', 'BLUE'],          ['BLUE', 'BLUE', 'BLUE'],           ['BLUE', 'BLUE', 'BLUE']],
    [['YELLOW', 'YELLOW', 'YELLOW'],    ['YELLOW', 'YELLOW', 'YELLOW'],     ['YELLOW', 'YELLOW', 'YELLOW']]
]

class Camera:
    gallery = []
    distance = 24
    isOpen = True

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def capture(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not capture frame.")
            return
        height, width, _ = frame.shape
        height = height // 2
        width = width // 2
        color = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = width + (self.distance * 2 * j)
                y = height + (self.distance * 2 * i)
                b, g, r = frame[y, x]
                color.append((r, g, b))
        self.gallery.append(color)

    def draw_circle(self, frame, pos):
        radius = self.distance // 2
        cv2.circle(frame, pos, radius, (255, 0, 0), 2)

    def draw(self, frame):
        height, width, _ = frame.shape
        height = height // 2
        width = width // 2
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = width + (self.distance * 2 * i)
                y = height + (self.distance * 2 * j)
                self.draw_circle(frame, (x, y))

    def turn(self):
        ret, frame = self.cap.read()
        self.draw(frame)
        if not ret:
            print("Error: Could not capture frame.")
            self.isOpen = False
        cv2.imshow("Camera", frame)
        key = cv2.waitKey(30)
        self.event_handler(key)

    def live(self):
        while (self.isOpen):
            self.turn()

    def event_handler(self, key):
        if key == 27 or key == ord('q'):
            self.isOpen = False
            print("Closing...")
        if key == ord(' '):
            print("Capturing...")
            self.capture()
        if key == 82:
            print("Zooming in...")
            self.distance += 1
        if key == 84:
            print("Zooming out...")
            self.distance -= 1
        if key == ord('r'):
            print("Refreshing...")
            self.distance = 24

class Colors:
    colors = {
        "blue": (0, 0, 255),
        "green": (0, 255, 0),
        "orange": (255, 165, 0),
        "red": (255, 0, 0),
        "white": (255, 255, 255),
        "yellow": (255, 255, 0)
    }

    def __init__(self):
        pass

    def distance(self, c1, c2):
        r1, g1, b1 = c1
        r2, g2, b2 = c2
        return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5

    def getNearColor(self, c):
        r, g, b = c
        distances = []
        for color in self.colors.values():
            distances.append(self.distance(c, color))
        index = distances.index(min(distances))
        return list(self.colors.values())[index]



Cam = Camera()
Cam.live()
p = Panel("", border_style="green", title="Rubiks Cube", title_align="left", expand=False)
with Live(p, refresh_per_second=20):
    while Cam.isOpen:
        p.renderable = "{} {} {}\n{} {} {}\n{} {} {}".format(
            BOXES[DISPLAY_RC[0][0][0]], BOXES[DISPLAY_RC[0][0][1]], BOXES[DISPLAY_RC[0][0][2]],
            BOXES[DISPLAY_RC[0][1][0]], BOXES[DISPLAY_RC[0][1][1]], BOXES[DISPLAY_RC[0][1][2]],
            BOXES[DISPLAY_RC[0][2][0]], BOXES[DISPLAY_RC[0][2][1]], BOXES[DISPLAY_RC[0][2][2]],
        )
        Cam.capture()
        print(Cam.gallery())
# camColors = Cam.getColors()
# Color = Colors()
# for colors in camColors:
#     print("Colors:")
#     for color in colors:
#         print(f"{color}: {Color.getNearColor(color)}")
#     print()
