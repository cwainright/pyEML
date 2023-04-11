"""Python source module for working with EML-styled metadata

`emld2.py` holds all constants, variables, classes, methods, and functions necessary to
instantiate an `Emld` from EML-valid xml. A user can then create, read, edit, and delete  
`Emld` nodes to produce or append metadata. Finally, a user can build outputs, 
like an .xml document for submission with a dataset deliverable.

Authored: 2023-04-07
Author: Charles Wainright
Entity: US National Park Service
License: MIT, license information at end of file
"""

import lxml.etree as etree

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
        ```
        myemld.get_title(pretty=True)
        myemld.set_title(title='my new title')
        myemld.get_title(pretty=True)
        myemld.delete_title()
        myemld.get_title(pretty=True)
        ```
        """

        try:
            if not self.root.findall('./dataset/title'):
                raise Exception
            if len(self.root.findall('./dataset/title')) == 1:
                title_element = self.root.find('./dataset/title')
                if pretty == True:
                    print('Dataset title:')
                    print(title_element.text)
                else:
                    return title_element
            if len(self.root.findall('./dataset/title')) > 1:
                title_element = self.root.findall('./dataset/title')
                print('Your dataset has multiple nodes named "title":')
                counter = 1
                for elm in title_element:
                    print(f'{counter}. {elm.text}')
                    counter += 1
                print('Suggested solutions:')
                print('1. Use `delete_title()` to clear your dataset\'s title and retry `set_title()`.')
                print('2. Edit your xml file and remove repeated dataset/title nodes.')

        except:
            print('Your dataset does not have a title. Use `set_title()` to resolve this problem.')
            return None

    def set_title(self, title:str):
        """Set the dataset's title
        
        Args:
        title (str): The title that you want to assign to your dataset.

        Examples:
        ```
        myemld.get_title(pretty=True)
        myemld.set_title(title='my new title')
        myemld.get_title(pretty=True)
        myemld.delete_title()
        myemld.get_title(pretty=True)
        ```

        """
        try:
            title_element = self.get_title()
            if self.interactive == True:
                if title_element is not None:
                    print('Your dataset already has a title:')
                    print(title_element.text)
                    overwrite = input("Do you want to overwrite your dataset's title? 'y' and enter to overwrite, any other key to keep title.")
                    print(f'User input: {overwrite}')
                    if overwrite.lower() == 'y':
                        force = True
                    else:
                        print('`set_title()` stopped. Kept original title.')
                        self.get_title(pretty=True)
                        force = False
                else:
                    force = True
            if self.interactive == False or force == True:
                if not self.root.findall('./dataset'):
                    dataset_element = etree.SubElement(self.root, 'dataset')
                dataset_element = self.root.findall('./dataset')
                if len(dataset_element) == 1:
                    dataset_element = dataset_element[0]
                else:
                    self.get_title() # will return the exception about a dataset having zero or more than one title node
                if title_element is not None:
                    self.delete_title(quiet=True)
                title_element = etree.Element('title')
                title_element.text = title
                dataset_element.append(title_element)
                if self.interactive == True:
                    self.get_title(pretty=True)
        except:
            print('set title problem')

    def delete_title(self, quiet:bool=True):
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
        
        if self.get_title() is not None:
        # if there's no title, this redirect to show "there is no title" exception in self.get_title()
            if quiet == True:
                pass
            elif self.interactive == True:
                print('Warning! Your dataset has one or more title nodes:')
                counter = 1
                for elm in self.root.findall('./dataset/title'):
                    print(f'{counter}. {elm.text}')
                    counter += 1
                overwrite = input('Do you want to delete title node(s)? "y" and enter to delete, any other key to abort.')
                if overwrite.lower == 'y':
                    for elm in self.root.findall('./dataset/title'):
                        elm.getparent().remove(elm)
                else:
                    print('Title deletion aborted.')
                    self.get_title(pretty=True)
            if self.interactive == False or quiet == True:
                for elm in self.root.findall('./dataset/title'):
                        elm.getparent().remove(elm)
            
    def write_eml(self, filename:str):
        """Write EML-formatted xml file
        
        Args:
        filename (str): the filename and filepath where you want to save your EML-formatted xml.

        Examples:
        ```
        tree.write('test_output.xml', pretty_print=True)
        ```
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