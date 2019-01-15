"""
helper classes for strategy
"""

from typing import Any, List


class Tree:
    """
    A bare-bones Tree ADT that identifies the root with the entire tree. Copied
    from CSC148H1S (2018) Lab 6. Modified for game strategy.py purposes
    """

    def __init__(self, value: object = None,
                 children: List['Tree'] = None) -> None:
        """
        Create Tree self with content value and 0 or more children

        >>> t = Tree(0)
        >>> [t.value, t.children, t.score] == [0, [], None]
        True
        """
        self.value = value
        # copy children if not None
        self.children = children[:] if children is not None else []
        self.score = None

    def __repr__(self) -> str:
        """
        Return representation of Tree (self) as string that
        can be evaluated into an equivalent Tree.

        >>> t1 = Tree(5)
        >>> t1
        Tree(5)
        >>> t2 = Tree(7, [t1])
        >>> t2
        Tree(7, [Tree(5)])
        """
        # Our __repr__ is recursive, because it can also be called
        # via repr...!
        return ('Tree({}, {})'.format(repr(self.value), repr(self.children))
                if self.children
                else 'Tree({})'.format(repr(self.value)))

    def __eq__(self, other: Any) -> bool:
        """
        Return whether this Tree is equivalent to other.
        >>> t1 = Tree(5)
        >>> t2 = Tree(5, [])
        >>> t1 == t2
        True
        >>> t3 = Tree(5, [t1])
        >>> t2 == t3
        False
        """
        return (type(self) is type(other) and
                self.value == other.value and
                self.children == other.children)

    def __str__(self, indent=0) -> str:
        """
        Produce a user-friendly string representation of Tree self,
        indenting each level as a visual clue.

        >>> t = Tree(17)
        >>> print(t)
        17
        >>> t1 = Tree(19, [t, Tree(23)])
        >>> print(t1)
        19
           17
           23
        >>> t3 = Tree(29, [Tree(31), t1])
        >>> print(t3)
        29
           31
           19
              17
              23
        """
        root_str = indent * " " + str(self.value)
        return '\n'.join([root_str] +
                         [c.__str__(indent + 3) for c in self.children])


class Stack:
    """
    Last-in, first-out (LIFO) stack. Copied from CSC148H1S (2018) Lab 3.
    Modified for game strategy.py purposes
    """

    def __init__(self) -> None:
        """
        Create a new, empty Stack self.
        """
        self._contents = []

    def add(self, obj: Any) -> None:
        """
        Add object obj to top of Stack self.

        >>> s = Stack()
        >>> s.add(7)
        """
        self._contents.append(obj)

    def remove(self) -> Any:
        """
        Remove and return top element of Stack self.

        Assume Stack self is not empty.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.remove()
        7
        """
        return self._contents.pop()

    def is_empty(self) -> bool:
        """
        Return whether Stack self is empty.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.add(7)
        >>> s.is_empty()
        False
        """
        return len(self._contents) == 0
