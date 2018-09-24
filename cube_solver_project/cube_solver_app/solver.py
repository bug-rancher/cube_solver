import json
import copy

from .cube import Cube
from .move import Move
from .algorithms import Algorithms
from .sticker import Sticker
from .edge import Edge
from .corner import Corner


class Solver(object):
    def __init__(self):
        self.__cube = None
        self.__virtual_cube = None

        self.__moves_list = []

        self.__algorithms = Algorithms()
        self.__rotation_counter = 0

        self.__up_face_color = None
        self.__side_face_colors = None
        self.__down_face_color = None

        self.__symbols_table = {"F": ["F", "R", "B", "L"],
                                "F2": ["F2", "R2", "B2", "L2"],
                                "F'": ["F'", "R'", "B'", "L'"],
                                "R": ["R", "B", "L", "F"],
                                "R2": ["R2", "B2", "L2", "F2"],
                                "R'": ["R'", "B'", "L'", "F'"],
                                "B": ["B", "L", "F", "R"],
                                "B2": ["B2", "L2", "F2", "R2"],
                                "B'": ["B'", "L'", "F'", "R'"],
                                "L": ["L", "F", "R", "B"],
                                "L2": ["L2", "F2", "R2", "B2"],
                                "L'": ["L'", "F'", "R'", "B'"],
                                "U": ["U", "U", "U", "U"],
                                "U2": ["U2", "U2", "U2", "U2"],
                                "U'": ["U'", "U'", "U'", "U'"],
                                "D": ["D", "D", "D", "D"],
                                "D2": ["D2", "D2", "D2", "D2"],
                                "D'": ["D'", "D'", "D'", "D'"],
                                "Z": ["Z", "Z", "Z", "Z"]}

    def solve(self, cube):
        self.__cube = cube
        self.__virtual_cube = copy.deepcopy(cube)

        self.__set_colors()

        self.__first_cross()
        self.__first_layer()
        self.__second_layer()
        self.__second_cross_orientation()
        self.__second_cross_permutation()
        self.__corners_permutation()
        self.__corners_orientation()

    def __set_colors(self):
        self.__up_face_color = self.__cube.layout[1][1]
        self.__side_face_colors = [self.__cube.layout[4][1], self.__cube.layout[4][4], self.__cube.layout[4][7],
                                   self.__cube.layout[4][10], self.__cube.layout[4][1], self.__cube.layout[4][4],
                                   self.__cube.layout[4][7]]
        self.__down_face_color = self.__cube.layout[7][1]

    def __first_cross(self):
        for i in range(4):
            wanted_edge = Edge([Sticker(self.__up_face_color), Sticker(self.__side_face_colors[i])])
            self.__find_element_and_execute_algorithm(wanted_edge, "first_cross")

            self.__make_moves(("Z",))

    def __find_element_and_execute_algorithm(self, element, function_name):
        if type(element) == Edge:
            try:
                position = self.__virtual_cube.edges.index(element.r_0)
                self.__make_moves(self.__algorithms.stages[function_name]["r_0"][position])
            except ValueError:
                pass

            try:
                position = self.__virtual_cube.edges.index(element.r_1)
                self.__make_moves(self.__algorithms.stages[function_name]["r_1"][position])
            except ValueError:
                pass

        if type(element) == Corner:
            try:
                position = self.__virtual_cube.corners.index(element.r_0)
                self.__make_moves(self.__algorithms.stages[function_name]["r_0"][position])
            except ValueError:
                pass

            try:
                position = self.__virtual_cube.corners.index(element.r_1)
                self.__make_moves(self.__algorithms.stages[function_name]["r_1"][position])
            except ValueError:
                pass

            try:
                position = self.__virtual_cube.corners.index(element.r_2)
                self.__make_moves(self.__algorithms.stages[function_name]["r_2"][position])
            except ValueError:
                pass

    def __make_moves(self, symbols):
        for symbol in symbols:
            self.__make_one_move(symbol)

        self.__virtual_cube.fill_edges()
        self.__virtual_cube.fill_corners()

    def __make_one_move(self, symbol):
        self.__turn_cube(self.__virtual_cube, symbol)

        if symbol == "Z":
            self.__rotation_counter += 1

        if symbol != "Z":
            virtual_cube_position = self.__rotation_counter % 4
            symbol_for_solution = self.__symbols_table[symbol][virtual_cube_position]
            self.__turn_cube(self.__cube, symbol_for_solution)

            self.__update_moves_list(symbol_for_solution)

    def __turn_cube(self, cube, symbol):
        if symbol == "F": cube.front_clockwise()
        elif symbol == "F2": cube.front_double()
        elif symbol == "F'": cube.front_counterclockwise()
        elif symbol == "R": cube.right_clockwise()
        elif symbol == "R2": cube.right_double()
        elif symbol == "R'": cube.right_counterclockwise()
        elif symbol == "B": cube.back_clockwise()
        elif symbol == "B2": cube.back_double()
        elif symbol == "B'": cube.back_counterclockwise()
        elif symbol == "L": cube.left_clockwise()
        elif symbol == "L2": cube.left_double()
        elif symbol == "L'": cube.left_counterclockwise()
        elif symbol == "U": cube.up_clockwise()
        elif symbol == "U2": cube.up_double()
        elif symbol == "U'": cube.up_counterclockwise()
        elif symbol == "D": cube.down_clockwise()
        elif symbol == "D2": cube.down_double()
        elif symbol == "D'": cube.down_counterclockwise()
        elif symbol == "Z": cube.turn_cube_right()

    def __update_moves_list(self, symbol):
        number = len(self.__moves_list)
        layout = copy.deepcopy(self.__cube.layout)

        move = Move(number, symbol, layout)
        self.__moves_list.append(move)

    def __first_layer(self):
        for i in range(4):
            wanted_corner = Corner([Sticker(self.__up_face_color),
                                    Sticker(self.__side_face_colors[i]),
                                    Sticker(self.__side_face_colors[i + 1])])

            self.__find_element_and_execute_algorithm(wanted_corner, "first_layer_extract")
            self.__find_element_and_execute_algorithm(wanted_corner, "first_layer_position")
            self.__find_element_and_execute_algorithm(wanted_corner, "first_layer_insert")

            self.__make_moves(("Z",))

    def __second_layer(self):
        for i in range(4):
            wanted_edge = Edge([Sticker(self.__side_face_colors[i]), Sticker(self.__side_face_colors[i + 1])])

            self.__find_element_and_execute_algorithm(wanted_edge, "second_layer_extract")
            self.__find_element_and_execute_algorithm(wanted_edge, "second_layer_position")
            self.__find_element_and_execute_algorithm(wanted_edge, "second_layer_insert")

            self.__make_moves(("Z",))

    def __second_cross_orientation(self):
        if self.__all_cross_stickers_in_places():
            return

        if self.__neither_cross_sticker_in_place():
            self.__make_moves(self.__algorithms.stages["second_cross_orientation"]["neither"])

        if self.__vertical_cross_stickers_in_places():
            self.__make_moves(self.__algorithms.stages["second_cross_orientation"]["vertical"])

        elif self.__horizontal_cross_stickers_in_places():
            self.__make_moves(self.__algorithms.stages["second_cross_orientation"]["horizontal"])

        while not self.__neighbouring_cross_stickers_in_places():
            self.__make_moves(("Z",))

        if self.__neighbouring_cross_stickers_in_places():
            self.__make_moves(self.__algorithms.stages["second_cross_orientation"]["neighbouring"])

    def __all_cross_stickers_in_places(self):
        result = (self.__virtual_cube.edges[8][0] == self.__down_face_color and
                  self.__virtual_cube.edges[9][0] == self.__down_face_color and
                  self.__virtual_cube.edges[10][0] == self.__down_face_color and
                  self.__virtual_cube.edges[11][0] == self.__down_face_color)

        return result

    def __neither_cross_sticker_in_place(self):
        result = (self.__virtual_cube.edges[8][0] != self.__down_face_color and
                  self.__virtual_cube.edges[9][0] != self.__down_face_color and
                  self.__virtual_cube.edges[10][0] != self.__down_face_color and
                  self.__virtual_cube.edges[11][0] != self.__down_face_color)

        return result

    def __vertical_cross_stickers_in_places(self):
        result = (self.__virtual_cube.edges[8][0] == self.__down_face_color and
                  self.__virtual_cube.edges[10][0] == self.__down_face_color)

        return result

    def __horizontal_cross_stickers_in_places(self):
        result = (self.__virtual_cube.edges[9][0] == self.__down_face_color and
                  self.__virtual_cube.edges[11][0] == self.__down_face_color)

        return result

    def __neighbouring_cross_stickers_in_places(self):
        result = (self.__virtual_cube.edges[8][0] == self.__down_face_color and
                  self.__virtual_cube.edges[9][0] == self.__down_face_color)

        return result

    def __second_cross_permutation(self):
        for i in range(4):
            if self.__all_second_cross_side_stickers_in_places(i):
                while not self.__down_layer_orientation_match():
                    self.__make_moves(("D",))

                return

        for i in range(4):
            for j in range(4):
                if self.__two_near_second_cross_side_stickers_in_places(i, j):
                    for k in range(j):
                        self.__make_moves(("D'",))

                    for m in range(3):
                        self.__make_moves(("Z",))

                    self.__make_moves(self.__algorithms.stages["second_cross_permutation"]["algorithm"])

                    while not self.__down_layer_orientation_match():
                        self.__make_moves(("D",))

                    return

        for i in range(4):
            if self.__two_far_second_cross_side_stickers_in_places(i):
                self.__make_moves(self.__algorithms.stages["second_cross_permutation"]["algorithm"])
                self.__make_moves(("Z",))
                self.__make_moves(self.__algorithms.stages["second_cross_permutation"]["algorithm"])

                while not self.__down_layer_orientation_match():
                    self.__make_moves(("D",))

                return

    def __all_second_cross_side_stickers_in_places(self, i):
        result = (self.__virtual_cube.edges[8][1] == self.__side_face_colors[i] and
                  self.__virtual_cube.edges[9][1] == self.__side_face_colors[i + 1] and
                  self.__virtual_cube.edges[10][1] == self.__side_face_colors[i + 2] and
                  self.__virtual_cube.edges[11][1] == self.__side_face_colors[i + 3])

        return result

    def __down_layer_orientation_match(self):
        result = self.__virtual_cube.edges[8][1] == self.__virtual_cube.layout[4][1]

        return result

    def __two_near_second_cross_side_stickers_in_places(self, i, j):
        stickers = [self.__virtual_cube.edges[8][1], self.__virtual_cube.edges[9][1], self.__virtual_cube.edges[10][1],
                    self.__virtual_cube.edges[11][1], self.__virtual_cube.edges[8][1]]

        result = (stickers[j] == self.__side_face_colors[i] and
                  stickers[j + 1] == self.__side_face_colors[i + 1])

        return result

    def __two_far_second_cross_side_stickers_in_places(self, i):
        result = (self.__virtual_cube.edges[9][1] == self.__side_face_colors[i + 1] and
                  self.__virtual_cube.edges[11][1] == self.__side_face_colors[i + 3])

        return result

    def __corners_permutation(self):
        for i in range(2):
            for j in range(4):
                if self.__two_corners_in_places():
                    return

                if self.__corer_in_position_to_begin():
                    self.__make_moves(("Z", "Z"))
                    self.__make_moves(self.__algorithms.stages["corners_permutation"]["algorithm"])

                    if not self.__corer_in_position_to_begin():
                        self.__make_moves(self.__algorithms.stages["corners_permutation"]["algorithm"])

                    return

                else:
                    self.__make_moves(("Z",))

            self.__make_moves(self.__algorithms.stages["corners_permutation"]["algorithm"])

    def __two_corners_in_places(self):
        result = (((self.__virtual_cube.corners[4][0] == self.__virtual_cube.edges[4][0] and self.__virtual_cube.corners[4][2] == self.__virtual_cube.edges[4][1]) or
                   (self.__virtual_cube.corners[4][1] == self.__virtual_cube.edges[4][0] and self.__virtual_cube.corners[4][0] == self.__virtual_cube.edges[4][1]) or
                   (self.__virtual_cube.corners[4][2] == self.__virtual_cube.edges[4][0] and self.__virtual_cube.corners[4][1] == self.__virtual_cube.edges[4][1])) and
                  ((self.__virtual_cube.corners[6][0] == self.__virtual_cube.edges[6][0] and self.__virtual_cube.corners[6][2] == self.__virtual_cube.edges[6][1]) or
                   (self.__virtual_cube.corners[6][1] == self.__virtual_cube.edges[6][0] and self.__virtual_cube.corners[6][0] == self.__virtual_cube.edges[6][1]) or
                   (self.__virtual_cube.corners[6][2] == self.__virtual_cube.edges[6][0] and self.__virtual_cube.corners[6][1] == self.__virtual_cube.edges[6][1])))

        return result

    def __corer_in_position_to_begin(self):
        result = ((self.__virtual_cube.corners[4][0] == self.__virtual_cube.edges[4][0] and self.__virtual_cube.corners[4][2] == self.__virtual_cube.edges[4][1]) or
                  (self.__virtual_cube.corners[4][1] == self.__virtual_cube.edges[4][0] and self.__virtual_cube.corners[4][0] == self.__virtual_cube.edges[4][1]) or
                  (self.__virtual_cube.corners[4][2] == self.__virtual_cube.edges[4][0] and self.__virtual_cube.corners[4][1] == self.__virtual_cube.edges[4][1]))

        return result

    def __corners_orientation(self):
        for i in range(4):
            if self.__down_face_color_on_left():
                self.__make_moves(self.__algorithms.stages["corners_orientation"]["first"])
                self.__make_moves(("D",))
                self.__make_moves(self.__algorithms.stages["corners_orientation"]["second"])
                self.__make_moves(("D'",))

            elif self.__down_face_color_in_place():
                pass

            elif self.__down_face_color_on_right():
                self.__make_moves(self.__algorithms.stages["corners_orientation"]["second"])
                self.__make_moves(("D",))
                self.__make_moves(self.__algorithms.stages["corners_orientation"]["first"])
                self.__make_moves(("D'",))

            self.__make_moves(("Z", "Z", "Z"))

    def __down_face_color_on_left(self):
        result = self.__virtual_cube.corners[4][0] == self.__down_face_color

        return result

    def __down_face_color_in_place(self):
        result = self.__virtual_cube.corners[4][1] == self.__down_face_color

        return result

    def __down_face_color_on_right(self):
        result = self.__virtual_cube.corners[4][2] == self.__down_face_color

        return result

    def get_moves(self):
        new_moves_list = []

        for move in self.__moves_list:
            new_moves_list.append(move.__dict__)

        result = {"is_error": False,
                  "moves": new_moves_list}

        moves_in_json = json.dumps(result)

        return moves_in_json


def solve(input):
    layout = json.loads(input)

    cube = Cube(layout)
    solver = Solver()

    solver.solve(cube)

    moves = solver.get_moves()

    return moves
