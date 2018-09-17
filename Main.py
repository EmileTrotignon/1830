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
from typing import List, Union, Dict, Optional, Callable
from graphlib.main import *
import ascii_hex as ah


def rotate(li, n):

    return li[n:] + li[:n]


def opposite_side(side: int) -> int:

    if side < 3:
        return side + 3
    else:
        return side - 3


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

    def paint_over(self, other: 'Str2D', start=(0, 0), ignore=' ', ignore2='_/\\') -> 'Str2D':

        x0, y0 = start

        for y, line in enumerate(other):

            for x, char in enumerate(line):

                if y + y0 < len(self) and x0 + x < len(self[y0 + y]) \
                        and char not in ignore and not(char in ignore2 and self[y0 + y][x0 + x] not in ignore):
                    self[y0 + y][x0 + x] = char

        return self


class Locus:

    pass


class Track(Locus):

    def __init__(self, end_list=None):

        self.n = -1
        self.end_list = [] if end_list is None else end_list
        self.value = 0

    def __repr__(self):

        return f'Track [|{str(self.end_list)}|]"'

    def connect(self, other_locus: Union['Track', 'City']):
        """ One way connection"""

        self.end_list.append(other_locus)

    def neighbouring_locii(self, entry='start'):
        """ Return the connected end objects, except for the entry"""

        if entry != 'start':
            final_list = copy(self.end_list)
            final_list.remove(entry)
            return final_list

        return self.end_list


class City(Locus):

    def __init__(self, value, name='no_name', token_list=None, max_token=1):

        #self.n = -1
        self.name = name
        self.value = value
        self.token_list = [] if token_list is None else token_list
        self.end_list = []
        self.max_token = max_token

    def __repr__(self):

        return f'city'

    def __str__(self):

        rep = f'City named {self.name}, worth {self.value} with those tokens : {self.token_list}'
        return rep

    def connect(self, track: Track):

        """ One way connection"""

        self.end_list.append(track)

    def add_token(self, company):

        if len(self.token_list) < self.max_token:
            self.token_list.append(company)
            company.token_list.append(self)
        else:
            print(f'city full, cant add token: max token = {self.max_token}, token placed = {len(self.token_list)}')

    def neighbouring_locii(self, entry='start'):

        """ Return the connected end objects, except for the entry"""

        if entry != 'start':
            final_list = copy(self.end_list)
            final_list.remove(entry)

            return final_list

        return self.end_list


def connect(locus0: Union['Track', 'City'], locus1: Union['Track', 'City']):

    locus0.connect(locus1)
    locus1.connect(locus0)


class Hexagon:

    def __init__(self, track_list: List[Track], city_list: List[City],
                 side_tuple: Tuple[List[Track]]=None,
                 upgradeable=True, ascii_repr=ah.UNKNOWN_TILE):

        self.track_list = track_list
        self.city_list = city_list
        self.side_tuple = side_tuple if side_tuple is not None else ([], [], [], [], [], [])
        self.upgradeable = upgradeable
        self._ascii_repr = Str2D(ascii_repr[1:])

    def __repr__(self) -> str:

        return f'Hexagon({self.track_list}, {self.city_list}, upgradeable={self.upgradeable},' \
               f' ascii_repr={self._ascii_repr}'

    def __str__(self) -> str:

        return str(self._ascii_repr)

    def __getitem__(self, key):

        return self.side_tuple[key]

    def rotated(self, n_rot: int) -> 'Hexagon':
        # rotate clockwise
        return Hexagon(self.track_list, self.city_list, rotate(self.side_tuple, n_rot))

    def str_2d(self) -> Str2D:

        return self._ascii_repr

    def add_track(self, connected:List[Union[Track, City, int]]):
        """add track to unplaced hexagon"""

        track = Track()
        for end in connected:
            if type(end) == int:
                self.side_tuple[end].append(track)
            else:
                connect(track, end)

        self.track_list.append(track)

    def connect(self, other: 'Hexagon', side: int):

        self_track_list = self[side]
        other_track_list = other[opposite_side(side)]
        for self_track in self_track_list:
            for other_track in other_track_list:
                connect(self_track, other_track)

    def add_city(self, value, token_list=None, name='no_name', max_token=1):

        self.city_list.append(City(value, token_list=token_list, name=name, max_token=max_token))


empty_hex = Hexagon([], [], ascii_repr=ah.EMPTY_TILE)


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

    def __getitem__(self, key: Tuple[int, int]):

        return self.hex_dic[key]

    def get_neighbours_coors(self, hex_coor: Tuple[int, int]) -> Tuple:

        x = hex_coor[0]
        y = hex_coor[1]
        return (x, y - 2), (x + 1, y - 1), (x + 1, y + 1), (x, y + 2), (x - 1, y - 1), (x - 1, y + 1)

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

        for x, y in self.hex_dic:

            self.ascii_repr.paint_over(self.hex_dic[x, y].str_2d(), start=(x * hx, y * (hy - 1) // 2))

        return self.ascii_repr

    def upgrade_hex(self, x: int, y: int, new_hex: Callable[[], Hexagon], check_rules=True):

        old_hex = self.hex_dic[(x, y)]
        if (not check_rules) or old_hex.upgradeable:

            self.hex_dic[(x, y)] = new_hex()

            for side, neighbours_coors in enumerate(self.get_neighbours_coors((x, y))):

                try:

                    neighbour = self.hex_dic[neighbours_coors]
                    self.hex_dic[(x, y)].connect(neighbour, side)
                except KeyError:
                    pass

            self.gen_ascii_repr()
            return True
        return False

    def add_company(self, company: Company):

        """Floats a new company"""

        self.company_dic[company.name] = company

    def generate_graph(self, company=None) -> WeightedVerticesGraph:
        locii_list = sum((self.hex_dic[coor].track_list + self.hex_dic[coor].city_list for coor in self.hex_dic), [])

        i = 0
        for locus in locii_list:
            locus.n = i
            i += 1

        neighbouring_locii_list = [locus.neighbouring_locii() for locus in locii_list]

        if company is not None:  # Check tokens

            """for k, locus in enumerate(locii_list):

                if type(locus) == City and len(locus.token_list) >= locus.max_token and company not in locus.token_list:
                    neighbouring_locii_list[k] = []"""

        neighbour_list = [list(set([locus.n for locus in neighbour_list])) for neighbour_list in neighbouring_locii_list]
        weight_list = [locus.value for locus in locii_list]
        #g = neighbour_list[1000000000000]
        graph = WeightedVerticesGraph(neighbour_list, weight_list)

        return graph


def hex_to_char_coord(x, y):

    hy = len(empty_hex.str_2d())
    hx = len(empty_hex.str_2d()[0])
    return x * hx, y * (hy - 1) // 2
