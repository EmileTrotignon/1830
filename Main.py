# ==================================================================================================================== #
# ==================================================================================================================== #
#                                                                                                                      #
#  * Main.py                 *                                                                 |=---::++.--.++.:.-:.   #
#                                                                                                    -:-   -:-    -:-  #
#  * By : Emile Trotignon    *                                                                      :+:   :+:     :+:  #
#                                                                                                  :=:   :=:     :=:   #
# ---------------------------------------------------------------------------------------:==+-----+=+---+=+::===:+---- #
#                                                                                        +#+     +#:   :#:             #
#  * Created the : ??/??/2017 *                                                         =#=     =#=   =#=              #
#                                                                                       =#=    =#=   =#=               #
#  * TIPE : 1830              *                                                           :=##=+---+=#==---=| * MPSI * #
#                                                                                                                      #
# ==================================================================================================================== #
# ==================================================================================================================== #


from copy import copy, deepcopy
from typing import List, Union, Dict, Optional
from graphlib.main import *
import ascii_hex as ah


def rotate(li, n):

    return li[n:] + li[:n]


class Str2D:

    def __init__(self, entry: Union[List[List[str]], str]):

        if type(entry) == str:
            self._str_list = [list(s) for s in entry.split('\n')]
        else:
            self._str_list = entry

    def __getitem__(self, key: int) -> List[str]:

        return self._str_list[key]

    def __setitem__(self, key: int, item: List[str]):

        self._str_list[key] = item

    def __len__(self):

        return len(self._str_list)

    def __repr__(self) -> str:

        return f'Str2D({self._str_list})'

    def __str__(self) -> str:

        return '\n'.join(''.join(li) for li in self)

    def paint_over(self, other: 'Str2D', start=(0, 0), ignore=' ') -> 'Str2D':

        x0, y0 = start

        for y, line in enumerate(other):

            for x, char in enumerate(line):

                if y + y0 < len(self) and x0 + x < len(self[y0 + y]) and char != ignore:
                    self[y0 + y][x0 + x] = char

        return self


class Locus:

    pass


class Track(Locus):

    def __init__(self, hexagon, end_list0=None, end_list1=None):

        self.hexagon = hexagon
        self.end1 = [] if end_list0 is None else end_list0
        self.end2 = [] if end_list1 is None else end_list1
        self.end_tuple = (self.end1, self.end2)
        self.value = 0

    def __repr__(self):

        return 'Track object connected to {} and {} in {}'.format(str(self.end1), str(self.end2), str(self.hexagon))

    def connect(self, number, other_track_end):

        if number == 1:
            self.end1.end_list.append(other_track_end)
            other_track_end.end_list.append(self.end1)
        if number == 2:
            self.end2.end_list.append(other_track_end)
            other_track_end.end_list.append(self.end2)

    def neighbouring_locis(self, entry='start'):
        """ Return the connected end objects, except for the entry"""

        final_list = copy(self.end1 + self.end2)

        if entry != 'start':
            final_list.remove(entry)

        return final_list


class City(Locus):

    def __init__(self, name, hexagon, value, token_list=None):

        self.name = name
        self.hexagon = hexagon
        self.value = value
        self.token_list = [] if token_list is None else token_list
        self.end_list = []

    def __str__(self):

        rep = f'City named {self.name}, worth {self.value} in {str(self.hexagon)} with those tokens : {self.token_list}'
        return rep

    def connect(self, track: Track, end_number: int):

        self.end_list.append(track)
        track.end_tuple[end_number].append(self)

    def add_token(self, company):

        self.token_list.append(company)
        self.token_list.append(self)

    def neighbouring_locis(self, entry='start'):

        """ Return the connected end objects, except for the entry"""

        final_list = copy(self.end_list)

        if entry != 'start':
            final_list.remove(entry)

        return final_list


class Hexagon:

    def __init__(self, track_list: List[Track], city_dic: Dict[str, City], side_list: List[Tuple[Track, int]],
                 upgradeable=True, ascii_repr=ah.UNKNOWN_TILE):

        self.track_list = track_list
        self.city_dic = city_dic
        self.side_list = side_list
        self.upgradeable = upgradeable
        self._ascii_repr = Str2D(ascii_repr[1:])

    def __repr__(self) -> str:

        return f'Hexagon({self.track_list}, {self.city_dic}, upgradeable={self.upgradeable},' \
               f' ascii_repr={self._ascii_repr}'

    def __str__(self) -> str:

        return str(self._ascii_repr)

    def rotated(self, n_rot: int) -> 'Hexagon':

        return Hexagon(self.track_list, self.city_dic, rotate(self.side_list, n_rot))

    def str_2d(self) -> Str2D:

        return self._ascii_repr

    def add_track(self, end1, end2):

        self.track_list.append(Track(self, end1, end2))

        for e1 in end1:
            if type(e1) == City:

                e1.co_track_list.append(self)

            if type(e1) == Track:

                # so that end1 is always connected to another track's end2 and vice versa
                end1.end2.append(self)

        for e2 in end2:

            if type(e2) == City:

                end2.co_track_list.append(self)

            if type(e2) == Track:

                # so that end1 is always connected to another track's end2 and vice versa
                e2.e1.append(self)

    def add_city(self, name, hexagon, value, token_list):

        self.city_dic[name] = City(name, hexagon, value, token_list)

    def rotate(self):
        return self


empty_hex = Hexagon([], {}, ascii_repr=ah.EMPTY_TILE)


class Company:

    def __init__(self, name, token_list: List[City], train_list: List[Optional[int]], n_token: int):

        self.name = name
        self.token_list = token_list
        self.train_list = train_list
        self.n_token = n_token

    def __repr__(self):

        return 'Company named {}'.format(self.name)

    def run_trains(self, board):

        graph = board.generate_graph(company=self)
        start_vertices = [token.n for token in self.token_list]
        return graph.gen_max_pathes(start_vertices, self.train_list)


class Board:

    def __init__(self, company_dic: Dict[str, Company], resolution: Tuple[int, int]):

        self.hex_dic = {}
        self.company_dic = company_dic
        self.resolution = resolution
        self.ascii_repr = None
        self.gen_hex_dic()

    def __repr__(self) -> str:

        return f'Board({self.company_dic, {self.resolution}})'

    def __str__(self) -> str:

        return str(self.ascii_repr) if self.ascii_repr is not None else str(self.gen_ascii_repr())

    def gen_hex_dic(self):

        """Generate a rectangular hex board"""

        for x in range(self.resolution[0]):

            for y in range(self.resolution[1]):

                if x % 2 == y % 2:
                    self.hex_dic[(x, y)] = empty_hex

        self.gen_ascii_repr()

    def gen_ascii_repr(self):

        hy = len(empty_hex.str_2d())
        hx = len(empty_hex.str_2d()[0])
        line = ' ' * (15 * self.resolution[0] + 4)
        self.ascii_repr = Str2D(((line + '\n') * int((((hy - 1) * self.resolution[1] + hy + 1) / 2)))[:-1])
        print(hy)

        for x, y in self.hex_dic:

            self.ascii_repr.paint_over(empty_hex.str_2d(), start=(x * hx, y * (hy - 1) // 2))

        return self.ascii_repr

    def upgrade_hex(self, x, y, new_hex, check_rules=True):

        old_hex = self.hex_dic[(x, y)]
        if (not check_rules) or old_hex.upgradeable:
            self.hex_dic[(x, y)] = new_hex
            return True
        return False


    def add_company(self, company: Company):

        """Floats a new company"""

        self.company_dic[company.name] = company

    def generate_graph(self, company=None) -> WeightedVerticesGraph:
        locis_list = sum((hexa.track_list + hexa.city_list for hexa in self.hex_dic), [])

        i = 0
        for locus in locis_list:
            locus.n = i
            i += 1

        neighbouring_locis_list = [locus.neighbouring_locis() for locus in locis_list]

        if company is not None:  # Check tokens

            for k, locus in enumerate(locis_list):

                if type(locus) == City and None not in locus.token_list and company not in locus.token_list:
                    neighbouring_locis_list[k] = []

        neighbour_list = [[locus.n for locus in neighbour_list] for neighbour_list in neighbouring_locis_list]
        weight_list = [locus.value for locus in locis_list]
        graph = WeightedVerticesGraph(neighbour_list, weight_list)

        return graph


def hex_to_char_coord(x, y):

    hy = len(empty_hex.str_2d())
    hx = len(empty_hex.str_2d()[0])
    return x * hx, y * (hy - 1) // 2

print(Board({}, (20, 20)))
