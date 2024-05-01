from rich import print

import cv2

class Colors:
    colors = {
        "blue": (0, 0, 255),
        "green": (0, 255, 0),
        "orange": (255, 165, 0),
        "red": (255, 0, 0),
        "white": (255, 255, 255),
        "yellow": (255, 255, 0)
    }

    colorsName = {
        (0, 0, 255): 'B',
        (0, 255, 0): 'G',
        (255, 165, 0): 'O',
        (255, 0, 0): 'R',
        (255, 255, 255): 'W',
        (255, 255, 0): 'Y'
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

    def getColorName(self, c):
        return self.colorsName[c]


class Camera:
    isRunning = True
    wantClose = False;
    distance = 24
    gallery = []

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
        faces = ["White", "Orange", "Green", "Red", "Blue", "Yellow"]
        tmp = "All faces captured"
        if len(self.gallery) < 6:
            tmp = f"Press space to capture {faces[len(self.gallery)]} face"
        cv2.putText(frame, tmp, (0, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    def start(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            self.draw(frame)
            if not ret:
                print("Error: Could not capture frame.")
                break
            cv2.imshow('Camera', frame)
            key = cv2.waitKey(30)
            self.event_handler(key)
        cv2.destroyAllWindows()

    def event_handler(self, key):
        if key == 27 or key == ord('q'):
            if self.wantClose:
                self.isRunning = False
                print("Closing...")
            else:
                if len(self.gallery) >= 6:
                    self.isRunning = False
                    print("Closing...")
                else:
                    print(f"Are you sure u want to close ? You need {6 - len(self.gallery)} pictures to complete the cube...")
                    self.wantClose = True
        if key == ord(' '):
            if (len(self.gallery) >= 6):
                print("You have all your faces in the gallery")
            else:
                print("Capturing...")
                self.capture()
                self.flashEffect = 10
            self.wantClose = False
        if key == 82:
            print("Zooming in...")
            self.distance += 1
            self.wantClose = False
        if key == 84:
            print("Zooming out...")
            self.distance -= 1
            self.wantClose = False
        if key == ord('r'):
            print("Refreshing...")
            self.distance = 24
            self.wantClose = False

    def getCube(self):
        if (len(self.gallery) < 6):
            raise ValueError("You don't have the 6 faces in the gallery")
        color = Colors()
        cube = []
        for img in self.gallery:
            cube.append([
                [color.getColorName(color.getNearColor(img[i])) for i in range(0, 3)],
                [color.getColorName(color.getNearColor(img[i])) for i in range(3, 6)],
                [color.getColorName(color.getNearColor(img[i])) for i in range(6, 9)]
            ])
        return cube
