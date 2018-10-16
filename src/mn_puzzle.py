from .puzzle import Puzzle
from .puzzle_tools import breadth_first_solve, depth_first_solve
from time import time
import doctest


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle | Any
        @rtype: bool

        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> mnp1 = MNPuzzle(start_grid, target_grid)
        >>> mnp2 = MNPuzzle(start_grid, target_grid)
        >>> mnp1.__eq__(mnp2)
        True
        >>> diff_start_grid = (("2", "*", "3"), ("1", "4", "5"))
        >>> mnp3 = MNPuzzle(diff_start_grid, target_grid)
        >>> mnp1.__eq__(mnp3)
        False
        """
        return (type(self) == type(other) and
                equal_grids(self.from_grid, other.from_grid) and
                equal_grids(self.to_grid, other.to_grid))

    def __str__(self):
        """
        Return a human-readable string representation of MNPuzzle self.

        @type self: MNPuzzle

        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> mnp1 = MNPuzzle(start_grid, target_grid)
        >>> print(mnp1)
        *23
        145
        """
        rows = []

        for row in self.from_grid:
            rows.append("".join(row))

        return "\n".join(rows)

    def extensions(self):
        """
        Return list of extensions of MNPuzzle self. Legal extensions are
        configurations that can be reached by swapping
        one symbol to the left, right, above, or below "*" with "*"

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]

        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> mnp = MNPuzzle(start_grid, target_grid)
        >>>
        >>> L1 = mnp.extensions()
        >>> ext_1 = (("2", "*", "3"), ("1", "4", "5"))
        >>> ext_2 = (("1", "2", "3"), ("*", "4", "5"))
        >>> L2 = [MNPuzzle(ext_1, target_grid), MNPuzzle(ext_2, target_grid)]
        >>> len(L1) == len(L2)
        True
        >>> all([s in L2 for s in L1])
        True
        >>> all([s in L1 for s in L2])
        True
        """

        def swap(empty, symbol):
            """

            Pre-condition: specified rows and columns for empty and symbol
            exist in two dimensional array (tuple of tuples)

            @type empty: tuple
            @type symbol: tuple
            @rtype: MNPuzzle
            """

            #  convert to list of lists since tuples are immutable
            grid = [list(i) for i in self.from_grid]

            # edit: swap empty place (*) and symbol
            grid[empty[0]][empty[1]] = grid[symbol[0]][symbol[1]]
            grid[symbol[0]][symbol[1]] = "*"

            # convert back to tuple of tuples
            new_from_grid = tuple(tuple(i) for i in grid)

            return MNPuzzle(new_from_grid, self.to_grid)

        # find emtpy location (only one empty space exists in MNPuzzle)
        empty = find_first(self.from_grid, "*")

        row, col = empty[0], empty[1]

        # candidate swap locations:  left, right, above, below
        candidates = [(row, col+1), (row, col-1), (row+1, col), (row-1, col)]

        valid_swap_locations = [c for c in candidates
                                if is_valid_location(c, self.n, self.m)]

        extensions = [swap(empty, symbol) for symbol in valid_swap_locations]

        return extensions

    def is_solved(self):
        """
        Return whether Puzzle self is solved. A configuration is solved
        when from_grid is the same as to_grid

        @type self: Puzzle
        @rtype: bool

        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> mnp = MNPuzzle(start_grid, target_grid)
        >>> mnp.is_solved()
        False
        >>> target_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> mnp = MNPuzzle(start_grid, target_grid)
        >>> mnp.is_solved()
        True
        """
        # all tuples in start and target grids have to be the same
        # for MN puzzle to be solved
        return equal_grids(self.from_grid, self.to_grid)


def find_first(grid, elem):
    """
    Return the position of the first elem in the grid, or None if not found
    @param tuple[tuple[str]] grid: grid
    @param [str] elem: element to be found in the grid
    @rtype: tuple(row, column)

    >>> grid = (("*", "2", "3"), ("1", "4", "5"))
    >>> find_first(grid, "*")
    (0, 0)
    >>> find_first(grid, "0") is None
    True
    """

    for row, t in enumerate(grid):
        if elem in t:
            column = t.index(elem)
            return row, column

    return None


def is_valid_location(location, rows, columns):
    """
    Return True if both row and column of this location
    are positioned within rowsxcolumns grid

    @type location: tuple(row,column)
    @type rows: number of rows
    @type columns: number of columns
    @rtype: bool
    >>> is_valid_location((3,4), 5, 6)
    True
    >>> is_valid_location((3,4), 4, 2)
    False
    >>> is_valid_location((-1,-1), 2, 2)
    False
    """
    valid_location = False

    if 0 <= location[0] < rows and 0 <= location[1] < columns:
        valid_location = True

    return valid_location


def equal_grids(grid1, grid2):
    """
    Return True if the grids are the same

    @param tuple[tuple[str]] grid1: first configuration
    @param tuple[tuple[str]] grid2: second configuration
    @rtype: bool

    >>> grid = (("*", "2", "3"), ("1", "4", "5"))
    >>> equal_grid = (("*", "2", "3"), ("1", "4", "5"))
    >>> diff_grid = (("1", "2", "3"), ("4", "5", "*"))
    >>> equal_grids(grid, equal_grid)
    True
    >>> equal_grids(grid, diff_grid)
    False
    """

    # all tuples in grid1 and grid2 have to be the same
    return all([a == b for a, b in zip(grid1, grid2)])

if __name__ == "__main__":
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
