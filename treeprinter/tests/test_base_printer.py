from unittest import TestCase
from treeprinter.printers.base import TreeTextBlock
from treeprinter.utils import Alignment


class TestTreeTextBlock(TestCase):
    def setUp(self):
        self.lines1 = [
            "The cat has      ",
            "eaten all of the ",
            "spaghetti        "
        ]
        self.lines2 = [
            "The dog lives   ",
            "in a tiny house "
        ]
        self.ttb1 = TreeTextBlock(lines=self.lines1, anchor=2)
        self.ttb2 = TreeTextBlock(lines=self.lines2, anchor=5)

    def test_properties(self):
        self.assertEqual(self.ttb1.before_anchor, 2)
        self.assertEqual(self.ttb1.after_anchor, 14)
        self.assertEqual(self.ttb1.height, 3)
        self.assertEqual(self.ttb1.width, 17)

    def test_merge_h_center(self):
        new_ttb = TreeTextBlock.merge_h(self.ttb1, self.ttb2, anchor_merge_dir=Alignment.CENTER)
        self.assertListEqual(new_ttb.lines, [
            "The cat has      The dog lives   ",
            "eaten all of the in a tiny house ",
            "spaghetti                        "
        ])

        self.assertEqual(new_ttb.anchor, 12)

    def test_merge_h_start(self):
        new_ttb = TreeTextBlock.merge_h(self.ttb1, self.ttb2, anchor_merge_dir=Alignment.START)
        self.assertEqual(new_ttb.anchor, 2)

    def test_merge_v(self):
        new_ttb = TreeTextBlock.merge_v(self.ttb1, self.ttb2)
        self.assertListEqual(new_ttb.lines, [
             '   The cat has      ',
             '   eaten all of the ',
             '   spaghetti        ',
             'The dog lives       ',
             'in a tiny house     '])
        self.assertEqual(new_ttb.anchor, 5)
