"""
Some functions for working with puzzles
"""
from .puzzle import Puzzle
from collections import deque

from .sudoku_puzzle import SudokuPuzzle
from .mn_puzzle import MNPuzzle
from .grid_peg_solitaire_puzzle import GridPegSolitairePuzzle
from .word_ladder_puzzle import WordLadderPuzzle

# set higher recursion limit
# which is needed in PuzzleNode.__str__
# you may uncomment the next lines on a unix system such as CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode

    Test when initial configuration is a solution
    >>> sgrid = ["A", "B", "C", "D"]
    >>> sgrid += ["C", "D", "A", "B"]
    >>> sgrid += ["B", "A", "D", "C"]
    >>> sgrid += ["D", "C", "B", "A"]
    >>> s = SudokuPuzzle(4, sgrid, {"A", "B", "C", "D"})
    >>> pns = depth_first_solve(s)
    >>> pns is None
    False
    >>> pns.puzzle == s
    True

    Test no solution e.g. invalid configuration for sudoku
    fail_fast() implemented
    >>> ff_grid = ["A", "B", "D", "*"]
    >>> ff_grid += ["C", "D", "A", "B"]
    >>> ff_grid += ["B", "A", "D", "C"]
    >>> ff_grid += ["D", "C", "B", "A"]
    >>> ffs = SudokuPuzzle(4, ff_grid, {"A", "B", "C", "D"})
    >>> pnsff = depth_first_solve(ffs)
    >>> pnsff is None
    True

    Test no solution for peg solitaire(no consecutive pegs)
    fail_fast() not implemented
    >>> gps_grid = [[".", "*", ".", "*", "#"]]
    >>> gps = GridPegSolitairePuzzle(gps_grid, {"*", ".", "#"})
    >>> pngps = depth_first_solve(gps)
    >>> pngps is None
    True
    """

    root = PuzzleNode(puzzle, None, None)

    solution = dfs(root)
    if solution is not None:
        reconstruct_path(solution)
        return root
    else:
        return None


def dfs(start_node):
    """
    Return PuzzleNode(puzzle) if puzzle is solved otherwise return None.

    @type start_node: PuzzleNode
    @rtype: PuzzleNode

    Test that leaf node contains solution
    >>> start_grid = (("1", "2", "3"), ("4", "*", "5"))
    >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
    >>> mn_root_node = PuzzleNode(MNPuzzle(start_grid, target_grid), None, None)
    >>> sol = dfs(mn_root_node)
    >>> sol is None
    False
    >>> sol.puzzle == MNPuzzle(target_grid, target_grid)
    True
    """
    visited = set()
    stack = [start_node]

    while len(stack) > 0:
        puzzle_node = stack.pop()

        curr_puzzle = puzzle_node.puzzle

        curr_puzzle_str = str(curr_puzzle)
        if curr_puzzle_str in visited:
            continue

        visited.add(curr_puzzle_str)

        if curr_puzzle.is_solved():
            return puzzle_node

        if curr_puzzle.fail_fast():
            continue

        for ext in curr_puzzle.extensions():
            ext_node = PuzzleNode(ext, None, puzzle_node)
            if str(ext) not in visited:
                stack.append(ext_node)

    return None


def reconstruct_path(node):
    """
    Make double linked list. Currently this linked list points
    from child to parent. Add missing link: from parent to child.

    @type node: PuzzleNode
    """
    while node.parent is not None:
        node.parent.children = [node]
        node = node.parent


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode

    Test when initial configuration is a solution
     >>> dictionary = {"same", "some", "hello"}
    >>> wlp = WordLadderPuzzle("same", "same", dictionary )
    >>> pn = breadth_first_solve(wlp)
    >>> pn is None
    False
    >>> pn.puzzle == wlp
    True

    Test no solution for peg solitaire(no consecutive pegs)
    >>> gps_grid = [[".", "*", ".", "*", "#"]]
    >>> gps = GridPegSolitairePuzzle(gps_grid, {"*", ".", "#"})
    >>> pngps = breadth_first_solve(gps)
    >>> pngps is None
    True
    """

    root = PuzzleNode(puzzle, None, None)

    solution = bfs(root)

    if solution is not None:
        reconstruct_path(solution)
        return root
    else:
        return None


def bfs(start_node):
    """
    Return PuzzleNode(puzzle) if puzzle is solved otherwise return None.

    @type start_node: PuzzleNode
    @rtype: PuzzleNode

    Test that leaf node contains solution
    >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
    >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
    >>> mn_root_node = PuzzleNode(MNPuzzle(start_grid, target_grid), None, None)
    >>> sol = dfs(mn_root_node)
    >>> sol is None
    False
    >>> sol.puzzle == MNPuzzle(target_grid, target_grid)
    True
    """
    visited = set()
    queue = deque([start_node])

    while len(queue) > 0:
        puzzle_node = queue.pop()

        curr_puzzle = puzzle_node.puzzle

        curr_puzzle_str = str(curr_puzzle)
        if curr_puzzle_str in visited:
            continue

        visited.add(curr_puzzle_str)

        if curr_puzzle.is_solved():
            return puzzle_node

        if curr_puzzle.fail_fast():
            continue

        for ext in curr_puzzle.extensions():
            ext_node = PuzzleNode(ext, None, puzzle_node)
            if str(ext) not in visited:
                queue.appendleft(ext_node)

    return None


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether Puzzle self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
