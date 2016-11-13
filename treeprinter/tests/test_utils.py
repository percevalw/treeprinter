from unittest import TestCase
from treeprinter.utils import pad_1d, pad_2d, Alignment


class TestUtils(TestCase):
    def test_pad_1d_start(self):
        value = pad_1d(element="val", pad=" ", size=8, padding=(2, 2), margin=(0, 0), direction=Alignment.START)
        self.assertEqual(value, "  val   ")

    def test_pad_1d_end(self):
        value = pad_1d(element="val", pad=" ", size=8, padding=(2, 2), margin=(0, 0), direction=Alignment.END)
        self.assertEqual(value, "   val  ")

    def test_pad_1d_margin(self):
        value = pad_1d(element="val", pad=" ", size=8, padding=(3, 1), margin=(1, 0), direction=Alignment.START)
        self.assertEqual(value, "    val  ")

    def test_pad_1d_padding(self):
        value = pad_1d(element="valeur", pad=" ", size=8, padding=(3, 0), margin=(0, 0), direction=Alignment.START)
        self.assertEqual(value, "   valeur")

    def test_pad_2d_x(self):
        value = pad_2d(element=["this",
                                "cat",
                                "eats"],
                       pad=" ", size_x=8, padding_x=(1, 1), margin_x=(2, 2), dir_x=Alignment.END)
        self.assertEqual(value,
                         ['     this   ',
                          '      cat   ',
                          '     eats   '])

    def test_pad_2d_y(self):
        value = pad_2d(element=["this",
                                "cat",
                                "eats"],
                       pad=" ", size_y=6, padding_y=(2, 0), margin_y=(1, 1), dir_y=Alignment.START)
        self.assertEqual(value,
                         ['    ',
                          '    ',
                          '    ',
                          'this',
                          'cat ',
                          'eats',
                          '    ',
                          '    '])

# def test_pad_2d(self):
#        self.fail()
