from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    DATASET_DIRECTORY = "/Users/sashaobucina/github/PuzzleSolver/datasets/"
    WORD_FILE_NAME = "words.txt"

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __eq__(self, other):
        """
        Return whether WordLadderPuzzle self is equivalent to other.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle | Any
        @rtype: bool

        >>> wlp1 = WordLadderPuzzle("start", "end", {'hello', 'there'})
        >>> wlp2 = WordLadderPuzzle("start", "end", {'hello', 'there'})
        >>> wlp1.__eq__(wlp2)
        True
        >>> wlp3 = WordLadderPuzzle("diff", "end", {'hello', 'there'})
        >>> wlp1.__eq__(wlp3)
        False
        >>> wlp4 = WordLadderPuzzle("start", "diff", {'hello', 'there'})
        >>> wlp1.__eq__(wlp4)
        False
        >>> wlp5 = WordLadderPuzzle("start", "end", {'hello', 'there', 'extra'})
        >>> wlp1.__eq__(wlp5)
        False
        """
        return (type(other) == type(self) and
                self._from_word == other._from_word and
                self._to_word == other._to_word and
                self._word_set == other._word_set)

    def __str__(self):
        """
        Return a human-readable string representation of WordLadderPuzzle self.

        >>> wlp1 = WordLadderPuzzle("start", "end", {'hello', 'there'})
        >>> print(wlp1)
        start -> end
        """
        return self._from_word + " -> " + self._to_word

    def extensions(self):
        """
        Return list of extensions of WordLadderPuzzle self. Legal extensions
        are WordPadderPuzzles that have a from_word that ca be reached
        from this one by changing a single letter to one of those in self._chars

        @type self: WordLadderPuzzle
        @rtype: list[Puzzle]

        >>> dictionary = {"same", "some", "hello", "tame", "sane","all", "samé"}
        >>> wlp = WordLadderPuzzle("same", "cost", dictionary )
        >>> extensions = list(wlp.extensions())
        >>> L = [WordLadderPuzzle("some", "cost", dictionary)]
        >>> L.append(WordLadderPuzzle("tame", "cost", dictionary))
        >>> L.append(WordLadderPuzzle("sane", "cost", dictionary ))
        >>> len(extensions) == len(L)
        True
        >>> all([s in L for s in extensions])
        True
        >>> all([s in extensions for s in L])
        True
        """
        from_word, to_word, ws = self._from_word, self._to_word, self._word_set
        legal = set()
        for i in range(len(from_word)):
            for d in self._chars:
                new = from_word[:i] + d + from_word[i+1:]
                if new != from_word and new in ws and new not in legal:
                    legal.add(new)

        extensions = [WordLadderPuzzle(word, to_word, ws) for word in legal]

        return extensions

    def is_solved(self):
        """
        This WordLadderPuzzle is solved when _from_word
        is the same as _to_word

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> dictionary={"same", "some", "hello", "tame", "sane","tata", "samé"}
        >>> wlp = WordLadderPuzzle("cost", "cost", dictionary )
        >>> wlp.is_solved()
        True
        >>> wlp2 = WordLadderPuzzle("most", "cost", dictionary )
        >>> wlp2.is_solved()
        False
        """
        return self._from_word == self._to_word


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open(WordLadderPuzzle.DATASET_DIRECTORY + WordLadderPuzzle.WORD_FILE_NAME, "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("amer", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
