from unittest import TestCase
from treeprinter.printers.default_printer import TreePrinter


class Tree(object):
    def __init__(self, tag, children=None):
        self.children = children or []
        self.tag = tag


class TestDefaultPrinter(TestCase):
    def setUp(self):
        self.tree = \
            Tree("animal", [
                Tree("cat"),
                Tree("dog", [Tree("Doge"), Tree("Dalmatian")]),
                Tree("wolf")])

    def test_format(self):
        printer = TreePrinter(children_attr="children", text_attr="tag")
        self.assertEqual(printer.pformat(self.tree), (
             "           animal           " '\n'
             "              |             " '\n'
             "   ----------------------   " '\n'
             "  |         |            |  " '\n'
             " cat       dog         wolf " '\n'
             "            |               " '\n'
             "         -------            " '\n'
             "        |       |           " '\n'
             "      Doge  Dalmatian       "))

    def test_decorator(self):
        @TreePrinter('children', 'tag')
        class DecoratedTree(object):
            def __init__(self, tag, children):
                self.children = children
                self.tag = tag

        self.assertTrue(hasattr(DecoratedTree, '__str__'))
        tree = DecoratedTree("house", [DecoratedTree("roof", []), DecoratedTree("walls", [])])
        self.assertEqual(str(tree), (
            '    house    ' '\n'
            '      |      ' '\n'
            '    -----    ' '\n'
            '   |     |   ' '\n'
            ' roof  walls ')
        )

