import copy
import json

from .sticker import Sticker
from .center import Center
from .edge import Edge
from .corner import Corner
from .move import Move


class Tester(object):
    def __init__(self):
        self.__layout = []

        self.__edges_samples = []
        self.__corners_samples = []

        self.__centres = []
        self.__edges = []
        self.__corners = []

        self.__errors_list = []

    def test(self, layout):
        self.__layout = layout

        self.__fill_elements()
        self.__run_tests()

    def __fill_elements(self):
        self.__fill_edges_samples()
        self.__fill_corners_samples()

        self.__fill_centres()
        self.__fill_edges()
        self.__fill_corners()

    def __fill_edges_samples(self):
        layout = self.__layout

        self.__edges_samples = [Edge([Sticker(layout[1][1]), Sticker(layout[4][1])]),
                                Edge([Sticker(layout[1][1]), Sticker(layout[4][4])]),
                                Edge([Sticker(layout[1][1]), Sticker(layout[4][7])]),
                                Edge([Sticker(layout[1][1]), Sticker(layout[4][10])]),

                                Edge([Sticker(layout[4][1]), Sticker(layout[4][4])]),
                                Edge([Sticker(layout[4][4]), Sticker(layout[4][7])]),
                                Edge([Sticker(layout[4][7]), Sticker(layout[4][10])]),
                                Edge([Sticker(layout[4][10]), Sticker(layout[4][1])]),

                                Edge([Sticker(layout[7][1]), Sticker(layout[4][1])]),
                                Edge([Sticker(layout[7][1]), Sticker(layout[4][4])]),
                                Edge([Sticker(layout[7][1]), Sticker(layout[4][7])]),
                                Edge([Sticker(layout[7][1]), Sticker(layout[4][10])])]

    def __fill_corners_samples(self):
        layout = self.__layout

        self.__corners_samples = [Corner([Sticker(layout[1][1]), Sticker(layout[4][1]), Sticker(layout[4][4])]),
                                  Corner([Sticker(layout[1][1]), Sticker(layout[4][4]), Sticker(layout[4][7])]),
                                  Corner([Sticker(layout[1][1]), Sticker(layout[4][7]), Sticker(layout[4][10])]),
                                  Corner([Sticker(layout[1][1]), Sticker(layout[4][10]), Sticker(layout[4][1])]),

                                  Corner([Sticker(layout[4][1]), Sticker(layout[7][1]), Sticker(layout[4][4])]),
                                  Corner([Sticker(layout[4][4]), Sticker(layout[7][1]), Sticker(layout[4][7])]),
                                  Corner([Sticker(layout[4][7]), Sticker(layout[7][1]), Sticker(layout[4][10])]),
                                  Corner([Sticker(layout[4][10]), Sticker(layout[7][1]), Sticker(layout[4][1])])]

    def __fill_centres(self):
        layout = self.__layout

        self.__centres = [Center([Sticker(layout[1][1], 1, 1)]),
                          Center([Sticker(layout[4][1], 4, 1)]),
                          Center([Sticker(layout[4][4], 4, 4)]),
                          Center([Sticker(layout[4][7], 4, 7)]),
                          Center([Sticker(layout[4][10], 4, 10)]),
                          Center([Sticker(layout[7][1], 7, 1)])]

    def __fill_edges(self):
        layout = self.__layout

        self.__edges = [Edge([Sticker(layout[2][1], 2, 1), Sticker(layout[3][1], 3, 1)]),
                        Edge([Sticker(layout[1][2], 1, 2), Sticker(layout[3][4], 3, 4)]),
                        Edge([Sticker(layout[0][1], 0, 1), Sticker(layout[3][7], 3, 7)]),
                        Edge([Sticker(layout[1][0], 1, 0), Sticker(layout[3][10], 3, 10)]),

                        Edge([Sticker(layout[4][2], 4, 2), Sticker(layout[4][3], 4, 3)]),
                        Edge([Sticker(layout[4][5], 4, 5), Sticker(layout[4][6], 4, 6)]),
                        Edge([Sticker(layout[4][8], 4, 8), Sticker(layout[4][9], 4, 9)]),
                        Edge([Sticker(layout[4][11], 4, 11), Sticker(layout[4][0], 4, 0)]),

                        Edge([Sticker(layout[6][1], 6, 1), Sticker(layout[5][1], 5, 1)]),
                        Edge([Sticker(layout[7][2], 7, 2), Sticker(layout[5][4], 5, 4)]),
                        Edge([Sticker(layout[8][1], 8, 1), Sticker(layout[5][7], 5, 7)]),
                        Edge([Sticker(layout[7][0], 7, 0), Sticker(layout[5][10], 5, 10)])]

    def __fill_corners(self):
        layout = self.__layout

        self.__corners = [Corner([Sticker(layout[2][2], 2, 2), Sticker(layout[3][2], 3, 2), Sticker(layout[3][3], 3, 3)]),
                          Corner([Sticker(layout[0][2], 0, 2), Sticker(layout[3][5], 3, 5), Sticker(layout[3][6], 3, 6)]),
                          Corner([Sticker(layout[0][0], 0, 0), Sticker(layout[3][8], 3, 8), Sticker(layout[3][9], 3, 9)]),
                          Corner([Sticker(layout[2][0], 2, 0), Sticker(layout[3][11], 3, 11), Sticker(layout[3][0], 3, 0)]),

                          Corner([Sticker(layout[5][2], 5, 2), Sticker(layout[6][2], 6, 2), Sticker(layout[5][3], 5, 3)]),
                          Corner([Sticker(layout[5][5], 5, 5), Sticker(layout[8][2], 8, 2), Sticker(layout[5][6], 5, 6)]),
                          Corner([Sticker(layout[5][8], 5, 8), Sticker(layout[8][0], 8, 0), Sticker(layout[5][9], 5, 9)]),
                          Corner([Sticker(layout[5][11], 5, 11), Sticker(layout[6][0], 6, 0), Sticker(layout[5][0], 5, 0)])]

    def __run_tests(self):
        self.__check_filled()
        self.__check_centres()
        self.__check_edges_correct()
        self.__check_edges_repeated()
        self.__check_corners_correct()
        self.__check_corners_repeated()

    def __check_filled(self):
        layout_with_errors = copy.deepcopy(self.__layout)
        errors_number = 0

        for i, row in enumerate(self.__layout):
            for j, column in enumerate(self.__layout[i]):
                if self.__layout[i][j] == "transparent":
                    layout_with_errors[i][j] = "rgb(0, 0, 0)"

                    errors_number += 1

        if errors_number > 0:
            self.__update_errors_list(errors_number, "unfilled stickers", layout_with_errors)

    def __check_centres(self):
        layout_with_errors = copy.deepcopy(self.__layout)
        errors_number = 0

        for i in range(len(self.__centres)):
            j = i + 1

            while j < len(self.__centres):

                if self.__centres[i].color == self.__centres[j].color:
                    bad_elements = [self.__centres[i], self.__centres[j]]
                    self.__mark_stickers(layout_with_errors, bad_elements)

                    errors_number += 1

                j += 1

        if errors_number > 0:
            self.__update_errors_list(errors_number, "repeated centres", layout_with_errors)

    def __check_edges_correct(self):
        layout_with_errors = copy.deepcopy(self.__layout)
        errors_number = 0

        for edge in self.__edges:
            found = False

            for edge_sample in self.__edges_samples:

                if edge.r_0 == edge_sample.r_0 or edge.r_1 == edge_sample.r_0:
                    found = True
                    break

            if not found:
                bad_elements = [edge]
                self.__mark_stickers(layout_with_errors, bad_elements)

                errors_number += 1

        if errors_number > 0:
            self.__update_errors_list(errors_number, "bad edges", layout_with_errors)

    def __check_edges_repeated(self):
        layout_with_errors = copy.deepcopy(self.__layout)
        bad_elements_indexes = []

        for i in range(len(self.__edges)):
            j = i + 1

            while j < len(self.__edges):

                if self.__edges[i].r_0 == self.__edges[j].r_0 or self.__edges[i].r_1 == self.__edges[j].r_0:

                    indexes_to_check = [i, j]

                    for index in indexes_to_check:

                        if index not in bad_elements_indexes:
                            bad_elements_indexes.append(index)
                            bad_element = [self.__edges[index]]
                            self.__mark_stickers(layout_with_errors, bad_element)

                j += 1

        if len(bad_elements_indexes) > 0:
            self.__update_errors_list(len(bad_elements_indexes), "repeated edges", layout_with_errors)

    def __check_corners_correct(self):
        layout_with_errors = copy.deepcopy(self.__layout)
        errors_number = 0

        for corner in self.__corners:
            found = False

            for corner_sample in self.__corners_samples:

                if (corner.r_0 == corner_sample.r_0 or corner.r_1 == corner_sample.r_0 or
                        corner.r_2 == corner_sample.r_0):

                    found = True
                    break

            if not found:
                bad_elements = [corner]
                self.__mark_stickers(layout_with_errors, bad_elements)

                errors_number += 1

        if errors_number > 0:
            self.__update_errors_list(errors_number, "bad corners", layout_with_errors)

    def __check_corners_repeated(self):
        layout_with_errors = copy.deepcopy(self.__layout)
        bad_elements_indexes = []

        for i in range(len(self.__corners)):
            j = i + 1

            while j < len(self.__corners):

                if (self.__corners[i].r_0 == self.__corners[j].r_0 or self.__corners[i].r_1 == self.__corners[j].r_0 or
                        self.__corners[i].r_2 == self.__corners[j].r_0):

                    indexes_to_check = [i, j]

                    for index in indexes_to_check:

                        if index not in bad_elements_indexes:
                            bad_elements_indexes.append(index)
                            bad_element = [self.__corners[index]]
                            self.__mark_stickers(layout_with_errors, bad_element)

                j += 1

        if len(bad_elements_indexes) > 0:
            self.__update_errors_list(len(bad_elements_indexes), "repeated corners", layout_with_errors)

    def __mark_stickers(self, layout_with_errors, bad_elements):
        for element in bad_elements:
            for sticker in element.stickers:

                y = sticker.y
                x = sticker.x

                layout_with_errors[y][x] = "rgb(0, 0, 0)"

    def __update_errors_list(self, error_numbers, message, layout_with_errors):
        error = Move(error_numbers, message, layout_with_errors)

        self.__errors_list.append(error)

    def get_errors(self):
        new_errors_list = []

        for error in self.__errors_list:
            new_errors_list.append(error.__dict__)

        is_error = False

        if len(new_errors_list) > 0:
            is_error = True

        result = {"is_error": is_error,
                  "moves": new_errors_list}

        errors_in_json = json.dumps(result)

        return errors_in_json


def test(layout):
    layout = json.loads(layout)

    tester = Tester()
    tester.test(layout)

    errors = tester.get_errors()
    errors_parsed = json.loads(errors)

    return errors_parsed["is_error"], errors
