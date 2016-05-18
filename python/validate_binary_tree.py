"""
Author: Jake Caban-Tomski (jacque006)

Problem:
Write a function to check that a binary tree is a valid binary search tree.
That means for any node n:
  - All nodes to the left of n have values less than or equal to n
  - All nodes to the right of n have values greater than or equal to n

Solution:
 - Assumes Python 2.7.6 is installed.
 - Run with: python [file.py] -v

Notes:
 - Only works on integers.
 - More permutations could be covered by a parameterized test.
 - Chose to throw an exception rather than return a boolean for the valid
  checks to allow the search to break early if it finds something wrong
  rather than search the entire tree.
 - Ideally, this would be broken up into multiple files/modules/packages:
  - Models
  - Exceptions
  - CRUD functions
  - Print functions
  - Validity functions
  - Tests
 Left as is for readability, pastability, and to only go
 a little too far over-engineering the solution.
"""
import unittest
import logging

from collections import defaultdict
from sys import maxint


class ValidBinaryTreeTest(unittest.TestCase):
    """
    Test class for binary tree validity functions.
    """

    def setUp(self):
        # Build starter, valid tree.
        self.tree = BinaryTree()

        """
              10
           5       13
         3   6  11    15
        """
        # Order of insertition matters since our
        # tree operations do not balance the tree.
        insert_value_into_tree(self.tree, 10)
        insert_value_into_tree(self.tree, 5)
        insert_value_into_tree(self.tree, 13)
        insert_value_into_tree(self.tree, 3)
        insert_value_into_tree(self.tree, 6)
        insert_value_into_tree(self.tree, 11)
        insert_value_into_tree(self.tree, 15)

    def test_valid_tree(self):
        """
        Test that valid tree passes.
        """
        self.assertIsNone(validate_binary_tree(self.tree))

    def test_invalid_left_child(self):
        """
        Test that a tree with an invalid left child fails.
        Swap 12 for 5.
        """
        invalid_node = get_node_by_value_from_tree(self.tree, 5)
        invalid_node.value = 12

        self.assertRaises(InvalidBinaryTreeException, validate_binary_tree, self.tree)

    def test_invalid_right_child(self):
        """
        Test that a tree with an invalid right child fails.
        Swap 20 for 11.
        """
        invalid_node = get_node_by_value_from_tree(self.tree, 11)
        invalid_node.value = 20

        self.assertRaises(InvalidBinaryTreeException, validate_binary_tree, self.tree)

    def test_out_of_range_left_child(self):
        """
        Test that a tree with an out of range left child fails.
        Swap 14 for 6.
        """
        invalid_node = get_node_by_value_from_tree(self.tree, 6)
        invalid_node.value = 14

        self.assertRaises(InvalidBinaryTreeException, validate_binary_tree, self.tree)

    def test_out_of_range_right_child(self):
        """
        Test that a tree with an out of range right child fails.
        Swap 9 for 11.
        """
        invalid_node = get_node_by_value_from_tree(self.tree, 6)
        invalid_node.value = 14

        self.assertRaises(InvalidBinaryTreeException, validate_binary_tree, self.tree)

    def test_same_value_left_branch_left_child(self):
        """
        Test that a tree with a same value left child in left branches passes.
        Swap 5 for 3.
        """
        invalid_node = get_node_by_value_from_tree(self.tree, 3)
        invalid_node.value = 5

        self.assertIsNone(validate_binary_tree(self.tree))

    def test_same_value_left_branch_right_child(self):
        """
        Test that a tree with a same value right child in left branches passes.
        Swap 5 for 6.
        """
        invalid_node = get_node_by_value_from_tree(self.tree, 6)
        invalid_node.value = 5

        self.assertIsNone(validate_binary_tree(self.tree))

    def test_same_value_right_branch_left_child(self):
        """
        Test that a tree with a same value left child in right branches passes.
        Swap 13 for 11.
        """
        invalid_node = get_node_by_value_from_tree(self.tree, 11)
        invalid_node.value = 13

        self.assertIsNone(validate_binary_tree(self.tree))

    def test_same_value_right_branch_right_child(self):
        """
        Test that a tree with a same value right child in right branches passes.
        Swap 13 for 15.
        """
        invalid_node = get_node_by_value_from_tree(self.tree, 15)
        invalid_node.value = 13

        self.assertIsNone(validate_binary_tree(self.tree))


"""
Binary tree validity functions.
"""


def validate_binary_tree(tree):
    """
    Checks that the given tree is valid.

    Throws an InvalidBinaryTreeException if it is not.
    """
    
    _validate_tree(tree)
    
    _validate_node(tree.root, -maxint, maxint)


def _validate_tree(tree):
    if not tree or not tree.root or not tree.root.value:
        raise InvalidBinaryTreeException('Tree, root, or root value does not exist')

    
def _validate_node(node, lower_bound, upper_bound):
    # Return early if no node (empty left or right child).
    if not node:
        return;

    value = node.value
    # Check that the node falls within the defined bounds.
    if value > upper_bound or value < lower_bound:
        raise InvalidBinaryTreeException(
            _create_node_value_exception_message(value, lower_bound, upper_bound))

    # Check children nodes, changing bounds to new values.
    _validate_node(node.left, lower_bound, value)
    _validate_node(node.right, value, upper_bound)


def _create_node_value_exception_message(node_value, lower_bound, upper_bound):
    return '%s does not fall within valid range. ' \
        'Node value: %s, Lower bound: %s, Upper bound: %s' % \
        (node_value, node_value, lower_bound, upper_bound)


"""
Binary Tree Models
"""


class BinaryTree(object):
    """
    Reprents a binary tree of nodes.
    """
    def __init__(self):
        # Root node.
        self.root = None


class BinaryTreeNode(object):
    """
    Represents a node in a binary tree.
    """
    def __init__(self, value):
        # Node's value. Must be interger.
        self.value = value
        # Left child whose value will be less than or equal to this node.
        self.left = None
        # Left child whsoe value will be greater than or equal to this node.
        self.right = None


"""
Exceptions
"""


class InvalidBinaryTreeException(Exception):
    """
    Excpetion thrown if binary tree is not valid.
    """
    pass


class InvalidValueException(Exception):
    """
    Exception thrown if a node is attemped to be inserted with a non-integer value. 
    """
    pass


"""
Tree CRUD functions
"""


def get_node_by_value_from_tree(tree, value):
    """
    Returnd a node by integer value from the tree, or none if it does not exist.

    Note: If multiples of the same value exist, this will return the first node
    with that value that this finds.
    """
    # Data validation.
    try:
        _validate_tree(tree)
    except InvalidBinaryTreeException, e:
        logging.error('Tree is not valid: %s', e)
        return None

    if not value:
        logging.error('Value not provided')
        return None

    return _get_node_by_value(tree.root, value)


def _get_node_by_value(node, value):
    # Return early if we reach the end of a leaf.
    if not node:
        return None

    # Found node.
    if node.value == value:
        return node

    # Check left child
    left_node = _get_node_by_value(node.left, value)
    if left_node:
        return left_node

    # Check right child
    right_node = _get_node_by_value(node.right, value)
    if right_node:
        return right_node


def insert_value_into_tree(tree, value):
    """
    Inserts the provided interger value into the provided binary tree.
    """
    # Data validation.
    if not tree:
        logging.error('Tree not defined')
        return

    try:
        _validate_value(value)
    except InvalidValueException, e:
        logging.error('Value is not valid: %s', e)
        return

    # Set root if it does not exist.
    if not tree.root:
        tree.root = BinaryTreeNode(value)
        logging.debug('Tree root created with value %s', value)
    else:
        _insert_value_into_node(tree.root, value)


def _validate_value(value):
    if not value or not isinstance(value, int):
        raise InvalidValueException('Value does not exist or is not an interger')


def _insert_value_into_node(node, value):
    # Note: Inserts on left branch if value is equal to node value.
    if value <= node.value:
        if node.left:
            _insert_value_into_node(node.left, value)
        else:
            # Create node wrapping value if we hit a terminating point.
            node.left = BinaryTreeNode(value)
    else:
        if node.right:
            _insert_value_into_node(node.right, value)
        else:
            node.right = BinaryTreeNode(value)


"""
Debug print functions
"""


def print_tree(tree):
    """
    Prints out the provided binary tree in a simple depth format.
    Used mainly for debugging, not reccomended for user display.
    """
    node_dict = defaultdict(list)
    _node_to_dict(tree.root, 0, node_dict)
    print ' '
    for depth in node_dict:
        print _get_spaces_for_depth(depth, node_dict) + str(node_dict[depth])


def _node_to_dict(node, depth, node_dict):
    if not node:
        return;

    node_dict[depth].append(node.value)
    _node_to_dict(node.left, depth + 1, node_dict)
    _node_to_dict(node.right, depth + 1, node_dict)


def _get_spaces_for_depth(depth, node_dict):
    spaces = ''
    for i in range(len(node_dict) - depth):
        spaces += ' '
    return spaces


if __name__ == '__main__':
    unittest.main()
