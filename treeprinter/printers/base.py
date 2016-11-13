import abc
from treeprinter.utils import pad_1d, pad_2d, merge_h, Alignment


class TreeTextBlock(object):
    def __init__(self, lines, anchor=None):
        self.lines = lines
        self.anchor = anchor if anchor is not None else int(len(self.lines[0]) / 2)

    @property
    def after_anchor(self):
        return len(self.lines[0]) - self.anchor - 1

    @property
    def before_anchor(self):
        return self.anchor

    @property
    def width(self):
        return len(self.lines[0])

    @property
    def height(self):
        return len(self.lines)

    def __str__(self):
        return '\n'.join(self.lines)

    def __repr__(self):
        return '\n'.join(self.lines)

    @staticmethod
    def merge_h(*blocks, anchor_merge_dir=Alignment.CENTER, func=None):
        """
        Merges multiple anchored text blocks horizontally, computing the new anchor either either aligned
         to the left, the right or the center of all the blocks
        :param blocks: The blocks to merge
        :type blocks: list of TreeTextBlock
        :param anchor_merge_dir: The method to compute the new block anchor
        :type anchor_merge_dir: Alignment
        :param func: A function to apply to each block after merging depending on its position in the list
        :type func: function
        :return: The new block
        :rtype: TreeTextBlock
        """
        if func is not None:
            blocks = [func(b, i, len(blocks)) for i, b in enumerate(blocks)]
        if anchor_merge_dir == Alignment.START:
            new_anchor = blocks[0].anchor
        elif anchor_merge_dir == Alignment.END:
            new_anchor = sum(b.width for b in blocks) - blocks[-1].after_anchor - 1
        else:
            new_anchor = int((sum(b.width for b in blocks)
                              - blocks[0].before_anchor
                              - blocks[-1].after_anchor) / 2) + blocks[0].before_anchor
        return TreeTextBlock(merge_h(*(b.lines for b in blocks), dir_y=Alignment.START), new_anchor)

    @staticmethod
    def merge_v(*blocks, func=None):
        """
        Merges multiple anchored text blocks horizontally keeping their anchor aligned
        :param blocks: The blocks to merge
        :type blocks: list of TreeTextBlock
        :param func: A function to apply to each block after merging depending on its position in the list
        :type func: function
        :return: The new block
        :rtype: TreeTextBlock
        """

        if func is not None:
            blocks = [func(b, i, len(blocks)) for i, b in enumerate(blocks)]
        max_width = max([max([len(l) for l in b.lines]) for b in blocks])
        max_anchor = max([b.anchor for b in blocks])
        new_size = max_width + max(max(0, (max_anchor - b.anchor) - (max_width - b.width)) for b in blocks)
        padded_blocks = [pad_2d(b.lines, size_x=new_size, padding_x=(max_anchor - b.anchor, 0), dir_x=Alignment.START)
                         for b in blocks]
        return TreeTextBlock([l for p in padded_blocks for l in p], max_anchor)


class BaseTreePrinter(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, alignment=Alignment.CENTER):
        self.alignment = alignment

    @abc.abstractmethod
    def get_children(self, tree):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_text(self, tree):
        raise NotImplementedError()

    def to_tree_text_block(self, tree):
        """

        :param tree: The tree to convert to a TreeTextBlock
        :type tree: T
        :return: The newly created TreeTextBlock
        """

        def decorate_top(b, index, total):
            v_line = pad_1d('|', ' ', b.width, padding=(b.anchor, 0), direction=Alignment.START)
            if index == 0:
                h_line = pad_1d('-' * b.after_anchor, ' ', b.width, direction=Alignment.END)
            elif index == total - 1:
                h_line = pad_1d('-' * b.before_anchor, ' ', b.width, direction=Alignment.START)
            else:
                h_line = '-' * b.width
            return TreeTextBlock([h_line, v_line] + b.lines, b.anchor)

        text = self.get_text(tree)
        if isinstance(text, str):
            text = text.split('\n')
        text_block = TreeTextBlock(pad_2d(text, margin_x=(1, 1)))

        children = self.get_children(tree)

        if len(children) == 0:
            return text_block
        else:
            mid_block = TreeTextBlock(['|'])

            if len(children) == 1:
                bottom_block = self.to_tree_text_block(children[0])
            else:
                bottom_block = TreeTextBlock.merge_h(*[self.to_tree_text_block(c) for c in children],
                                                     anchor_merge_dir=self.alignment, func=decorate_top)
            t = TreeTextBlock.merge_v(text_block,
                                      mid_block,
                                      bottom_block)
        return t

    def pformat(self, tree):
        """
        Converts a tree to a string
        :param tree: The tree to convert to a string
        :return: str
        """
        return str(self.to_tree_text_block(tree))

    def pprint(self, tree):
        """
        Prints a tree
        :param tree: The tree to print
        """
        print(self.pformat(tree))

    def __call__(self, cls):
        """
        Decorates a class by inserting the __str__ method in its method definitions
        to format using a TreePrinter each time an instance is being converted to a str
        :param cls: The class to decorate
        :return: The new class
        """
        cls_dict = dict(cls.__dict__)

        def wrap_str(w_self):
            return self.pformat(w_self)

        cls_dict['__repr__'] = wrap_str
        return type(cls.__name__, cls.__bases__ if hasattr(cls, "__bases__") else (), cls_dict)
