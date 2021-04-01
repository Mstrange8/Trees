"""
Project: Project 5 Trees
Author:  Matthew Strange
Course:  CS 2420
Date:  03/31/2021

Description: Program that implements a binary search tree that uses
around-the-world-in-80-days-3 as an input file.

Lessons Learned: How to create and manipulate a binary search tree.

"""
from pathlib import Path
from string import whitespace, punctuation
from bst import BST


def Pair(letter, count=1):
    return '({})'.format(letter)


def make_tree():
    """ A helper function to build the tree.
    
    The test code depends on this function being available from main.
    :param: None
    :returns: A binary search tree
    """
    bst = BST()
    _set = set()
    set_add = _set.add
    with open('around-the-world-in-80-days-3.txt', 'r') as f:
        _list = []
        for line in f.readlines():
            _list.append(line.strip())
        _list = ''.join(_list)
        punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~`'''
        for char in _list:
            if char in punc:
                _list = _list.replace(char, "")
        _set = [x for x in _list if not (x in _set or set_add(x))]
        for letter in _set:
            bst.add(Pair(letter))
    return bst


def main():
    bst = BST()
    bst.add(3)
    bst.add(7)
    bst.add(1)
    bst.inorder()


if __name__ == "__main__":
    main()
