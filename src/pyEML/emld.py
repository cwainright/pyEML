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
import src.pyEML.error_classes as error_classes

class Emld():
    """A container that holds data parsed from an EML-formatted xml file."""

    def __init__(self, filepath:str, NPS:bool=True, INTERACTIVE:bool=False):
        """Constructor for class Emld
        
        Args:
            filepath (str): Filepath and name for the source-xml that is parsed to an element tree.
            NPS (bool): True means NPS is the author of the xml.
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
            self.nps = NPS
            self.interactive = INTERACTIVE
            
            # filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/2023/20230210_iss135_emleditor/sandbox/testinput.xml'
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(filepath, parser)
            root = tree.getroot()
            self.tree = tree
            self.root = root

        except:
            print('exception')

    def get_title(self, pretty:bool=False):
        """Get the dataset's title 

        Args:
            pretty (bool, optional): True returns pretty-printed version. Defaults to False.

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
            node_text = './dataset/title'
            node_target= 'title'
            self._get_node(node_text=node_text, node_target=node_target, pretty=pretty)
        except:
            return None

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
            force = False
            # if self.interactive == True:
            #     if self.get_title() is not None:
            #         title_element = self.get_title()
            #         if len(title_element) == 0:
            #             self.get_title() # returns no title exception
            #         elif len(title_element) == 1:
            #             print('Your dataset already has a title:')
            #             print(title_element[0].text)
            #             overwrite = input("Do you want to overwrite your dataset's title? ('y' to overwrite / 'n' to cancel)\n\n")
            #             print(f'User input: {overwrite}\n')
            #             if overwrite.lower() == 'y':
            #                 force = True
            #             else:
            #                 print('`set_title()` stopped. Kept original title.')
            #                 self.get_title(pretty=True)
            #                 force = False
            #         elif len(title_element) > 1:
            #             print('Your dataset has multiple title nodes. Use `delete_title()` and then try `set_title()` again.')
            #     else:
            #         force = True
            if self.interactive == False or force == True or self.get_title() is None:
                if self.get_title() is not None:
                    self.delete_title(quiet=True)
                if not self.root.findall('./dataset'):
                    dataset_element = etree.SubElement(self.root, 'dataset')
                dataset_element = self.root.findall('./dataset')
                if len(dataset_element) != 1:
                    raise Exception
                title_element = etree.SubElement(dataset_element, 'title')
                title_element.text = title
                if self.interactive == True:
                    print('Dataset title updated:')
                    self.get_title(pretty=True)
        except:
            print('set title problem')

    def delete_title(self, quiet:bool=False):
        """Delete value(s) from dataset title node(s)
        
        Args:
        quiet (bool): Override self.interactive to turn off messages for this method.
        
        Examples:
            myemld.get_title(pretty=True)
            myemld.set_title(title='my new title')
            myemld.get_title(pretty=True)
            myemld.delete_title()
            myemld.get_title(pretty=True)
        """
        
        node_text = './dataset/title'
        node_target= 'title'
        self._delete_node(node_text=node_text, node_target=node_target, quiet=quiet)  
            
    def get_creator(self, pretty:bool=False):
        """Get information about the dataset's creator

        Args:
            pretty (bool, optional): True - Pretty-print tree to console. False - return element tree. Defaults to False.

        Examples:
            myemld.get_creator()
        """
        try:
            node_text = './dataset/creator'
            node_target= 'creator'
            self._get_node(node_text=node_text, node_target=node_target, pretty=pretty)
        except:
            return None

    def set_creator(self, creator:str):
        pass

    def delete_creator(self, quiet:bool=True):
        try:
            node_text = './dataset/title'
            node_target= 'title'
            self._get_node(node_text=node_text, node_target=node_target, pretty=False)
        except:
            return None
    
    def _serialize(self, node, depth=0):
        """Starts at a given node, crawls all of its sub-nodes, pretty-prints tags and text to console

        Args:
            node (lxml.etree._Element): The parent node at which you want to start your element-tree crawl
            depth (int, optional): _description_. Defaults to 0.

        Examples:
            # crawl a single node
            testroot = myemld.root.find('./dataset/creator') # returns a lxml.etree._Element
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

        # testroot = myemld.root.find('./dataset/creator')
        # def serialize(node, depth=0):
        #     indents = depth * '    '
        #     print(f'{indents}<{node.tag}>')
        #     for elm in node:
        #         if len(elm) == 0:
        #             print(f'{indents}    <{elm.tag}>')
        #             print(f'{indents}            {elm.text}')
        #             print(f'{indents}    </{elm.tag}>')
        #         else:
        #             serialize(elm, depth+1)
        #     print(f'{indents}</{node.tag}>')
        # serialize(testroot)

    def _delete_node(self, node_text:str, node_target:str, quiet:bool=False):
        """A helper method that deletes the value(s) at a node

        Args:
            node_text (str): _description_
            node_target (str): _description_
            quiet (bool, optional): _description_. Defaults to False.

        Raises:
            error_classes.MissingNodeException: _description_
        """
        try:
            node = self._get_node(node_text=node_text, node_target=node_target, pretty=False)
            if node is None:
                raise error_classes.MissingNodeException
            if node is not None:
                if quiet == True:
                        pass
                elif self.interactive == True:
                    print(f'Warning! Your dataset has one or {node_target} nodes:')
                    counter = 1
                    for elm in node:
                        print(f'{counter}. {elm.text}')
                        counter += 1
                    overwrite = input('Do you want to delete these node(s)? ("y" to delete, "n" to cancel.)')
                    print(f'User input: {overwrite}')
                    if overwrite.lower() == 'y':
                        force = True
                        print('Deleting nodes...')
                    else:
                        force = False
                        print(f'`{node_target}` deletion cancelled.')
                if self.interactive == False or quiet == True or force == True:
                    if len(node) == 1:
                        for child in node:
                            child.getparent().remove(child)
                    else:
                        for child in node:
                            for elm in child:
                                elm.getparent().remove(elm)
                if self.interactive == True:
                    self._get_node(node_text=node_text, node_target=node_target, pretty=True)
        except error_classes.MissingNodeException:
            myerror = error_classes.MissingNodeException(problem_val=node_target)
            if self.interactive == True:
                print(myerror.msg)
        

    def _get_node(self, node_text:str, node_target:str, pretty:bool):
        """A helper method that retrieves the value(s) at a node

        Args:
            node_text (str): _description_
            node_target (str): _description_
            pretty (bool): _description_

        Raises:
            error_classes.MissingNodeException: _description_

        Returns:
            _type_: _description_
        """
        try:
            node = self.root.findall(node_text)
            if node is None:
                raise error_classes.MissingNodeException(node_target)
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
        except error_classes.MissingNodeException as e:
            print(e.msg)

    def _set_node(self, node_text:str, node_target:str):
        """A helper method that sets the value(s) at a node

        Args:
            node_text (str): _description_
            node_target (str): _description_
        """
        pass
    
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