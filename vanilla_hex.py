from Main import *
import ascii_hex as ah

empty = Hexagon([], [], ascii_repr=ah.EMPTY_TILE)

"""A1 = Hexagon([], [], ascii_repr=ah.A1)
A1.add_track(0, 3)

A2 = Hexagon([], [], ascii_repr=ah.A2)
A2.add_track(3, 5)

A3 = Hexagon([], [], ascii_repr=ah.A3)
A3.add_track(3, 4)

A4 = Hexagon([], [], ascii_repr=ah.A4)
A4.add_city(10, max_token=0)
A4.add_track(0, [A4.city_list[0]])
A4.add_track([A4.city_list[0]], 3)

A5 = Hexagon([], [], ascii_repr=ah.A5)
A5.add_city(10, max_token=0)
A5.add_track(5, [A5.city_list[0]])
A5.add_track([A5.city_list[0]], 3)

A6 = Hexagon([], [], ascii_repr=ah.A6)
A6.add_city(10, max_token=0)
A6.add_track(4, [A6.city_list[0]])
A6.add_track([A6.city_list[0]], 3)"""


def a7():

    nh = Hexagon([], [], ascii_repr=ah.A7)
    nh.add_city(20, max_token=1)
    nh.add_track([nh.city_list[0], 0])
    nh.add_track([nh.city_list[0], 3])
    return nh

"""A8 = Hexagon([], [], ascii_repr=ah.A8)
A9 = Hexagon([], [], ascii_repr=ah.A9)
A10 = Hexagon([], [], ascii_repr=ah.A10)
A11 = Hexagon([], [], ascii_repr=ah.A11)
A12 = Hexagon([], [], ascii_repr=ah.A12)
A13 = Hexagon([], [], ascii_repr=ah.A13)
A14 = Hexagon([], [], ascii_repr=ah.A14)

bb1 = Hexagon([], [], ascii_repr=ah.bb1)
bb5 = Hexagon([], [], ascii_repr=ah.bb5)"""


board = Board({}, (5, 5))
board.upgrade_hex(0, 0, a7)
board.upgrade_hex(0, 2, a7)
board.upgrade_hex(0, 4, a7)
company = Company('company', [], [3, 2], n_token=2)
board[(0, 0)].city_list[0].add_token(company)
board[(0, 4)].city_list[0].add_token(company)

print(board)
best_path = company.run_trains(board)
print(sum(len(path) for path in best_path))

