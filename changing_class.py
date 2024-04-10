from rich.panel import Panel
from rich import print

from enum import Enum
import random

class RubiksColor(Enum):
    UNDEFINED   = 0
    BLUE        = 1
    GREEN       = 2
    ORANGE      = 3
    RED         = 4
    WHITE       = 5
    YELLOW      = 6

BOX = "■"

COLORS = {
    RubiksColor.BLUE: "[purple3]",
    RubiksColor.GREEN: "[green3]",
    RubiksColor.ORANGE: "[dark_orange3]",
    RubiksColor.RED: "[red3]",
    RubiksColor.WHITE: "[white]",
    RubiksColor.YELLOW: "[yellow2]",
    RubiksColor.UNDEFINED: "[/]"
}

BOXES = {
    RubiksColor.BLUE: COLORS[RubiksColor.BLUE] + BOX + COLORS[RubiksColor.UNDEFINED],
    RubiksColor.GREEN: COLORS[RubiksColor.GREEN] + BOX + COLORS[RubiksColor.UNDEFINED],
    RubiksColor.ORANGE: COLORS[RubiksColor.ORANGE] + BOX + COLORS[RubiksColor.UNDEFINED],
    RubiksColor.RED: COLORS[RubiksColor.RED] + BOX + COLORS[RubiksColor.UNDEFINED],
    RubiksColor.WHITE: COLORS[RubiksColor.WHITE] + BOX + COLORS[RubiksColor.UNDEFINED],
    RubiksColor.YELLOW: COLORS[RubiksColor.YELLOW] + BOX + COLORS[RubiksColor.UNDEFINED]
}

class RubiksCase:
    def __init__(self, color: RubiksColor = RubiksColor.UNDEFINED) -> None:
        self.color = color
    
    def __str__(self) -> str:
        if self.color == RubiksColor.UNDEFINED:
            return "?"
        return BOXES[self.color]
    
    def __repr__(self) -> str:
        return str(self)

class RubiksFace:
    def __init__(self, *args) -> None:
        self.face = [
            [RubiksColor.UNDEFINED, RubiksColor.UNDEFINED, RubiksColor.UNDEFINED],
            [RubiksColor.UNDEFINED, RubiksColor.UNDEFINED, RubiksColor.UNDEFINED],
            [RubiksColor.UNDEFINED, RubiksColor.UNDEFINED, RubiksColor.UNDEFINED]
        ]
        if not len(args):
            return
        if len(args) == 1 and type(args[0]) == list:
            if type(args[0][0]) == list:
                for j in range(len(args[0])):
                    for i in range(len(args[0][j])):
                        self.face[j][i] = self.parse_arg(args[0][j][i])
            else:
                index = (0, 0)
                for i in range(len(args[0])):
                    self.face[index[0], index[1]] = self.parse_arg(args[0][i])
                    index[1] += 1
                    if index[1] >= len(self.face[index[0]]):
                        index[0] += 1
                        index[1] = 0
            return
        if len(args) == 3 and type(args[0]) == list:
            for j in range(len(args)):
                for i in range(len(args[j])):
                    self.face[j][i] = self.parse_arg(args[j][i])
            return
        if type(args[0]) in (int, RubiksColor, str):
            index = (0, 0)
            for i in range(len(args)):
                self.face[index[0], index[1]] = self.parse_arg(args[i])
                index[1] += 1
                if index[1] >= len(self.face[index[0]]):
                    index[0] += 1
                    index[1] = 0
            return
        raise ValueError(f"Could not use the provided argument as a RubiksFace: {type(args[0])}")

def rotate(self, clockwise = True):
    poses = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]
    if not clockwise:
        poses.reverse()

    for i in range(3):
        tmp = self.face[poses[-1][0]][poses[-1][1]]
        for i in range(len(poses)):
            tmp, self.face[poses[i][0]][poses[i][1]] = self.face[poses[i][0]][poses[i][1]], tmp


    def parse_arg(self, arg):
        if type(arg) == int:
            if arg in range(7):
                return list(RubiksColor)[arg]
            raise ValueError(f"Argument {arg} is undefined for type RubiksColor")
        if type(arg) == RubiksColor:
            return arg
        if type(arg) == str:
            return RubiksColor[arg]
        raise ValueError(f"Type {type(arg)} could not be used to cast a RubiksColor (supported types are 'int', 'RubiksColor' and 'str')")

    def __rich_repr__(self):
        return Panel(
            f"""{self.face[0][0]} {self.face[0][1]} {self.face[0][2]}
{self.face[1][0]} {self.face[1][1]} {self.face[1][2]}
{self.face[2][0]} {self.face[2][1]} {self.face[2][2]}""", border_style="green"
        )

    def __str__(self) -> str:
        return str(Panel(
            f"""{self.face[0][0]} {self.face[0][1]} {self.face[0][2]}
{self.face[1][0]} {self.face[1][1]} {self.face[1][2]}
{self.face[2][0]} {self.face[2][1]} {self.face[2][2]}""", border_style="green"
        ))
    
    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, item: int):
        return self.face[item]

class RubiksCube:
    def __init__(self):
        self.T = RubiksFace([RubiksColor.WHITE, RubiksColor.WHITE, RubiksColor.WHITE], [RubiksColor.WHITE, RubiksColor.WHITE, RubiksColor.WHITE], [RubiksColor.WHITE, RubiksColor.WHITE, RubiksColor.WHITE])
        self.L = RubiksFace([RubiksColor.ORANGE, RubiksColor.ORANGE, RubiksColor.ORANGE], [RubiksColor.ORANGE, RubiksColor.ORANGE, RubiksColor.ORANGE], [RubiksColor.ORANGE, RubiksColor.ORANGE, RubiksColor.ORANGE])
        self.F = RubiksFace([RubiksColor.GREEN, RubiksColor.GREEN, RubiksColor.GREEN], [RubiksColor.GREEN, RubiksColor.GREEN, RubiksColor.GREEN], [RubiksColor.GREEN, RubiksColor.GREEN, RubiksColor.GREEN])
        self.R = RubiksFace([RubiksColor.RED, RubiksColor.RED, RubiksColor.RED], [RubiksColor.RED, RubiksColor.RED, RubiksColor.RED], [RubiksColor.RED, RubiksColor.RED, RubiksColor.RED])
        self.B = RubiksFace([RubiksColor.BLUE, RubiksColor.BLUE, RubiksColor.BLUE], [RubiksColor.BLUE, RubiksColor.BLUE, RubiksColor.BLUE], [RubiksColor.BLUE, RubiksColor.BLUE, RubiksColor.BLUE])
        self.D = RubiksFace([RubiksColor.YELLOW, RubiksColor.YELLOW, RubiksColor.YELLOW], [RubiksColor.YELLOW, RubiksColor.YELLOW, RubiksColor.YELLOW], [RubiksColor.YELLOW, RubiksColor.YELLOW, RubiksColor.YELLOW])
    
    def __getitem__(self, item: str):
        if item.lower() in ("t", "top", "up"):
            return self.T
        if item.lower() in ("l", "left", "ouest", "west"):
            return self.L
        if item.lower() in ("f", "front"):
            return self.F
        if item.lower() in ("r", "right", "est"):
            return self.R
        if item.lower() in ("b", "back"):
            return self.B
        if item.lower() in ("d", "down"):
            return self.D
        raise ValueError(f"Could not interprete {item} as a face position !")

    def reset(self):
        self.__init__()

    def rotate_face(self, index):
        new_face = [['', '', ''], ['', '', ''], ['', '', '']]
        face = self.cube[index]
        for row in range(3):
            for col in range(3):
                new_face[col][2 - row] = face[row][col]
        self.cube[index] = new_face

# face:
#     T
#   L F R B
#     D
    def rotate(self, face, direction):
        if (direction == "counter-clockwise"):
            self.rotate(face, "clockwise")
            self.rotate(face, "clockwise")
            self.rotate(face, "clockwise")
            return
        if face == 'T':
            self.rotate_face(self.get_face('T'))
            line = self.cube[self.get_face('F')][0]
            self.cube[self.get_face('F')][0] = self.cube[self.get_face('R')][0]
            self.cube[self.get_face('R')][0] = self.cube[self.get_face('B')][0]
            self.cube[self.get_face('B')][0] = self.cube[self.get_face('L')][0]
            self.cube[self.get_face('L')][0] = line
        if face == 'D':
            self.rotate_face(self.get_face('D'))
            line = self.cube[self.get_face('F')][2]
            self.cube[self.get_face('F')][2] = self.cube[self.get_face('L')][2]
            self.cube[self.get_face('L')][2] = self.cube[self.get_face('B')][2]
            self.cube[self.get_face('B')][2] = self.cube[self.get_face('R')][2]
            self.cube[self.get_face('R')][2] = line
        if face == 'F':
            self.rotate_face(self.get_face('F'))
            line = [self.cube[self.get_face('T')][2][0], self.cube[self.get_face('T')][2][1], self.cube[self.get_face('T')][2][2]]
            self.cube[self.get_face('T')][0][0] = self.cube[self.get_face('R')][0][2]
            self.cube[self.get_face('T')][0][1] = self.cube[self.get_face('R')][1][2]
            self.cube[self.get_face('T')][0][2] = self.cube[self.get_face('R')][2][2]
            self.cube[self.get_face('R')][0][2] = self.cube[self.get_face('D')][2][2]
            self.cube[self.get_face('R')][1][2] = self.cube[self.get_face('D')][2][1]
            self.cube[self.get_face('R')][2][2] = self.cube[self.get_face('D')][2][0]
            self.cube[self.get_face('D')][0][0] = self.cube[self.get_face('L')][2][0]
            self.cube[self.get_face('D')][0][1] = self.cube[self.get_face('L')][1][0]
            self.cube[self.get_face('D')][0][2] = self.cube[self.get_face('L')][0][0]
            self.cube[self.get_face('L')][2][0] = line[0]
            self.cube[self.get_face('L')][1][0] = line[1]
            self.cube[self.get_face('L')][0][0] = line[2]
        if face == 'B':
            self.rotate_face(self.get_face('B'))
            line = [self.cube[self.get_face('T')][0][0], self.cube[self.get_face('T')][0][1], self.cube[self.get_face('T')][0][2]]
            self.cube[self.get_face('T')][0][0] = self.cube[self.get_face('R')][0][2]
            self.cube[self.get_face('T')][0][1] = self.cube[self.get_face('R')][1][2]
            self.cube[self.get_face('T')][0][2] = self.cube[self.get_face('R')][2][2]
            self.cube[self.get_face('R')][0][2] = self.cube[self.get_face('D')][2][2]
            self.cube[self.get_face('R')][1][2] = self.cube[self.get_face('D')][2][1]
            self.cube[self.get_face('R')][2][2] = self.cube[self.get_face('D')][2][0]
            self.cube[self.get_face('D')][2][0] = self.cube[self.get_face('L')][0][0]
            self.cube[self.get_face('D')][2][1] = self.cube[self.get_face('L')][1][0]
            self.cube[self.get_face('D')][2][2] = self.cube[self.get_face('L')][2][0]
            self.cube[self.get_face('L')][2][0] = line[0]
            self.cube[self.get_face('L')][1][0] = line[1]
            self.cube[self.get_face('L')][0][0] = line[2]
        if face == 'L':
            self.rotate_face(self.get_face('L'))
            line = [self.cube[self.get_face('T')][0][0], self.cube[self.get_face('T')][1][0], self.cube[self.get_face('T')][2][0]]
            self.cube[self.get_face('T')][0][0] = self.cube[self.get_face('B')][2][2]
            self.cube[self.get_face('T')][1][0] = self.cube[self.get_face('B')][1][2]
            self.cube[self.get_face('T')][2][0] = self.cube[self.get_face('B')][0][2]
            self.cube[self.get_face('B')][0][2] = self.cube[self.get_face('D')][2][0]
            self.cube[self.get_face('B')][1][2] = self.cube[self.get_face('D')][1][0]
            self.cube[self.get_face('B')][2][2] = self.cube[self.get_face('D')][0][0]
            self.cube[self.get_face('D')][0][0] = self.cube[self.get_face('F')][0][0]
            self.cube[self.get_face('D')][1][0] = self.cube[self.get_face('F')][1][0]
            self.cube[self.get_face('D')][2][0] = self.cube[self.get_face('F')][2][0]
            self.cube[self.get_face('F')][0][0] = line[0]
            self.cube[self.get_face('F')][1][0] = line[1]
            self.cube[self.get_face('F')][2][0] = line[2]
        if face == 'R':
            self.rotate_face(self.get_face('R'))
            line = [self.cube[self.get_face('T')][0][2], self.cube[self.get_face('T')][1][2], self.cube[self.get_face('T')][2][2]]
            self.cube[self.get_face('T')][0][2] = self.cube[self.get_face('F')][0][2]
            self.cube[self.get_face('T')][1][2] = self.cube[self.get_face('F')][1][2]
            self.cube[self.get_face('T')][2][2] = self.cube[self.get_face('F')][2][2]
            self.cube[self.get_face('F')][0][2] = self.cube[self.get_face('D')][0][2]
            self.cube[self.get_face('F')][1][2] = self.cube[self.get_face('D')][1][2]
            self.cube[self.get_face('F')][2][2] = self.cube[self.get_face('D')][2][2]
            self.cube[self.get_face('D')][0][2] = self.cube[self.get_face('B')][2][0]
            self.cube[self.get_face('D')][1][2] = self.cube[self.get_face('B')][1][0]
            self.cube[self.get_face('D')][2][2] = self.cube[self.get_face('B')][0][0]
            self.cube[self.get_face('B')][0][0] = line[2]
            self.cube[self.get_face('B')][1][0] = line[1]
            self.cube[self.get_face('B')][2][0] = line[0]

    def show(self):
        def print_face(face):
            for row in range(3):
                print("            ", end=' ');
                for col in range(3):
                    color = self.get_color(face[row][col])
                    print(f"\033[{color}m■\033[0m", end=' ')
                print()
            print()
        print("-" * 12, end='')
        print(" Rubik's Cube ", end='')
        print("-" * 12)
        print()
        print_face(self.cube[0])
        for row in range(3):
            print("     ", end=' ');
            for index in range(1, 5):
                face = self.cube[index]
                for col in range(3):
                    color = self.get_color(face[row][col])
                    print(f"\033[{color}m■\033[0m", end=' ')
                print(end=' ')
            print()
        print()
        print_face(self.cube[5])
        print("-" * 12, end='')
        print("--------------", end='')
        print("-" * 12)

    def get_color(self, sticker):
        colors = {'W': '97', 'R': '91', 'G': '92', 'O': '95', 'B': '94', 'Y': '93'}
        return colors[sticker]

    def get_face(self, face):
        faces = {0: 'T', 1: 'L', 2: 'F', 3: 'R', 4: 'B', 5: 'D'}
        if isinstance(face, int):
            return faces.get(face)
        else:
            for index, label in faces.items():
                if label == face:
                    return index
        return None

    def shuffle(self, moves):
        all = []
        all_possible_moves = ['T', 'L', 'F', 'R', 'B', 'D']
        possible_moves = ['T', 'L', 'F', 'R', 'B', 'D']
        for _ in range(moves):
            rep = random.randint(1, 3)
            face = random.choice(possible_moves)
            move = f"{face}"
            if rep == 2:
                move += '2'
            elif rep == 3:
                move += "'"
            all.append(move)
            possible_moves = all_possible_moves.copy()
            possible_moves.remove(face)
        return all

    def do_move(self, move):
        face = move[0]
        if len(move) == 1:
            self.rotate(face, 'clockwise')
        elif move[1] == '2':
            self.rotate(face, 'clockwise')
            self.rotate(face, 'clockwise')
        elif move[1] == "'":
            self.rotate(face, 'counter-clockwise')