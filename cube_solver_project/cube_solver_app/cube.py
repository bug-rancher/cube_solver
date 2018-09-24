
class Cube(object):
    def __init__(self, initial_layout):

        self.layout = initial_layout
        self.edges = []
        self.corners = []

        self.fill_edges()
        self.fill_corners()

    def __turn_front_face_right(self):
        temp = self.layout[3][1]             # turn 4 face stickers on edges
        self.layout[3][1] = self.layout[4][0]
        self.layout[4][0] = self.layout[5][1]
        self.layout[5][1] = self.layout[4][2]
        self.layout[4][2] = temp

        temp = self.layout[3][0]             # turn 4 face stickers on corners
        self.layout[3][0] = self.layout[5][0]
        self.layout[5][0] = self.layout[5][2]
        self.layout[5][2] = self.layout[3][2]
        self.layout[3][2] = temp

        temp = self.layout[2][1]             # turn 4 side stickers on edges
        self.layout[2][1] = self.layout[4][11]
        self.layout[4][11] = self.layout[6][1]
        self.layout[6][1] = self.layout[4][3]
        self.layout[4][3] = temp

        temp = self.layout[2][0]             # turn 4 right side stickers on corners
        self.layout[2][0] = self.layout[5][11]
        self.layout[5][11] = self.layout[6][2]
        self.layout[6][2] = self.layout[3][3]
        self.layout[3][3] = temp

        temp = self.layout[2][2]             # turn 4 left side stickers on corners
        self.layout[2][2] = self.layout[3][11]
        self.layout[3][11] = self.layout[6][0]
        self.layout[6][0] = self.layout[5][3]
        self.layout[5][3] = temp

    def turn_cube_right(self):
        temp = self.layout[0][1]             # turn 4 face stickers on edges on top face
        self.layout[0][1] = self.layout[1][0]
        self.layout[1][0] = self.layout[2][1]
        self.layout[2][1] = self.layout[1][2]
        self.layout[1][2] = temp

        temp = self.layout[0][0]             # turn 4 face stickers on corners on top face
        self.layout[0][0] = self.layout[2][0]
        self.layout[2][0] = self.layout[2][2]
        self.layout[2][2] = self.layout[0][2]
        self.layout[0][2] = temp

        for i in range(3, 6):           # turn 4 faces
            for j in range(3):
                temp = self.layout[i][j]
                self.layout[i][j] = self.layout[i][j + 3]
                self.layout[i][j + 3] = self.layout[i][j + 6]
                self.layout[i][j + 6] = self.layout[i][j + 9]
                self.layout[i][j + 9] = temp

        temp = self.layout[6][1]             # turn 4 face stickers on edges on bottom face
        self.layout[6][1] = self.layout[7][2]
        self.layout[7][2] = self.layout[8][1]
        self.layout[8][1] = self.layout[7][0]
        self.layout[7][0] = temp

        temp = self.layout[6][0]             # turn 4 face stickers on corners on bottom face
        self.layout[6][0] = self.layout[6][2]
        self.layout[6][2] = self.layout[8][2]
        self.layout[8][2] = self.layout[8][0]
        self.layout[8][0] = temp

    def __turn_cube_down(self):
        for i in range(3):              # turn up, down, front and back faces
            for j in range(3):
                temp = self.layout[i][j]
                self.layout[i][j] = self.layout[5 - i][8 - j]
                self.layout[5 - i][8 - j] = self.layout[i + 6][j]
                self.layout[i + 6][j] = self.layout[i + 3][j]
                self.layout[i + 3][j] = temp

        temp = self.layout[3][4]             # turn 4 face stickers on edges on right face
        self.layout[3][4] = self.layout[4][5]
        self.layout[4][5] = self.layout[5][4]
        self.layout[5][4] = self.layout[4][3]
        self.layout[4][3] = temp

        temp = self.layout[3][3]             # turn 4 face stickers on corners on right face
        self.layout[3][3] = self.layout[3][5]
        self.layout[3][5] = self.layout[5][5]
        self.layout[5][5] = self.layout[5][3]
        self.layout[5][3] = temp

        temp = self.layout[3][10]             # turn 4 face stickers on edges on left face
        self.layout[3][10] = self.layout[4][9]
        self.layout[4][9] = self.layout[5][10]
        self.layout[5][10] = self.layout[4][11]
        self.layout[4][11] = temp

        temp = self.layout[3][9]             # turn 4 face stickers on corners on left face
        self.layout[3][9] = self.layout[5][9]
        self.layout[5][9] = self.layout[5][11]
        self.layout[5][11] = self.layout[3][11]
        self.layout[3][11] = temp

    def __manipulate(self, transformation):
        for i in range(transformation["cube_right"]):
            self.turn_cube_right()

        for i in range(transformation["cube_down"]):
            self.__turn_cube_down()

        for i in range(transformation["front_right"]):
            self.__turn_front_face_right()

        for i in range(4 - transformation["cube_right"]):
            self.turn_cube_right()

        for i in range(4 - transformation["cube_down"]):
            self.__turn_cube_down()

    def front_clockwise(self):
        transformation = {"cube_right": 0, "cube_down": 0, "front_right": 1}

        self.__manipulate(transformation)

    def front_double(self):
        transformation = {"cube_right": 0, "cube_down": 0, "front_right": 2}

        self.__manipulate(transformation)

    def front_counterclockwise(self):
        transformation = {"cube_right": 0, "cube_down": 0, "front_right": 3}

        self.__manipulate(transformation)

    def right_clockwise(self):
        transformation = {"cube_right": 1, "cube_down": 0, "front_right": 1}

        self.__manipulate(transformation)

    def right_double(self):
        transformation = {"cube_right": 1, "cube_down": 0, "front_right": 2}

        self.__manipulate(transformation)

    def right_counterclockwise(self):
        transformation = {"cube_right": 1, "cube_down": 0, "front_right": 3}

        self.__manipulate(transformation)

    def back_clockwise(self):
        transformation = {"cube_right": 2, "cube_down": 0, "front_right": 1}

        self.__manipulate(transformation)

    def back_double(self):
        transformation = {"cube_right": 2, "cube_down": 0, "front_right": 2}

        self.__manipulate(transformation)

    def back_counterclockwise(self):
        transformation = {"cube_right": 2, "cube_down": 0, "front_right": 3}

        self.__manipulate(transformation)

    def left_clockwise(self):
        transformation = {"cube_right": 3, "cube_down": 0, "front_right": 1}

        self.__manipulate(transformation)

    def left_double(self):
        transformation = {"cube_right": 3, "cube_down": 0, "front_right": 2}

        self.__manipulate(transformation)

    def left_counterclockwise(self):
        transformation = {"cube_right": 3, "cube_down": 0, "front_right": 3}

        self.__manipulate(transformation)

    def up_clockwise(self):
        transformation = {"cube_right": 0, "cube_down": 1, "front_right": 1}

        self.__manipulate(transformation)

    def up_double(self):
        transformation = {"cube_right": 0, "cube_down": 1, "front_right": 2}

        self.__manipulate(transformation)

    def up_counterclockwise(self):
        transformation = {"cube_right": 0, "cube_down": 1, "front_right": 3}

        self.__manipulate(transformation)

    def down_clockwise(self):
        transformation = {"cube_right": 0, "cube_down": 3, "front_right": 1}

        self.__manipulate(transformation)

    def down_double(self):
        transformation = {"cube_right": 0, "cube_down": 3, "front_right": 2}

        self.__manipulate(transformation)

    def down_counterclockwise(self):
        transformation = {"cube_right": 0, "cube_down": 3, "front_right": 3}

        self.__manipulate(transformation)

    def whole_right(self):
        transformation = {"cube_right": 1, "cube_down": 0, "front_right": 0}

        self.__manipulate(transformation)


    def fill_edges(self):
        self.edges = [[self.layout[2][1], self.layout[3][1]],
                      [self.layout[1][2], self.layout[3][4]],
                      [self.layout[0][1], self.layout[3][7]],
                      [self.layout[1][0], self.layout[3][10]],
                      [self.layout[4][2], self.layout[4][3]],
                      [self.layout[4][5], self.layout[4][6]],
                      [self.layout[4][8], self.layout[4][9]],
                      [self.layout[4][11], self.layout[4][0]],
                      [self.layout[6][1], self.layout[5][1]],
                      [self.layout[7][2], self.layout[5][4]],
                      [self.layout[8][1], self.layout[5][7]],
                      [self.layout[7][0], self.layout[5][10]]]

    def fill_corners(self):
        self.corners = [[self.layout[2][2], self.layout[3][2], self.layout[3][3]],
                        [self.layout[0][2], self.layout[3][5], self.layout[3][6]],
                        [self.layout[0][0], self.layout[3][8], self.layout[3][9]],
                        [self.layout[2][0], self.layout[3][11], self.layout[3][0]],
                        [self.layout[5][2], self.layout[6][2], self.layout[5][3]],
                        [self.layout[5][5], self.layout[8][2], self.layout[5][6]],
                        [self.layout[5][8], self.layout[8][0], self.layout[5][9]],
                        [self.layout[5][11], self.layout[6][0], self.layout[5][0]]]
