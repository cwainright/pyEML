"""Python source module for working with EML-styled metadata in xml form

`emld.py` holds all constants, variables, classes, methods, and functions necessary to
instantiate an `Emld` from EML-valid xml. A user can then create, read, edit, and delete  
`Emld` nodes to create, read, update, and delete metadata. Finally, a user can build outputs, 
like an .xml document for submission with a dataset deliverable.

Authored: 2023-04-07
Author: Charles Wainright
Entity: US National Park Service
License: MIT, license information at end of file
"""

import lxml.etree as etree
from src.pyEML.error_classes import bcolors, MissingNodeException

# const `LOOKUPS` holds abstracted EML-schema information that an `Emld` get, set, and delete methods need
# to build variables. This abstraction lets the engineer maintain EML-node specifics in
# one place, `LOOKUPS`, instead of in individual methods.
LOOKUPS = {
    'title': {
        'node_xpath': './dataset/title',
        'node_target': 'title',
        'values_dict': {
            'title': None
            }
    },
    'creator': {
        'node_xpath': './dataset/creator',
        'node_target': 'creator',
        'values_dict': {
            'creator': {
                'individualName': {
                'givenName': None,
                'surName': None
            },
            'organizationName': None,
            'electronicMailAddress': None
            }
        }
    }
}


class Emld():
    """A container that holds data parsed from an EML-formatted xml file."""

    def __init__(self, filepath:str, INTERACTIVE:bool=False):
        """Constructor for class Emld
        
        Args:
            filepath (str): Filepath and name for the source-xml that is parsed to an element tree.
            INTERACTIVE (bool): Turns on status messages and overwrite detection. True is for interactive sessions. Shows status messages, asks user for permission before overwriting.
                False is for automated scripting. Silences status messages and writes metadata verbatim as scripted.
        
        Attributes:
            xml_src (str): Filepath and name for the source-xml that is parsed to an element tree.
            nps (bool): Turns on NPS-specific data package requirements. True: NPS is the author of the xml. `_set_by_for_nps()` - does NOT execute if kwarg self.nps == False.
                `_set_npspublisher()` - does NOT execute if kwarg self.nps == False.
            interactive (bool): Turns on status messages and overwrite detection. True is for interactive sessions. Show status messages, ask user for permission before overwriting.
                False is for automated scripting. Silence status messages and write metadata verbatim as scripted.
            tree (lxml.etree._ElementTree): an lxml element tree containing data parsed from self.xmlstring.
            root (lxml.etree._Element): the root node of self.tree.
        """
        try:
            self.xml_src = filepath
            self.interactive = INTERACTIVE
            
            # filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/2023/20230210_iss135_emleditor/sandbox/testinput.xml'
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(filepath, parser)
            root = tree.getroot()
            self.tree = tree
            self.root = root

        except:
            print('exception')

    def get_title(self):
        """Get the dataset's title 

        Args:
            None

        Raises:
            Exception: _description_

        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_title(pretty=True)
            myemld.set_title(title='my new title')
            myemld.get_title(pretty=True)
            myemld.delete_title()
            myemld.get_title(pretty=True)
        """

        try:

            node_xpath = LOOKUPS['title']['node_xpath']
            node_target= LOOKUPS['title']['node_target']
            if self.interactive == True:
                pretty=True
                quiet=False
                self._get_node(node_xpath=node_xpath, node_target=node_target, pretty=pretty, quiet=quiet)
            else:
                pretty=False
                quiet=True
                node = self._get_node(node_xpath=node_xpath, node_target=node_target, pretty=pretty, quiet=quiet)
                if node: # only returns an object if pretty == False
                    return node
            
        except:
            print('problem get_title')

    def set_title(self, title:str):
        """Set the dataset's title
        
        Args:
            title (str): The title that you want to assign to your dataset.

        Examples:
            myemld.get_title(pretty=True)
            myemld.set_title(title='my new title')
            myemld.get_title(pretty=True)
            myemld.delete_title()
            myemld.get_title(pretty=True)
        """
        try:
            node_xpath = LOOKUPS['title']['node_xpath']
            node_target= LOOKUPS['title']['node_target']
            values = LOOKUPS['title']['values_dict']
            assert title not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{title}". `title` cannot be blank.'
            assert len(title) >= 3, f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{title}". {bcolors.BOLD}`title`{bcolors.ENDC} must be at least three characters.'

            values['title'] = title
            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_title()
        
        except AssertionError as a:
            print(a)

    def delete_title(self):
        """Delete value(s) from dataset title node(s)
        
        Args:
            None

        Examples:
            myemld.get_title(pretty=True)
            myemld.set_title(title='my new title')
            myemld.get_title(pretty=True)
            myemld.delete_title()
            myemld.get_title(pretty=True)
        """
        node_xpath = LOOKUPS['title']['node_xpath']
        node_target= LOOKUPS['title']['node_target']
        if self.interactive == True:
            quiet=False
        else:
            quiet=True
        self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet)  
            
    def get_creator(self):
        """Get information about the dataset's creator

        Args:
            None

        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_creator()
        """
        try:
            node_xpath = LOOKUPS['creator']['node_xpath']
            node_target= LOOKUPS['creator']['node_target']
            if self.interactive == True:
                pretty=True
                quiet=False
                self._get_node(node_xpath=node_xpath, node_target=node_target, pretty=pretty, quiet=quiet)
            else:
                pretty=False
                quiet=True
                node = self._get_node(node_xpath=node_xpath, node_target=node_target, pretty=pretty, quiet=quiet)
                if node: # only returns an object if pretty == False
                    return node

        except:
            print('problem get_creator')

    def set_creator(self, first:str=None, last:str=None, org:str=None, email:str=None):
        try:
            node_xpath = LOOKUPS['creator']['node_xpath']
            node_target= LOOKUPS['creator']['node_target']
            dirty_vals = LOOKUPS['creator']['values_dict']

            if first not in (None, ''):
                dirty_vals['creator']['individualName']['givenName'] = first
            if last not in (None, ''):
                dirty_vals['creator']['individualName']['surName'] = last
            if org not in (None, ''):
                dirty_vals['creator']['organizationName'] = org
            if email not in (None, ''):
                dirty_vals['creator']['electronicMailAddress'] = email

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            cleanvals = self._delete_none(dirty_vals)
            self._set_node(values=cleanvals, node_target=node_target, node_xpath=node_xpath, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_creator()
            
        except:
            print('error set_creator')

    def delete_creator(self):
        try:
            node_xpath = './dataset/creator'
            node_target= 'creator'
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet)  

        except:
            print('error')
    
    def _serialize(self, node, depth=0):
        """Starts at a given node, crawls all of its sub-nodes, pretty-prints tags and text to console

        Args:
            node (lxml.etree._Element): The parent node at which you want to start your element-tree crawl
            depth (int, optional): _description_. Defaults to 0.

        Examples:
            # crawl a single node
            testroot = myemld.root.find('./dataset/creator') # returns one lxml.etree._Element
            myemld._serialize(testroot)

            # crawl multiple nodes
            testroot = myemld.root.findall('./dataset') # returns a list of lxml.etree._Element
            for root in testroot:
                print(root.tag)
        """
        if len(node) == 0:
            print(f'<{node.tag}>')
            print(f'    {node.text}')
            print(f'</{node.tag}>')
        else:
            spaces = depth * '    '
            print(f'{spaces}<{node.tag}>')
            for elm in node:
                if len(elm) == 0:
                    print(f'{spaces}    <{elm.tag}>')
                    print(f'{spaces}        {elm.text}')
                    print(f'{spaces}    </{elm.tag}>')
                else:
                    self._serialize(elm, depth+1)
            print(f'{spaces}</{node.tag}>')

    def _delete_node(self, node_xpath:str, node_target:str, quiet:bool):
        """Deletes the value(s) at a node

        Args:
            node_xpath (str): _description_
            node_target (str): _description_
            quiet (bool, optional): _description_. Defaults to False.

        Raises:
            error_classes.MissingNodeException: _description_

        Todo:
            Bug fix: When deleting any node for the second time (i.e., trying to delete a node that you just deleted),
                while quiet == False, `MissingNodeException` are chained together so that you get the same message multiple times.
                E.g.,
                    myemld.delete_title(quiet=False) # execute the first time, enter 'y' if self.interactive == True and prompted to delete
                    myemld.delete_title(quiet=False) # execute the second time; should produce two `MissingNodeException`s

        """
        try:
            node = self._get_node(node_xpath=node_xpath, node_target=node_target, pretty=False, quiet=True) 
            if node is None or len(node) == 0:
                raise MissingNodeException(node_target)
            else:
                if quiet == True:
                    if len(node) == 1:
                        for child in node:
                            child.getparent().remove(child)
                    else:
                        for child in node:
                            for elm in child:
                                elm.getparent().remove(elm)
                else:
                    if len(node) == 1:
                        print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nYour dataset has a `{bcolors.BOLD}{node_target}{bcolors.ENDC}` node:')
                    if len(node) > 1:
                        print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nYour dataset has {len(node)} `{bcolors.BOLD}{node_target}{bcolors.ENDC}` nodes:')
                    counter = 1
                    for elm in node:
                        if len(node) <=1:
                            self._serialize(elm)
                        if len(node) >1:
                            print(f'{counter}:')
                            self._serialize(elm)
                            counter += 1

                    overwrite = input(f'{bcolors.BOLD}Do you want to delete these node(s)?\n{bcolors.ENDC}("{bcolors.BOLD}y{bcolors.ENDC}" to delete, "{bcolors.BOLD}n{bcolors.ENDC}" to cancel.)\n\n')
                    print(f'User input: {overwrite}')
                    if overwrite.lower() == 'y':
                        for child in node:
                            child.getparent().remove(child)
                        # if len(node) == 0:
                            
                        # elif len(node) == 1:
                        #     for child in node:
                        #         child.getparent().remove(child)
                        # else:
                        #     for child in node:
                        #         child.getparent().remove(child)
                        #         for elm in child:
                        #             elm.getparent().remove(elm)
                        print(f'`{bcolors.BOLD}{node_target}{bcolors.ENDC}` deleted.')
                    else:
                        print(f'`{bcolors.BOLD}{node_target}{bcolors.ENDC}` deletion cancelled.')

        except MissingNodeException as e:
            if quiet == False:
                print(e.msg)
            
    def _get_node(self, node_xpath:str, node_target:str, pretty:bool, quiet:bool):
        """Get the value(s) at a node

        Args:
            node_xpath (str): _description_
            node_target (str): _description_
            pretty (bool): _description_
            quiet (bool):

        Raises:
            error_classes.MissingNodeException: _description_

        Returns:
            _type_: _description_
        """
        try:
            node = self.root.findall(node_xpath)
            if len(node) == 0:
                raise MissingNodeException(node_target)
            else:
                if pretty == True:
                    if len(node) == 1:
                        for child in node:
                            self._serialize(child)
                    else:
                        for child in node:
                            for element in child:
                                self._serialize(element)
                else:
                    return node
        except MissingNodeException as e:
            if quiet == False:
                print(e.msg)
        
    def _set_node(self, values:dict, node_target:str, node_xpath:str, quiet:bool):
        """Set the value(s) at a node

        Args:
            values (any): the values to be added to the `node_xpath`
            node_xpath (str): xpath for the node to which values will be added
            node_target (str): text name of the node; for f-string generation
        """
        try:
            # if there's already a node at `node_target`, delete it
            if quiet == True:
                self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet)
            else:
                node = self._get_node(node_xpath=node_xpath, node_target=node_target, pretty=False, quiet=quiet)
                if len(node) == 1:
                    print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nYour dataset has a `{bcolors.BOLD}{node_target}{bcolors.ENDC}` node:')
                if len(node) > 1:
                    print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nYour dataset has {len(node)} `{bcolors.BOLD}{node_target}{bcolors.ENDC}` nodes:')
                counter = 1
                for elm in node:
                    if len(node) <=1:
                        self._serialize(elm)
                    if len(node) >1:
                        print(f'{counter}:')
                        self._serialize(elm)
                        counter += 1

                overwrite = input(f'{bcolors.BOLD}Do you want to delete these node(s)?\n{bcolors.ENDC}("{bcolors.BOLD}y{bcolors.ENDC}" to delete, "{bcolors.BOLD}n{bcolors.ENDC}" to cancel.)\n\n')
                print(f'User input: {overwrite}')
                if overwrite.lower() == 'y':
                    self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=True)
                else:
                    print(f'`{bcolors.BOLD}{node_target}{bcolors.ENDC}` set cancelled.')

            
            # if there's not a node at `node_target`, need to find crawl xpath to add missing nodes
            node_list = self._find_parents(node_xpath=node_xpath)
            node_check = {}
            for element in node_list:
                nodeset = self.root.findall(element)
                if len(nodeset) == 0:
                    node_check[element]=False
                else:
                    node_check[element]=True

            assert False in node_check.values(), 'Node deletion failed' # there must be at least one False in node_check or program will duplicate tags
            # if all upstream nodes exist, make child element(s)
            parent_node = nodeset[0]
            # target_node = etree.SubElement(parent_node, node_target)
            self._serialize_nodes(_dict = values, target_node=parent_node)
            # for key, value in list(values.items()):
            #     if isinstance(value, (float, int, str)):
            #         new_node = etree.SubElement(parent_node, key)
            #         new_node.text = values[key]
        except AssertionError as a:
            print(a)
    
    def _find_parents(self, node_xpath:str):
        """Helper method that traverses upstream in an element tree to find each parent node above a `node_target`

        Args:
            node_xpath (str): an xpath to a node in an element tree

        Returns:
            list: Each list element is the xpath for one parent-node upstream from the `node_target`

        Examples:
            node_xpath = './dataset/creator/individualName/givenName'
            myemld._find_parents(node_xpath)
        """
        parent_nodes = []
        xpath_split = node_xpath.split('/')
        xpath_split = xpath_split[1:]
        self._reverse_serialize(xpath_split, parent_nodes)
        return parent_nodes

    def _reverse_serialize(self, xpath_split:list, parent_nodes:list):
        """Helper method that recursively builds xpaths from a list of node names

        Args:
            xpath_split (list): a list of node names parsed from an element tree xpath in `_find_parents()`
            parent_nodes (list): a list of xpaths recursively concatenated from each element in `xpath_split`
        """
        listcopy = xpath_split
        prefix = './' # xpath prefix
        newstring = prefix + '/'.join(xpath_split)
        parent_nodes.append(newstring)
        if len(listcopy) > 1:
            listcopy.pop()
            self._reverse_serialize(listcopy, parent_nodes)

    def _serialize_nodes(self, _dict:dict, target_node:etree._Element):
        """Build `etree.SubElement`s from key-value pairs in a dictionary

        Args:
            _dict (dict): A dictionary of key-value pairs. Keys are mapped to element.tag and values are mapped to element.text unless otherwise specified.
            parent_node (etree._Element): The parent element to which child nodes need to be serially added
        """
        for key, value in list(_dict.items()):
            if isinstance(value, (float, int, str)):
                child_node = etree.SubElement(target_node, key)
                child_node.text = _dict[key]
            elif isinstance(value, dict):
                child_node = etree.SubElement(target_node, key)
                self._serialize_nodes(value, child_node)
            elif isinstance(value, list):
                for v_i in value:
                    child_node = etree.SubElement(target_node, key)
                    if isinstance(v_i, dict):
                        self._serialize_nodes(v_i, child_node)
    
    def _delete_none(self, _dict):
        """Delete None values recursively from all of the dictionaries"""
        # adapted from https://stackoverflow.com/questions/33797126/proper-way-to-remove-keys-in-dictionary-with-none-values-in-python
        for key, value in list(_dict.items()):
            if isinstance(value, dict):
                self._delete_none(value)
            elif value in ('', None, 'None'):
                del _dict[key]
            elif value is None:
                del _dict[key]
            elif isinstance(value, list):
                for v_i in value:
                    if isinstance(v_i, dict):
                        self._delete_none(v_i)

        return _dict
    
    def write_eml(self, filename:str):
        """Write EML-formatted xml file
        
        Args:
            filename (str): the filename and filepath where you want to save your EML-formatted xml.

        Examples:
            tree.write('test_output.xml', pretty_print=True)
        """
        if not filename.endswith('.xml'):
            print('Your filename must end in the .xml file extension')
        else:
            self.tree.write(filename, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    def make_nps(self):
        pass

"""Copyright (C) 2023 Charles Wainright, US National Park Service

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""