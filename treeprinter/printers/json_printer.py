import collections
from treeprinter.printers.base import BaseTreePrinter


class JsonItem(object):
    def __init__(self, key_value_tuple):
        self.key, self.value = key_value_tuple

    @property
    def value_type(self):
        return type(self.value)


class JsonPrinter(BaseTreePrinter):
    def get_children(self, tree):
        if not isinstance(tree, JsonItem):
            tree = JsonItem(("", tree))
        if isinstance(tree.value, collections.Mapping):
            return [JsonItem(c) for c in tree.value.items()]
        elif isinstance(tree.value, collections.Sequence) and not isinstance(tree.value, str):
            return [JsonItem((c, None)) for c in tree.value]
        elif not isinstance(tree.value, type(None)):
            return [JsonItem(("{}".format(tree.value), None))]
        else:
            return []

    def get_text(self, tree):
        if not isinstance(tree, JsonItem):
            tree = JsonItem(("", tree))
        if isinstance(tree.value, collections.Mapping):
            return "{{{}}}".format(tree.key)
        elif isinstance(tree.value, collections.Sequence) and not isinstance(tree.value, str):
            return "[{}]".format(tree.key)
        else:
            return tree.key
