import unittest

from aoc2020.task11.task11 import load, _interlink_neighboring_seats, Seat


class LobbyTest(unittest.TestCase):
    def test_full_flow(self):
        threshold = 5
        lobby = load("./test_input.txt", -1)
        self.assertEqual(10, len(lobby.plan))
        self.assertEqual(10, len(lobby.plan[0]))
        self.assertEqual(10, len(lobby.plan[-1]))

        self.assertEqual(
            """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""",
            str(lobby)
        )
        lobby._iteration(threshold)
        self.assertEqual(
            """#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##""",
            str(lobby)
        )
        lobby._iteration(threshold)
        self.assertEqual(
            """#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#""",
            str(lobby)
        )
        lobby._iteration(threshold)
        self.assertEqual(
            """#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#""",
            str(lobby)
        )
        lobby._iteration(threshold)
        self.assertEqual(
            """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#""",
            str(lobby)
        )
        lobby._iteration(threshold)
        self.assertEqual(
            """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#""",
            str(lobby)
        )
        lobby._iteration(threshold)
        self.assertEqual(
            """#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#""",
            str(lobby)
        )
        self.assertEqual(26, lobby.count_occupied())

    def test_linking_neighbors(self):
        s0 = Seat(Seat.FREE_SEAT)
        s1 = Seat(Seat.FREE_SEAT)
        s2 = Seat(Seat.FREE_SEAT)
        s3 = Seat(Seat.FREE_SEAT)
        s4 = Seat(Seat.FREE_SEAT)
        s5 = Seat(Seat.FREE_SEAT)
        seats = _interlink_neighboring_seats(
            plan=[
                [s0,                     s1,                     Seat(Seat.EMPTY_SPACE)],
                [s2,                     Seat(Seat.EMPTY_SPACE), Seat(Seat.EMPTY_SPACE)],
                [Seat(Seat.EMPTY_SPACE), s3,                     Seat(Seat.EMPTY_SPACE)],
                [s4,                     Seat(Seat.EMPTY_SPACE), s5]
            ],
            radius=-1
        )
        self.assertEqual(6, len(seats))
        self.assertEqual(2, len(seats[0].neighbors))
        self.assertTrue(s1 in s0.neighbors)
        self.assertTrue(s2 in s0.neighbors)
        self.assertEqual(3, len(seats[1].neighbors))
        self.assertTrue(s0 in s1.neighbors)
        self.assertTrue(s3 in s1.neighbors)
        self.assertTrue(s2 in s1.neighbors)
        self.assertEqual(4, len(seats[2].neighbors))
        self.assertTrue(s0 in s2.neighbors)
        self.assertTrue(s1 in s2.neighbors)
        self.assertTrue(s3 in s2.neighbors)
        self.assertTrue(s4 in s2.neighbors)
        self.assertEqual(4, len(seats[3].neighbors))
        self.assertTrue(s2 in s3.neighbors)
        self.assertTrue(s1 in s3.neighbors)
        self.assertTrue(s5 in s3.neighbors)
        self.assertTrue(s4 in s3.neighbors)
        self.assertEqual(3, len(seats[4].neighbors))
        self.assertTrue(s2 in s4.neighbors)
        self.assertTrue(s3 in s4.neighbors)
        self.assertTrue(s5 in s4.neighbors)
        self.assertEqual(2, len(seats[5].neighbors))
        self.assertTrue(s3 in s5.neighbors)
        self.assertTrue(s4 in s5.neighbors)


if __name__ == '__main__':
    unittest.main()
