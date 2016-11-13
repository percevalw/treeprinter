from treeprinter.printers.base import BaseTreePrinter


class TreePrinter(BaseTreePrinter):
    def __init__(self, children_attr, text_attr):
        super(TreePrinter, self).__init__()
        self.children_attr = children_attr
        self.text_attr = text_attr

    def get_children(self, tree):
        if callable(self.children_attr):
            return self.children_attr(tree)
        children = getattr(tree, self.children_attr)
        if callable(children):
            return children()
        return children

    def get_text(self, tree):
        if callable(self.text_attr):
            return self.text_attr(tree)
        text = getattr(tree, self.text_attr)
        if callable(text):
            return text()
        return text


