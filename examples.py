from treeprinter import TreePrinter, JsonPrinter, Alignment
from treeprinter.utils import pad_2d

@TreePrinter('children', 'tag')
class Tree():
    def __init__(self, tag, children=None):
        self.children = children or []
        self.tag = tag

if __name__ == "__main__":
    print(Tree("animal", [
            Tree("cat"),
            Tree("dog", [Tree("chihuahua"), Tree("dalmatian")]),
            Tree("wolf")]))

    printer = JsonPrinter(alignment=Alignment.END)
    json = {
        "fruits": ["Apple", "Banana", "Pear"],
        "presidents": {
            "France": ["Sarkozy", "Hollande"],
            "USA": ["Trump", "Obama"]
        },
        "star": "sun"
    }
    printer.pprint(json)