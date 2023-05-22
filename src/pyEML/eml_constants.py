
import metapype.eml.names as names
from metapype.model.node import Node
from src.pyEML.error_classes import AllBlanks

LOOKUPS = {
    'title': {
        'path': [
            names.DATASET,
            names.TITLE
        ],
        'parent': [
            names.DATASET
        ],
        'target': 'title',
        'values': {
            'title': None
            }
    },
    'creator': {
        'path': [
            names.DATASET,
            names.CREATOR
        ],
        'parent': [
            names.DATASET
        ],
        'target': 'creator'
    }
}

class EmlNode():
    def __init__(self) -> None:
        pass
    
    def show(self):
        self._show(node=self.node, depth=0)

    def _show(self, node:Node, depth:int):
        """The recursive part of show()

        Args:
            node (Node): The metapype.model.node.Node at which the overview should start. 
            depth (int): The depth to at which you want to start the overview. 0 starts the overview at the supplied `node_xpath`. 1 starts the overview at `node_xpath`'s children. -1 starts the overview at `node_xpath`'s parent. Defaults to 0.
        """
        if depth < 3:
            spaces = '    ' * depth
            if depth == 0:
                print(f'{spaces}<{node.name}>')
            if len(node.children) == 0:
                print(f'{spaces}    {node.content}')
            else:
                for child in node.children:
                    print(f'{spaces}    <{child.name}>')
                    self._show(child, depth+1)
            print(f'{spaces}</{node.name}>')

class Creator(EmlNode):
    def __init__(self, first:str=None, last:str=None, org:str=None, email:str=None) -> None:
        try:
            if all(v is None for v in [first, last, email, org]): raise AllBlanks
            self.node = Node('creator')
            self.attrs = {
                'first': first,
                'last': last,
                'org': org,
                'email': email
            }

            clean_attrs = {}
            for k,v in self.attrs.items():
                if v != None:
                    clean_attrs[k] = v

            if 'first' or 'last' in clean_attrs.keys():
                indiv_node = Node('individualName')
                self.node.add_child(indiv_node)
            if 'first' in clean_attrs.keys():
                first_node = Node('givenName')
                indiv_node.add_child(first_node)
                first_node.content = clean_attrs['first']
                del clean_attrs['first']
            if 'last' in clean_attrs.keys():
                last_node = Node('surName')
                indiv_node.add_child(last_node)
                last_node.content = clean_attrs['last']
                del clean_attrs['last']

            for k, v in clean_attrs:
                new_node = Node(k)
                new_node.content = v
                self.node.add_child(new_node)

        except AllBlanks as a:
            print(a.msg)
