Tree printer
============

This library provides a tree printer class for easy tree displaying

## Installation 
``` sh
$ pip install treeprinter
```

## Basic usage

### Printer instance
``` python
from treeprinter import TreePrinter

class Tree(object):
    def __init__(self, tag, children=None):
        self.children = children or []
        self.tag = tag

tree = Tree("animal", [
            Tree("cat"),
            Tree("dog", [Tree("chihuahua"), Tree("dalmatian")]),
            Tree("wolf")])

printer = TreePrinter('children', 'tag')
printer.pprint(tree)
```
```
             animal              
                |                
   ---------------------------   
  |             |             |  
 cat           dog          wolf 
                |                
           ----------            
          |          |           
      chihuahua  dalmatian       
```

### Printer decorator
You could also get the same result by decorating your class like so to implement the \_\_str\_\_ method
``` python
@TreePrinter('children', 'tag')
class Tree(object):
    def __init__(self, tag, children=None):
        self.children = children or []
        self.tag = tag

print(tree)
```


## Extensions
You can extend the library by implementing the base displayer
(see printers/json_printer.py)

``` python
from treeprinter import JsonPrinter

printer = JsonPrinter()
json = {
    "fruits": ["Apple", "Banana", "Pear"],
    "presidents": {
        "France": ["Sarkozy", "Hollande"],
        "USA": ["Trump", "Obama"]
    },
    "star": "Sun"
}
printer.pprint(json)
```

```
                                     {}                     
                                      |                     
                   --------------------------------------   
                  |                         |            |  
            {presidents}                [fruits]       star 
                  |                         |            |  
          ----------------           --------------     Sun 
         |                |         |       |      |        
     [France]           [USA]     Apple  Banana  Pear       
         |                |                                 
     ---------         ------                               
    |         |       |      |                              
 Sarkozy  Hollande  Trump  Obama                            
```