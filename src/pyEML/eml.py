# import logging
# from metapype.eml.exceptions import MetapypeRuleError
import metapype.eml.names as names
# import metapype.eml.validate as validate
from metapype.model.node import Node
# from metapype.eml import export
from metapype.model import metapype_io
from src.pyEML.error_classes import bcolors, MissingNodeException
from lxml import etree
from src.pyEML.eml_constants import LOOKUPS, Creator, EmlNode, EmlNodeSet

def _nodeset(nodeset):
        """Ingest an `EmlNodeSet`, `EmlNode`, or `metapype.model.node.Node` instance and recursively changes it and all of its children to `EmlNode` instances

        Args:
            nodeset (EmlNodeSet): _description_
        """
        if isinstance(nodeset, EmlNodeSet):
            for node in nodeset:
                node.__class__ = EmlNode
                if len(node.children) !=0:
                    for child in node.children:
                        _nodeset(child)
        elif isinstance(nodeset, Node):
            nodeset.__class__ = EmlNode
            if len(nodeset.children) !=0:
                    for child in nodeset.children:
                        _nodeset(child)

class Eml():

    def __init__(self, filepath:str=None, INTERACTIVE:bool=True) -> None:
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
                    # self.eml = EmlNode(metapype_io.from_xml(self.orig))
                    # self.eml.add_attribute('system', 'metapype')
                if filepath.endswith('.json'):
                    self.eml = metapype_io.from_json(self.orig)
                    self.eml.add_attribute('system', 'metapype')

                if self.orig is not None:
                    if self.interactive == True:
                        print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}Eml{bcolors.ENDC}` created from xml file and interactive session started.')
                else:
                    raise Exception
                
                _nodeset(self.eml) # update the class of self.eml and all of its child nodes

                # Business logic: allow a user to edit sets of nodes.
                # e.g., a user may want to add a "creator" to their metadata.
                # The user doesn't mean that they want to add `Node('creator')`.
                # The user wants to add data to creator.individualName.givenName, creator.individualName.surName, creator.electronicMailAddress...
                # These 'sets of nodes' are abstracted to the `EmlNodeSet` class and stored in the Eml() instance.
                # EML data integrity rules for node sets are enforced on creation of `EmlNodeSet` sub-classes like `Creator()` and `Title()`.
                self.creators = self._get_node(path=LOOKUPS['creator']['path'], target=LOOKUPS['creator']['target'], pretty=False, quiet=True)
                self.creators = EmlNodeSet(self.creators)
                self.title = self._get_node(path=LOOKUPS['title']['path'], target=LOOKUPS['title']['target'], pretty=False, quiet=True)
                self.title = EmlNodeSet(self.title)
            else:
                self.eml = Node(names.EML)
                _nodeset(self.eml)
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
        """Get the dataset's title node(s)"""

        path = LOOKUPS['title']['path']
        target = LOOKUPS['title']['target']

        if self.interactive == True:
            pretty=True
            quiet=False
            self._get_node(path=path, target=target, pretty=pretty, quiet=quiet)
        else:
            pretty=False
            quiet=True
            node = self._get_node(path=path, target=target, pretty=pretty, quiet=quiet)
            if node: # only returns an object if pretty == False
                return node

    def set_title(self, title:str):
        """Set the dataset's title node

        Args:
            title (str): Value to assign as the metadata title.
        """
        try:
            path = LOOKUPS['title']['path']
            parent = LOOKUPS['title']['parent']
            target = LOOKUPS['title']['target']
            values = LOOKUPS['title']['values']
            
            assert title not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{title}". `{target}` cannot be blank.'
            assert len(title) >= 3, f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{title}". {bcolors.BOLD}`{target}`{bcolors.ENDC} must be at least three characters.'

            values['title'] = title
            self._set_node(path=path, parent=parent, values=values, target=target, append=False)

            # nodes = self.eml.find_all_nodes_by_path(path=path)
            # parents = self.eml.find_all_nodes_by_path(path=parent)
            # assert len(parents) == 1, print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}\nReturned multiple parent{bcolors.BOLD}`node`{bcolors.ENDC}s:\n')
            # parent = parents[0]

            # new_node = Node(path[-1])
            # new_node.content = title

        except AssertionError as a:
            print(a)

    def delete_title(self):
        """Delete the dataset's title node

        Args:
            None

        Examples:
            myeml.delete_title()
        """
        try:
            path = LOOKUPS['title']['path']
            parent = LOOKUPS['title']['parent']
            target = LOOKUPS['title']['target']

            if self.interactive == True:
                quiet = False
            else:
                quiet = True

            self._delete_node(path=path, parent=parent, target=target, quiet=quiet)
            
        except:
            print('error delete_title()') 

    def get_creator(self):
        path = LOOKUPS['creator']['path']
        target = LOOKUPS['creator']['target']

        if self.interactive == True:
            pretty=True
            quiet=False
            self._get_node(path=path, target=target, pretty=pretty, quiet=quiet)
        else:
            pretty=False
            quiet=True
            node = self._get_node(path=path, target=target, pretty=pretty, quiet=quiet)
            if node: # only returns an object if pretty == False
                return node

    def set_creator(self, *creators:Creator, append:bool=False):
        """Delete the dataset's creator node(s)

        Args:
            creators (src.pyEML.eml_constants.Creator): Arbitrary arg. Any number of `Creator` instances.
            append (bool, optional): True will append `creators` dictionary to existing creators records. False will replace existing creators records with `creators` dict. Defaults to False.
        """
        try:
            path = LOOKUPS['creator']['path']
            target = LOOKUPS['creator']['target']
            parent = LOOKUPS['creator']['parent']


            if self.interactive == True:
                quiet = False
            else:
                quiet = True
            if append == False:
                self.delete_creator()
            parents = self._get_node(self, path=parent, target=target, pretty=False, quiet=quiet)

            assert isinstance(parents, list), print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}\nParent nodes did not return list{bcolors.BOLD}`node`{bcolors.ENDC}s.\n')
            assert len(parents) == 1, print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}\nReturned multiple parent{bcolors.BOLD}`node`{bcolors.ENDC}s.\n')
            parent_node = parents[0]
            for _ in creators:
                parent_node.add_child(_)

        except:
            print('error set_creator()')

    def delete_creator(self):
        """Delete the dataset's creator node(s)

        Args:
            None

        Examples:
            myeml.delete_title()
        """
        try:
            path = LOOKUPS['creator']['path']
            parent = LOOKUPS['creator']['parent']
            target = LOOKUPS['creator']['target']
            
            if self.interactive == True:
                quiet = False
            else:
                quiet = True

            self._delete_node(path=path, parent=parent, target=target, quiet=quiet)
            
        except:
            print('error delete_creator()') 

    def show(self, node_xpath:str=None, depth:int=0):
        """Pretty-print up to three levels of xml tags and text

        This method pretty-prints to console the tag structure to a max depth of three levels of tags (depth = 0, 1, 2).
        This shows a user their element tree structure without details like deeply-nested nodes, namespaces, and attributes.
        `show()` is good for simply checking an element tree's structure or confirming that a `set` or `delete` method worked.
        If you want the full-detail of your element tree, use `pretty_print()` or `save_xml()`.

        Args:
            node_xpath (str, optional): A relative xpath to the node from which you want to start the overview. Defaults to None.
            depth (int, optional): The depth to at which you want to start the overview. 0 starts the overview at the supplied `node_xpath`. 1 starts the overview at `node_xpath`'s children. -1 starts the overview at `node_xpath`'s parent. Defaults to 0.

        Examples:
            myeml.show()
            myeml.show('./dataset')
            myeml.show('./additionalMetadata/metadata')
            myeml.show('./additionalMetadata')
            myeml.show('./dataset/keywordSet')
        """
        if node_xpath is None:
            node = self.eml
            self._show(node=node, depth=depth)
        if isinstance(node_xpath, str):
            assert node_xpath.startswith('./'), print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}\n{bcolors.BOLD}`node_xpath`{bcolors.ENDC}, if supplied, must begin with "./"\n')
            node_xpath = node_xpath.replace('./', '')
            node = node_xpath.split('/')
            for n in node:
                n = 'names.' + n
            node = self.eml.find_all_nodes_by_path(node)
        
            for n in node:
                self._show(node=n, depth=depth)
        elif isinstance(node_xpath, Node):
            self._show(node=node_xpath, depth=depth)
        elif isinstance(node_xpath, list):
            for n in node_xpath:
                self._show(node=n, depth=depth)
    
    def _show(self, node:Node, depth:int):
        """The recursive part of show()

        Args:
            node (:obj:`Node` or :obj:`list` of :obj:`Node`): The metapype.model.node.Node at which the overview should start. 
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

    def _set_node(self, path:list, parent:list, values:list, target:str, append:bool):
        """Set the values at a node

        Args:
            values (list): A list of dictionaries. Dict keys map to xml tag names. Dict values map to xml text.
        """
        try:
            nodes = self.eml.find_all_nodes_by_path(path=path)
            parents = self.eml.find_all_nodes_by_path(path=parent)
            assert len(parents) == 1, print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}\nReturned multiple parent{bcolors.BOLD}`node`{bcolors.ENDC}s.\n')
            
            if self.interactive == True:
                quiet = False
                pretty = True
            else:
                quiet = True
                pretty = False
            
            if append == False:
                if len(nodes) != 0:
                    self._delete_node(path=path, parent=parent, target=target, quiet=quiet)
            
            parent = parents[0]

            # write a recursive function to build nodes
            # need to re-work emld._serialize_nodes()
            for _ in range(0, len(values)):
                name = list(values.keys())[0]
                new_node = Node(name)
                new_node.content = values['title'] 
                parent.add_child(new_node)

            if self.interactive == True:
                print('success')
                self._get_node(path=path, target=target, pretty=pretty, quiet=quiet)
        except:
            pass

    def _delete_node(self, path:list, parent:list, target:str, quiet:bool):
        try:
            # find any existing nodes
            values = self.eml.find_all_nodes_by_path(path=path)

            if values is None or len(values) == 0: # if there's no node, raise exception
                raise MissingNodeException(target)
            else: # if there's a node, work through possible parent node cases
                parent = self.eml.find_all_nodes_by_path(path=parent) # collect parent nodes

                # case 1: there are many parent nodes
                # raise exception because our algo can't know which parent node to append to; this must be resolved via the LOOKUPS dict
                # should be impossible except when invalid xml exists or the LOOKUPS dict is wrong
                assert len(parent) < 2, print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}\nReturned multiple parent{bcolors.BOLD}`node`{bcolors.ENDC}s.\n Invalid EML xml causes this error.\nUse `myeml.validate()` to determine why your EML is invalid and for suggested fixes.')
                # case 2: there are no parent nodes
                # should be impossible except when invalid xml exists
                assert len(parent) > 0, print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}\nReturned zero parent{bcolors.BOLD}`node`{bcolors.ENDC}s.\n Invalid EML xml causes this error.\nUse `myeml.validate()` to determine why your EML is invalid and how to fix it.')
                # case 2: there's one parent node so we delete children (this is our base-case)
                # if quiet is True, silently delete nodes
                # else, ask permission to delete nodes
                if len(parent) == 1:
                    parent = parent[0]
                    if quiet == True:
                        for value in values:
                            parent.remove_child(child=value)
                            self.eml.delete_node_instance(id=value.id)
                    else:
                        if len(values) == 1:
                            print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nMetadata package contains one `{bcolors.BOLD}{target}{bcolors.ENDC}` node:')
                        if len(values) > 1:
                            print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nMetadata package contains {len(values)} `{bcolors.BOLD}{target}{bcolors.ENDC}` nodes:')
                        self._get_node(path=path, target=target, pretty=True, quiet=False)
                        overwrite = input(f'{bcolors.BOLD}Do you want to delete these node(s)?\n{bcolors.ENDC}("{bcolors.BOLD}y{bcolors.ENDC}" to delete, "{bcolors.BOLD}n{bcolors.ENDC}" to cancel.)\n\n')
                        print(f'User input: {overwrite}')
                        if overwrite.lower() == 'y':
                            for value in values:
                                parent.remove_child(child=value)
                                self.eml.delete_node_instance(id=value.id)
                            print(f'`{bcolors.BOLD}{target}{bcolors.ENDC}` deleted.')
                        else:
                            print(f'`{bcolors.BOLD}{target}{bcolors.ENDC}` deletion cancelled.')
                
                # algo needs to build parent nodes
                elif len(parent) == 0:
                    pass

        except MissingNodeException as e:
            if quiet == False:
                print(e.msg)

    def validate(self):
        """Validate that an EML object will render to valid EML xml

        This method should rely on:
        emlvp.validator.Validator
        """
        pass
    
    def _get_node(self, path:list, target:str, pretty:bool, quiet:bool):

        try:
            # collect all nodes at `path`
            nodes = self.eml.find_all_nodes_by_path(path=path)
            target_ids = []
            for target in nodes:
                target_ids.append(target.id)
            target_nodes = []
            for target in target_ids:
                target_nodes.append(self.eml.get_node_instance(target))
            
            # check that nodes were returned
            if len(target_nodes) == 0:
                raise MissingNodeException(target)
            else:
                if pretty == True:
                    node_xpath = './' + '/'.join(path) # build xpath string from `path`
                    if len(target_nodes) == 1:
                        self.show(node_xpath)
                    else:
                        print(f'Metadata package contains {len(target_nodes)} `{bcolors.BOLD}{target}{bcolors.ENDC}` nodes:')
                        print('----------')
                        self.show(node_xpath)
                else:
                    return target_nodes
        except MissingNodeException as e:
            if quiet == False:
                print(e.msg)
    
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
    
    def print(self, node:Node=None):
        if node is None:
            myxml = metapype_io.to_xml(self.eml)
            root = etree.fromstring(myxml)
            print(etree.tostring(root, pretty_print=True).decode())
        else:
            myxml = metapype_io.to_xml(node)
            root = etree.fromstring(myxml)
            print(etree.tostring(root, pretty_print=True).decode())
        