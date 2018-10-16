from puzzle import Puzzle

from mn_puzzle import is_valid_location


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent to other.

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool

        >>> grid1 = list()
        >>> grid1.append(["#", "*", "*", "#"])
        >>> grid1.append(["*", "*", "*", "*"])
        >>> grid1.append(["*", "*", ".", "*"])
        >>> grid1.append(["#", "*", "*", "#"])
        >>> gpsp1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> grid2 = list()
        >>> grid2.append(["#", "*", "*", "#"])
        >>> grid2.append(["*", "*", "*", "*"])
        >>> grid2.append(["*", "*", ".", "*"])
        >>> grid2.append(["#", "*", "*", "#"])
        >>> gpsp2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> gpsp1.__eq__(gpsp2)
        True
        >>> grid3 = list()
        >>> grid3.append(["*", "*", "*", "*"])
        >>> grid3.append(["*", "*", "*", "*"])
        >>> grid3.append(["*", "*", ".", "*"])
        >>> grid3.append(["*", "*", "*", "*"])
        >>> gpsp3 = GridPegSolitairePuzzle(grid3, {"*", ".", "#"})
        >>> gpsp1.__eq__(gpsp3)
        False
        """

        return (type(other) == type(self) and
                self._marker == other._marker and
                self._marker_set == other._marker_set)

    def __str__(self):
        """
        Return a human-readable string representation
        of GridPegSolitairePuzzle self.

        >>> grid = list()
        >>> grid.append(["#", "*", "*", "#"])
        >>> grid.append(["*", "*", "*", "*"])
        >>> grid.append(["*", "*", ".", "*"])
        >>> grid.append(["#", "*", "*", "#"])
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> print(gpsp)
        #**#
        ****
        **.*
        #**#
        """
        rows = []

        for row in self._marker:
            rows.append("".join(row))

        return "\n".join(rows)

    def extensions(self):
        """
        Return list of extensions of GridPegSolitairePuzzle self.
        Legal extensions consist of all configurations that can be reached
        by making a single jump from this configuration

        @type self: Puzzle
        @rtype: list[Puzzle]

        >>> grid = list()
        >>> grid.append(["#", "*", "*", "#"])
        >>> grid.append(["*", "*", "*", "*"])
        >>> grid.append(["*", "*", ".", "*"])
        >>> grid.append(["#", "*", "*", "#"])
        >>> gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> ext1 = list()
        >>> ext1.append(["#", "*", ".", "#"])
        >>> ext1.append(["*", "*", ".", "*"])
        >>> ext1.append(["*", "*", "*", "*"])
        >>> ext1.append(["#", "*", "*", "#"])
        >>> ext2 = list()
        >>> ext2.append(["#", "*", "*", "#"])
        >>> ext2.append(["*", "*", "*", "*"])
        >>> ext2.append([".", ".", "*", "*"])
        >>> ext2.append(["#", "*", "*", "#"])
        >>> extensions = gpsp.extensions()
        >>> L = list()
        >>> L.append(GridPegSolitairePuzzle(ext1, {"*", ".", "#"}))
        >>> L.append(GridPegSolitairePuzzle(ext2, {"*", ".", "#"}))
        >>> len(extensions) == len(L)
        True
        >>> all([s in L for s in extensions])
        True
        >>> all([s in extensions for s in L])
        True
        >>> no_ext = list()
        >>> no_ext.append(["#", ".", ".", "#"])
        >>> no_ext.append(["*", ".", "*", "."])
        >>> no_ext.append([".", ".", ".", "."])
        >>> no_ext.append(["#", ".", ".", "#"])
        >>> gps_no_ext = GridPegSolitairePuzzle(no_ext, {"*", ".", "#"})
        >>> extensions = gps_no_ext.extensions()
        >>> len(extensions) == 0
        True
        """

        def has_peg(location):
            # Pre-condition: row and column exist in two
            # dimensional array (list of lists)
            return self._marker[location[0]][location[1]] == "*"

        def jump(start, empty):

            max_rows, max_columns = len(self._marker), len(self._marker[0])

            #  copy two dimensional array (can also use copy, deepcopy)
            grid_c = [row[:] for row in self._marker]

            # calculate position of peg that will be jumped over and eliminated
            over = int((start[0] + empty[0])/2), int((start[1] + empty[1])/2)

            if is_valid_location(start, max_rows, max_columns) \
                    and has_peg(start) and has_peg(over):

                # perform peg jump into empty space
                grid_c[start[0]][start[1]] = "."
                grid_c[empty[0]][empty[1]] = "*"

                # eliminate peg that was jumped over
                grid_c[over[0]][over[1]] = "."

                # return valid extension
                return GridPegSolitairePuzzle(grid_c, self._marker_set)
            else:
                return None

        extensions = []

        # positions of all empty spaces .
        for item in find_all(self._marker, "."):

            row, col = item[0], item[1]

            # location of space in the grid
            space = (row, col)

            # Potential solutions: jump from two spaces above, jump from two
            # spaces bellow, jump from two spaces to the right, jump from
            # two spaces to the left
            potential_jumps = [(row-2, col), (row+2, col),
                               (row, col-2), (row, col+2)]

            # if jump from potential solution is legal return
            # valid extension otherwise None
            for sol in potential_jumps:
                gpsp = jump(sol, space)
                if gpsp is not None and gpsp not in extensions:
                    extensions.append(gpsp)

        return extensions

    def is_solved(self):
        """
        # A configuration is solved when there is exactly one "*" left

        @type self: Puzzle
        @rtype: bool

        >>> grid = list()
        >>> grid.append(["#", ".", ".", "#"])
        >>> grid.append([".", "*", ".", "."])
        >>> grid.append([".", ".", ".", "."])
        >>> grid.append(["#", ".", ".", "#"])
        >>> puzzle = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> puzzle.is_solved()
        True
        >>> grid = list()
        >>> grid.append(["#", ".", ".", "#"])
        >>> grid.append([".", "*", ".", "."])
        >>> grid.append(["*", ".", ".", "."])
        >>> grid.append(["#", ".", ".", "#"])
        >>> puzzle = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
        >>> puzzle.is_solved()
        False
        """
        # find positions of all pegs ("*")
        indices = find_all(self._marker, "*")
        return len(indices) == 1


def find_all(grid, elem):
    elements = []
    for row, item in enumerate(grid):
        indices = [i for i, x in enumerate(item) if x == elem]
        for column in indices:
            elements.append((row, column))

    return elements

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]

    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
