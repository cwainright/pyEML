"""A pyEML source module that contains node lookup values and associated class definitions"""
import metapype.eml.names as names
from metapype.model.node import Node
from metapype.model import metapype_io
from src.pyEML.error_classes import AllBlanks
from types import MethodType
from lxml import etree

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

class EmlNode(Node):
    """An abstraction of a node in an EML document

    Inherits:
        Node (cls): metapype.model.node.Node

    This is the parent class to individual types of Eml Nodes (e.g., creators, keywords) and is essentially a placeholder for methods that apply to any EmlNode.
    """
    def __init__(self):
        pass
    
    def __repr__(self) -> str:
        repr = self._show()
        return repr
        
    def _show(self, mystr:str='', depth:int=0):
        if depth < 3:
            spaces = '    ' * depth
            if len(self.children) == 0:
                mystr += f'{spaces}<{self.name}>{self.content}</{self.name}>'
                return mystr
            else:
                mystr += f'{spaces}<{self.name}>'
                for child in self.children:
                    self.show(child, depth+1)
                mystr += f'{spaces}</{self.name}>'
    
    def show(self, depth:int=0):
        """Recursive pretty-printing of nodes

        Args:
            node (src.pyEML.eml_constants.EmlNode): The Eml node at which the recursion should start. 
            depth (int): The depth to at which you want to start the overview. 0 starts the overview at the supplied `EmlNode`. 1 starts the overview at `node`'s children. -1 starts the overview at `node`'s parent. Defaults to 0.
        """
        if depth < 3:
            spaces = '    ' * depth
            if len(self.children) == 0:
                print(f'{spaces}<{self.name}>{self.content}</{self.name}>')
            else:
                print(f'{spaces}<{self.name}>')
                for child in self.children:
                    self.show(child, depth+1)
                print(f'{spaces}</{self.name}>')

# this assigns the method to the class definition
# EmlNode.show = MethodType(show, EmlNode)

class EmlNodeSet(list):
    def __init__(self, list_of_nodes:list):
        """A list of EmlNode instances

        An instance class `EmlNodeSet` is a list of `src.pyEML.eml_constants.EmlNode` instances. This class extends Python's base list class.

        Inherits:
            list (cls): Python's base list class.

        Args:
            list_of_nodes (list): A list of src.pyEML.eml_constants.EmlNode instances
        """
        super().__init__(list_of_nodes)

    def __repr__(self) -> str:
        repr = ''
        for i in self:
            repr += i._show()
        return repr

    
    def show(self, depth:int=0):
        for n in self:
            n.show()
    
    # def show(self):
    #     # self._show(node=self.node, depth=0)
    #     for _ in self:
    #         myxml = metapype_io.to_xml(_)
    #         root = etree.fromstring(myxml)
    #         print(etree.tostring(root, pretty_print=True).decode())

class Creator(EmlNode):
    """Abstraction of EML dataset.creator node

    Inherits:
        EmlNode (cls): Parent class for Eml Nodes.
    """
    def __init__(self, first:str=None, last:str=None, org:str=None, email:str=None):
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
