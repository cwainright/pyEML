import metapype.eml.names as names
from metapype.model.node import Node
from metapype.model import metapype_io
from src.pyEML.error_classes import bcolors
from lxml import etree
from src.pyEML.lookups import LOOKUPS

class Eml():

    def __init__(self, filepath:str=None, INTERACTIVE:bool=True) -> None:
        """_summary_
        Attributes:
            src (str): Filepath and name for the source-xml that is parsed to an element tree.
            interactive (bool):Turns on status messages and overwrite detection. True is for interactive sessions. Show status messages, ask user for permission before overwriting. False is for automated scripting. Silence status messages and write metadata verbatim as scripted.
            orig (str): The original xml, if importing existing xml. None, if starting from scratch.
        Args:
            filepath (str, optional): _description_. Defaults to None.
            INTERACTIVE (bool, optional): _description_. Defaults to True.

        Raises:
            Exception: _description_
        """
        try:
            self.src = filepath
            self.interactive = INTERACTIVE
            self.orig = None
            if filepath is not None:
                assert filepath.endswith(('.xml', '.json')), print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.{bcolors.ENDC}\nYou provided "{bcolors.BOLD}{filepath}{bcolors.ENDC}".\n`{bcolors.BOLD}Eml{bcolors.ENDC}` instances can be created from xml or json.\nFilename should end in "{bcolors.BOLD}.xml{bcolors.ENDC}" or "{bcolors.BOLD}.json{bcolors.ENDC}".')
                fhand = open(filepath, "r")
                self.orig = fhand.read()
                fhand.close()
                if filepath.endswith('.xml'):
                    self.eml = metapype_io.from_xml(self.orig)
                    self.eml.add_attribute('system', 'metapype')
                    msg = 'xml'
                if filepath.endswith('.json'):
                    self.eml = metapype_io.from_json(self.orig)
                    self.eml.add_attribute('system', 'metapype')
                    msg = 'json'

                if self.orig is not None:
                    if self.interactive == True:
                        print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}Eml{bcolors.ENDC}` created from {msg} and interactive session started.')
                else:
                    raise Exception
            else:
                self.eml = Node(names.EML)
                self.eml.add_attribute('system', 'metapype')

                if self.interactive == True:
                    print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}Empty `{bcolors.BOLD}Eml{bcolors.ENDC}` created and interactive session started.')

        except TypeError as t:
            print(t)
        except ValueError as v:
            print(v)
        except AssertionError as a:
            print(a)
        except:
            print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}\n{bcolors.BOLD}`Eml`{bcolors.ENDC} not created.')

    def get_title(self):
        """Get the dataset's title node(s)
        """
        path = LOOKUPS['title']['path']
        nodes = self.eml.find_all_nodes_by_path(path=path)
        target_ids = []
        for target in nodes:
            target_ids.append(target.id)
        target_nodes = []
        for target in target_ids:
            target_nodes.append(self.eml.get_node_instance(target))
        for target in target_nodes:
            self.overview(target)

    def set_title(self, title:str):

        try:
            path = LOOKUPS['title']['path']
            parent = LOOKUPS['title']['parent']

            nodes = self.eml.find_all_nodes_by_path(path=path)
            parents = self.eml.find_all_nodes_by_path(path=parent)
            assert len(parents) == 1, print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}\nReturned multiple parent{bcolors.BOLD}`node`{bcolors.ENDC}s:\n')
            parent = parents[0]

            new_node = Node(path[-1])
            new_node.content = title

            if len(nodes) == 0:
                parent.add_child(new_node)
            else:
                self.delete_title()
                parent.add_child(new_node)
            if self.interactive == True:
                print('success')
                self.get_title()
        except AssertionError as a:
            print(a)


    def delete_title(self):
        """Delete the dataset's title node(s)

        Args:
            None

        Examples:
            myeml.delete_title()
        """
        try:
            path = LOOKUPS['title']['path']
            parent = LOOKUPS['title']['parent']

            values = self.eml.find_all_nodes_by_path(path=path)
            parent = self.eml.find_all_nodes_by_path(path=parent)
            assert len(parent) == 1, print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}\nReturned multiple parent{bcolors.BOLD}`node`{bcolors.ENDC}s:\n')
            parent = parent[0]
            for value in values:
                parent.remove_child(child=value)
                self.eml.delete_node_instance(id=value.id)

            # if self.interactive == True:
            #     self.show_overview()
        except AssertionError as a:
            print(a)

    
    def overview(self, node_xpath:str=None, depth:int=0):
        """Pretty-print up to three levels of xml tags and text

        This method pretty-prints to console the tag structure to a max depth of three levels of tags (depth = 0, 1, 2).
        This shows a user their element tree structure without details like deeply-nested nodes, namespaces, and attributes.
        `show_overview()` is good for simply checking an element tree's structure or confirming that a `set` or `delete` method worked.
        If you want the full-detail of your element tree, use `pretty_print()` or `save_xml()`.

        Args:
            node_xpath (str, optional): A relative xpath to the node from which you want to start the overview. Defaults to None.
            depth (int, optional): The depth to at which you want to start the overview. 0 starts the overview at the supplied `node_xpath`. 1 starts the overview at `node_xpath`'s children. -1 starts the overview at `node_xpath`'s parent. Defaults to 0.

        Examples:
            myeml.overview()
            myeml.overview('./dataset')
            myeml.overview('./additionalMetadata/metadata')
            myeml.overview('./additionalMetadata')
            myeml.pioverview('./dataset/keywordSet')
        """
        if node_xpath is None:
            node = self.eml
            self._show_overview(node=node, depth=depth)
        if isinstance(node_xpath, str):
            assert node_xpath.startswith('./'), print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}\n{bcolors.BOLD}`node_xpath`{bcolors.ENDC}, if supplied, must begin with "./"\n')
            node_xpath = node_xpath.replace('./', '')
            node = node_xpath.split('/')
            for n in node:
                n = 'names.' + n
            node = self.eml.find_all_nodes_by_path(node)
        
            for n in node:
                self._show_overview(node=n, depth=depth)
        elif isinstance(node_xpath, Node):
            self._show_overview(node=node_xpath, depth=depth)
    
    def _show_overview(self, node:Node, depth:int):
        """The recursive part of show_overview()

        Args:
            node (Node): The metapype.model.node.Node at which the overview should start. 
            depth (int): The depth to at which you want to start the overview. 0 starts the overview at the supplied `node_xpath`. 1 starts the overview at `node_xpath`'s children. -1 starts the overview at `node_xpath`'s parent. Defaults to 0.
        """
        if depth < 2:
            spaces = '    ' * depth
            if depth == 0:
                print(f'{spaces}<{node.name}>')
            if len(node.children) == 0:
                print(f'{spaces}    {node.content}')
            else:
                for child in node.children:
                    print(f'{spaces}    <{child.name}>')
                    self._show_overview(child, depth+1)
            print(f'{spaces}</{node.name}>')

    def save_xml(self, filename:str):
        """Save a metadata model to .xml

        Args:
            filename (str): The xml output's filename, ending with '.xml'
        """
        try:
            assert filename.endswith('.xml'), print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}\n{bcolors.BOLD}`filename`{bcolors.ENDC}, must end with ".xml"\n')
            myxml = metapype_io.to_xml(self.eml)
            root = etree.fromstring(myxml)
            tree = etree.ElementTree(root)
            tree.write(filename, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        except AssertionError as a:
            print(a)
    
    def pretty_print(self, node:Node=None):
        if node is None:
            myxml = metapype_io.to_xml(self.eml)
            root = etree.fromstring(myxml)
            print(etree.tostring(root, pretty_print=True).decode())
        else:
            myxml = metapype_io.to_xml(node)
            root = etree.fromstring(myxml)
            print(etree.tostring(root, pretty_print=True).decode())
        