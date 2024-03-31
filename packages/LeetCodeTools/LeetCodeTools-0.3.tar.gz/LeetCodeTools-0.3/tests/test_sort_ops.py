import unittest
from LeetCodeTools import bubble_sort
import random


class TestBubbleSort(unittest.TestCase):

    def test1(self):
        inp1 = [1, 2, 3, 4]
        out1 = [1, 2, 3, 4]
        out2 = [0, 1, 2, 3]
        self.assertEqual(bubble_sort(inp1), (out1, out2))

    def test2(self):
        inp1 = []
        out1 = []
        out2 = []
        self.assertEqual(bubble_sort(inp1), (out1, out2))

    def test3(self):
        inp1 = [1, None, -1]
        with self.assertRaises(TypeError):
            bubble_sort(inp1)

    def test4(self):
        inp1 = [-1.2, -5, 0, 5.5, 5]
        out1 = [-5, -1.2, 0, 5, 5.5]
        out2 = [1, 0, 2, 4, 3]
        self.assertEqual(bubble_sort(inp1), (out1, out2))

    def test5(self):
        inp1 = [1]
        out1 = [1]
        out2 = [0]
        self.assertEqual(bubble_sort(inp1), (out1, out2))

    def test6(self):
        inp1 = [random.randint(-50, 50) for _ in range(10)]
        out1, out2 = bubble_sort(inp1)
        out1_recreate = [inp1[i] for i in out2]
        self.assertEqual(out1, out1_recreate)


if __name__ == "__main__":
    unittest.main()
