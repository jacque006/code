"""
Author: Jacob Caban-Tomski
Finds the Nth largest int in a list of ints.
"""
import unittest
import heapq


"""
Implementation
"""

def get_largest_int(list_ints, n_largest_ele=1):
    """
    Returns the Nth largest int in the passed in list.
    Raises RuntimeError if passed in values do not meet expected type
    or range of values.
    """
    ele_idx = n_largest_ele - 1
    if ele_idx < 0:
        raise RuntimeError('n_largest_ele is less than 0')

    if not list_ints or len(list_ints) < 1:
        raise RuntimeError('list_ints is None or has no entries')

    if len(list_ints) < n_largest_ele:
        raise RuntimeError(
            'list_ints is too small or n_largest_ele is too large')

    # Max heap, get topmost elements.
    # Default python heap is a min heap, so use this utility instead.
    return heapq.nlargest(n_largest_ele, list_ints)[ele_idx]


"""
Tests
"""


class GetLargestIntTest(unittest.TestCase):

    def setUp(self):
        # Normally we'd use a parameterized test framework for this.
        self.test_data = [
            # test num, int list, n_largest_ele, expected result
            [0, [0], 1, 0],
            [1, [0, 1], 1, 1],
            [2, [0 ,1], 2, 0],
            [3, [3, 1, 2, 4], 1, 4],
            [4, [3, 1, 2, 4], 2, 3],
            [5, [3, 1, 2, 4], 3, 2],
            [6, [3, 1, 2, 4], 4, 1],
        ]

    def test_none(self):
        """
        Tests that an exception is raised when list is None.
        """
        with self.assertRaises(RuntimeError):
            get_largest_int(None)

    def test_small_element(self):
        """
        Tests that an exception is raised when n_largest_ele
        is less than 1.
        """
        with self.assertRaises(RuntimeError):
            get_largest_int([], 0)

    def test_empty_list(self):
        """
        Tests that an exception is raised when the passed in
        list of ints is empty.
        """
        with self.assertRaises(RuntimeError):
            get_largest_int([], 1)

    def test_list_entry_mismatch(self):
        """
        Tests that an exception is raised when n_largest_ele
        is larger than the list of ints.
        """
        with self.assertRaises(RuntimeError):
            get_largest_int([0], 2)

    def test_get_largest_int(self):
        """
        Tests that various valid scenarios return the correct value.
        """
        for entry in self.test_data:
            result = get_largest_int(entry[1], entry[2])
            self.assertEqual(
                entry[3], result,
                "Test {0} failed with result {1}"
                .format(entry[0], result))


if __name__ == '__main__':
    unittest.main()
