import random

from kociemba import solve as god_solve
from rich import print
from rich.panel import Panel


class RubiksCube:
    def __init__(self, cube=[
            [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
            [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
            [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
            [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']]
        ]):
        if (len(cube) != 6):
            raise ValueError("A cube must have 6 faces")
        for face in cube:
            if (len(face) != 3):
                raise ValueError("Each face must have 3 rows")
            for row in face:
                if (len(row) != 3):
                    raise ValueError("Each row must have 3 stickers")
                for sticker in row:
                    if sticker not in "WGRBOY":
                        raise ValueError("Invalid color.\nValid colors are:\n\tW: White\n\tG: Green\n\tR: Red\n\tB: Blue\n\tO: Orange\n\tY: Yellow")
        self.cube = cube

    def reset(self):
        self.__init__()

    def rotate_face(self, index):
        new_face = [['', '', ''], ['', '', ''], ['', '', '']]
        face = self.cube[index]
        for row in range(3):
            for col in range(3):
                new_face[col][2 - row] = face[row][col]
        self.cube[index] = new_face

    def invert(self, line):
        return [line[2], line[1], line[0]]

# face:
#     U
#   L F R B
#     D
    def rotate(self, movement): #face, direction):
        if not len(movement) in (1, 2) or movement[0] not in "ULFRBD" :
            raise ValueError("Invalid movement")
        face = movement[0]
        rep = 1
        if len(movement) == 2:
            if movement[1] not in "2'":
                raise ValueError("ratio")
            rep = 2 if movement[1] == '2' else 3

        for _ in range(rep):
            if face == 'U':
                self.rotate_face(self.get_face('U'))
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
                line = [self.cube[self.get_face('U')][2][0], self.cube[self.get_face('U')][2][1], self.cube[self.get_face('U')][2][2]]
                self.cube[self.get_face('U')][2][0] = self.cube[self.get_face('L')][2][2]
                self.cube[self.get_face('U')][2][1] = self.cube[self.get_face('L')][1][2]
                self.cube[self.get_face('U')][2][2] = self.cube[self.get_face('L')][0][2]
                self.cube[self.get_face('L')][0][2] = self.cube[self.get_face('D')][0][0]
                self.cube[self.get_face('L')][1][2] = self.cube[self.get_face('D')][0][1]
                self.cube[self.get_face('L')][2][2] = self.cube[self.get_face('D')][0][2]
                self.cube[self.get_face('D')][0][0] = self.cube[self.get_face('R')][2][0]
                self.cube[self.get_face('D')][0][1] = self.cube[self.get_face('R')][1][0]
                self.cube[self.get_face('D')][0][2] = self.cube[self.get_face('R')][0][0]
                self.cube[self.get_face('R')][0][0] = line[0]
                self.cube[self.get_face('R')][1][0] = line[1]
                self.cube[self.get_face('R')][2][0] = line[2]
            if face == 'B':
                self.rotate_face(self.get_face('B'))
                line = [self.cube[self.get_face('U')][0][2], self.cube[self.get_face('U')][0][1], self.cube[self.get_face('U')][0][0]]
                self.cube[self.get_face('U')][0][0] = self.cube[self.get_face('R')][0][2]
                self.cube[self.get_face('U')][0][1] = self.cube[self.get_face('R')][1][2]
                self.cube[self.get_face('U')][0][2] = self.cube[self.get_face('R')][2][2]
                self.cube[self.get_face('R')][0][2] = self.cube[self.get_face('D')][2][2]
                self.cube[self.get_face('R')][1][2] = self.cube[self.get_face('D')][2][1]
                self.cube[self.get_face('R')][2][2] = self.cube[self.get_face('D')][2][0]
                self.cube[self.get_face('D')][2][2] = self.cube[self.get_face('L')][2][0]
                self.cube[self.get_face('D')][2][1] = self.cube[self.get_face('L')][1][0]
                self.cube[self.get_face('D')][2][0] = self.cube[self.get_face('L')][0][0]
                self.cube[self.get_face('L')][0][0] = line[0]
                self.cube[self.get_face('L')][1][0] = line[1]
                self.cube[self.get_face('L')][2][0] = line[2]
            if face == 'L':
                self.rotate_face(self.get_face('L'))
                line = [self.cube[self.get_face('U')][0][0], self.cube[self.get_face('U')][1][0], self.cube[self.get_face('U')][2][0]]
                self.cube[self.get_face('U')][0][0] = self.cube[self.get_face('B')][2][2]
                self.cube[self.get_face('U')][1][0] = self.cube[self.get_face('B')][1][2]
                self.cube[self.get_face('U')][2][0] = self.cube[self.get_face('B')][0][2]
                self.cube[self.get_face('B')][2][2] = self.cube[self.get_face('D')][0][0]
                self.cube[self.get_face('B')][1][2] = self.cube[self.get_face('D')][1][0]
                self.cube[self.get_face('B')][0][2] = self.cube[self.get_face('D')][2][0]
                self.cube[self.get_face('D')][0][0] = self.cube[self.get_face('F')][0][0]
                self.cube[self.get_face('D')][1][0] = self.cube[self.get_face('F')][1][0]
                self.cube[self.get_face('D')][2][0] = self.cube[self.get_face('F')][2][0]
                self.cube[self.get_face('F')][0][0] = line[0]
                self.cube[self.get_face('F')][1][0] = line[1]
                self.cube[self.get_face('F')][2][0] = line[2]
            if face == 'R':
                self.rotate_face(self.get_face('R'))
                line = [self.cube[self.get_face('U')][0][2], self.cube[self.get_face('U')][1][2], self.cube[self.get_face('U')][2][2]]
                self.cube[self.get_face('U')][0][2] = self.cube[self.get_face('F')][0][2]
                self.cube[self.get_face('U')][1][2] = self.cube[self.get_face('F')][1][2]
                self.cube[self.get_face('U')][2][2] = self.cube[self.get_face('F')][2][2]
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
        cube = f"""       {self.get_color(self.cube[self.get_face('U')][0][0])}■[/] {self.get_color(self.cube[self.get_face('U')][0][1])}■[/] {self.get_color(self.cube[self.get_face('U')][0][2])}■[/]
       {self.get_color(self.cube[self.get_face('U')][1][0])}■[/] {self.get_color(self.cube[self.get_face('U')][1][1])}■[/] {self.get_color(self.cube[self.get_face('U')][1][2])}■[/]
       {self.get_color(self.cube[self.get_face('U')][2][0])}■[/] {self.get_color(self.cube[self.get_face('U')][2][1])}■[/] {self.get_color(self.cube[self.get_face('U')][2][2])}■[/]

{self.get_color(self.cube[self.get_face('L')][0][0])}■[/] {self.get_color(self.cube[self.get_face('L')][0][1])}■[/] {self.get_color(self.cube[self.get_face('L')][0][2])}■[/]  {self.get_color(self.cube[self.get_face('F')][0][0])}■[/] {self.get_color(self.cube[self.get_face('F')][0][1])}■[/] {self.get_color(self.cube[self.get_face('F')][0][2])}■[/]  {self.get_color(self.cube[self.get_face('R')][0][0])}■[/] {self.get_color(self.cube[self.get_face('R')][0][1])}■[/] {self.get_color(self.cube[self.get_face('R')][0][2])}■[/]  {self.get_color(self.cube[self.get_face('B')][0][0])}■[/] {self.get_color(self.cube[self.get_face('B')][0][1])}■[/] {self.get_color(self.cube[self.get_face('B')][0][2])}■[/]
{self.get_color(self.cube[self.get_face('L')][1][0])}■[/] {self.get_color(self.cube[self.get_face('L')][1][1])}■[/] {self.get_color(self.cube[self.get_face('L')][1][2])}■[/]  {self.get_color(self.cube[self.get_face('F')][1][0])}■[/] {self.get_color(self.cube[self.get_face('F')][1][1])}■[/] {self.get_color(self.cube[self.get_face('F')][1][2])}■[/]  {self.get_color(self.cube[self.get_face('R')][1][0])}■[/] {self.get_color(self.cube[self.get_face('R')][1][1])}■[/] {self.get_color(self.cube[self.get_face('R')][1][2])}■[/]  {self.get_color(self.cube[self.get_face('B')][1][0])}■[/] {self.get_color(self.cube[self.get_face('B')][1][1])}■[/] {self.get_color(self.cube[self.get_face('B')][1][2])}■[/]
{self.get_color(self.cube[self.get_face('L')][2][0])}■[/] {self.get_color(self.cube[self.get_face('L')][2][1])}■[/] {self.get_color(self.cube[self.get_face('L')][2][2])}■[/]  {self.get_color(self.cube[self.get_face('F')][2][0])}■[/] {self.get_color(self.cube[self.get_face('F')][2][1])}■[/] {self.get_color(self.cube[self.get_face('F')][2][2])}■[/]  {self.get_color(self.cube[self.get_face('R')][2][0])}■[/] {self.get_color(self.cube[self.get_face('R')][2][1])}■[/] {self.get_color(self.cube[self.get_face('R')][2][2])}■[/]  {self.get_color(self.cube[self.get_face('B')][2][0])}■[/] {self.get_color(self.cube[self.get_face('B')][2][1])}■[/] {self.get_color(self.cube[self.get_face('B')][2][2])}■[/]

       {self.get_color(self.cube[self.get_face('D')][0][0])}■[/] {self.get_color(self.cube[self.get_face('D')][0][1])}■[/] {self.get_color(self.cube[self.get_face('D')][0][2])}■[/]
       {self.get_color(self.cube[self.get_face('D')][1][0])}■[/] {self.get_color(self.cube[self.get_face('D')][1][1])}■[/] {self.get_color(self.cube[self.get_face('D')][1][2])}■[/]
       {self.get_color(self.cube[self.get_face('D')][2][0])}■[/] {self.get_color(self.cube[self.get_face('D')][2][1])}■[/] {self.get_color(self.cube[self.get_face('D')][2][2])}■[/]"""
        print("------------ Rubik's Cube ------------")
        print(Panel(cube, border_style="green", expand=False))
        print("--------------------------------------")

    def get_color(self, sticker):
        colors = {'W': '[bright_white]', 'R': '[red3]', 'G': '[chartreuse3]', 'O': '[dark_orange3]', 'B': '[dark_blue]', 'Y': '[yellow2]'}
        return colors[sticker]

    def get_face(self, face):
        faces = {0: 'U', 1: 'L', 2: 'F', 3: 'R', 4: 'B', 5: 'D'}
        if isinstance(face, int):
            return faces.get(face)
        else:
            for index, label in faces.items():
                if label == face:
                    return index
        return None

    def shuffle(self, moves=5):
        _moves = []
        all_possible_moves = ['U', 'L', 'F', 'R', 'B', 'D']
        possible_moves = ['U', 'L', 'F', 'R', 'B', 'D']
        for _ in range(moves):
            rep = random.randint(1, 3)
            face = random.choice(possible_moves)
            move = f"{face}"
            if rep == 2:
                move += '2'
            elif rep == 3:
                move += "'"
            _moves.append(move)
            possible_moves = all_possible_moves.copy()
            possible_moves.remove(face)
        for e in _moves:
            self.rotate(e)
        return _moves

    def do_move(self, move):
        face = move[0]
        if len(move) == 1:
            self.rotate(face, 'clockwise')
        elif move[1] == '2':
            self.rotate(face, 'clockwise')
            self.rotate(face, 'clockwise')
        elif move[1] == "'":
            self.rotate(face, 'counter-clockwise')

    def solve(self):
        sequence    = "URFDLB"
        values      = "URFDLB"
        corespond   = "WRGYOB"

        faces = [self.cube[self.get_face(e)] for e in sequence]

        faces = ''.join([''.join([''.join(y) for y in x]) for x in faces])

        for i in range(len(corespond)):
            faces = faces.replace(corespond[i], values[i])

        result = None

        try:
            result = god_solve(faces)
        except:
            pass
        if not result:
            return None

        for e in result.split(' '):
            self.rotate(e)
        return result.split(' ')
