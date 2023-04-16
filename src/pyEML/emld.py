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
from src.pyEML.error_classes import bcolors, MissingNodeException, InvalidDataStructure

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
    },
    'keywords': {
        'node_xpath': './dataset/keywordSet',
        'node_target': 'keywords',
        'values_dict': {
            'keywordSet': {
                'keyword': None
            }
        }
    },
    'publisher': {
        'node_xpath': './dataset/publisher',
        'node_target': 'publisher',
        'values_dict': {
            'publisher': {
                'address': {
                    'city': None,
                    'administrativeArea': None, #i.e., state or province
                    'postalCode': None,
                    'country': None
                },
                'onlineUrl': None,
                'userId': { # Research Organization Registry (ROR) id https://ror.org/
                    'directory': None,
                    'userId': None
                }
            }
        }
    },
    'pub_date': {
        'node_xpath': './dataset/pubDate',
        'node_target': 'publication date',
        'values_dict': {
            'pubDate': None
        }
    }
}


class Emld():
    """An object that holds data parsed from an EML-formatted xml file."""

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

        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_title()
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
            print('problem get_title()')

    def set_title(self, title:str):
        """Set the dataset's title
        
        Args:
            title (str): The title that you want to assign to your dataset.

        Examples:
            myemld.set_title(title='my new title')
        """
        try:
            node_xpath = LOOKUPS['title']['node_xpath']
            node_target= LOOKUPS['title']['node_target']
            values = LOOKUPS['title']['values_dict']
            assert title not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{title}". `{node_target}` cannot be blank.'
            assert len(title) >= 3, f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{title}". {bcolors.BOLD}`{node_target}`{bcolors.ENDC} must be at least three characters.'

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
            myemld.delete_title()
        """
        try:
            node_xpath = LOOKUPS['title']['node_xpath']
            node_target= LOOKUPS['title']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet) 
        except:
            print('error delete_title()') 
            
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
        """Specify the dataset creator's name, organization, and email

        Args:
            first (str, optional): The dataset creator's first name. Defaults to None.
            last (str, optional): The dataset creator's last name. Defaults to None.
            org (str, optional): The dataset creator's organization (e.g., company, government agency). Defaults to None.
            email (str, optional): The dataset creator's email address. Defaults to None.

        Examples:
            myemld.set_creator(first='Albus', last='Fumblesnore')
        """
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
        """Delete information about the dataset creator

        Args:
            None

        Examples:
            myemld.delete_creator()
        """
        try:
            node_xpath = LOOKUPS['creator']['node_xpath']
            node_target= LOOKUPS['creator']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet)  

        except:
            print('error delete_creator()')
    
    def get_keywords(self):
        """Get the dataset's keywords

        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_keywords()
        """
        try:
            node_xpath = LOOKUPS['keywords']['node_xpath']
            node_target= LOOKUPS['keywords']['node_target']
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
            print('problem get_keywords()')

    def set_keywords(self, *keywords):
        """Set the dataset's keywords

        Args:
            *keywords (str, arbitrary argument): `set_keywords()` accepts any number of comma-separated arguments

        Examples:
            myemld.delete_keywords()
        """
        try:
            for keyword in keywords:
                assert keyword not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{keyword}". {node_target} cannot be blank.'
                assert isinstance(keyword, (int, float, str)), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(keyword)}: {keyword}.\nKeywords must be comma-separated values of type str, int, or float.\nE.g., myemld.set_keywords("firstkeyword", "secondkeyword")'

            node_xpath = LOOKUPS['keywords']['node_xpath']
            node_target= LOOKUPS['keywords']['node_target']
            values = LOOKUPS['keywords']['values_dict']
            values['keywordSet']['keyword'] = keywords

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, quiet=quiet)

            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_keywords()

        except AssertionError as a:
            print(a)

    def delete_keywords(self):
        """Delete dataset keywords

        Args:
            None

        Examples:
            myemld.delete_keywords()
        """
        try:
            node_xpath = LOOKUPS['keywords']['node_xpath']
            node_target= LOOKUPS['keywords']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet)  

        except:
            print('error delete_keywords()')

    def get_publisher(self):
        """Get the dataset's publisher

        Args:
            None

        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_publisher()
        """
        try:
            node_xpath = LOOKUPS['publisher']['node_xpath']
            node_target= LOOKUPS['publisher']['node_target']
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
            print('problem get_publisher()')

    def set_publisher(self,
        org:str=None,
        street_address:str=None,
        city:str=None,
        state:str=None,
        zip=None, # allow user to enter str or int and type-cast later
        country:str=None,
        url:str=None,
        email:str=None,
        ror_id=None # allow user to enter str or int and type-cast later
        ):
        """Set the dataset publisher

        Args:
            org (str, optional): The publisher's organization; usually a company or government agency. Defaults to None.
            street_address (str, optional): The publisher's street address. Defaults to None.
            city (str, optional): The city of the publisher's street address. Defaults to None.
            state (str, optional): The state or province of the publisher's street address. Defaults to None.
            zip (str or int, optional): The zip or postal code of the publisher's street address. Defaults to None.
            url (str, optional): The publisher's website. Defaults to None.
            email (str, optional): The publisher's email address. Defaults to None.
            ror_id (str or int, optional): The publisher's Research Organization Registry (ROR) id; see https://ror.org/. Defaults to None.

        Examples:
            myemld.set_publisher(org='My organization')
            myemld.set_publisher(
                org='My organization',
                street_address='105 NE 5th Ave, #14',
                city='Chicago',
                state='IL',
                zip=60606,
                country='USA',
                url='www.nps.gov',
                email='myname@nps.gov',
                ror_id=11234
            )
        """
        try:
            if org is not None:
                assert org not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{org}". {node_target} cannot accept blank values.'
                assert isinstance(org, (int, float, str)), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(org)}: {org}.\Organization must be of type str, int, or float.\nE.g., myemld.set_publisher(org="yourorg")'
            if street_address is not None:
                assert street_address not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{street_address}". {node_target} cannot accept blank values.'
                assert isinstance(street_address, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(street_address)}: {street_address}.\Addresses must be of type str.\nE.g., myemld.set_publisher(street_address="101 5th Ave., #145")'
            if city is not None:
                assert city not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{city}". {node_target} cannot accept blank values.'
                assert isinstance(city, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(city)}: {city}.\City must be of type str.\nE.g., myemld.set_publisher(city="Memphis")'
            if state is not None:
                assert state not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{state}". {node_target} cannot accept blank values.'
                assert isinstance(state, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(state)}: {state}.\State must be of type str.\nE.g., myemld.set_publisher(state="OR")'
            if zip is not None:
                assert zip not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{zip}". {node_target} cannot accept blank values.'
                assert isinstance(zip, (str, int)), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(zip)}: {zip}.\Zip code must be of type str.\nE.g., myemld.set_publisher(zip=12312) or myemld.set_publisher(zip="12312")'
                zip = str(zip) # type-cast if zip passes assertions
            if country is not None:
                assert country not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{country}". {node_target} cannot accept blank values.'
                assert isinstance(country, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(country)}: {country}.\Country must be of type str.\nE.g., myemld.set_publisher(country="USA")'
            if url is not None:
                assert url not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{url}". {node_target} cannot accept blank values.'
                assert isinstance(url, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(url)}: {url}.\nURL must be of type str.\nE.g., myemld.set_publisher(url="www.nps.gov")'
            if email is not None:
                assert email not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{email}". {node_target} cannot accept blank values.'
                assert isinstance(email, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(email)}: {email}.\Email must be of type str.\nE.g., myemld.set_publisher(email="myname@nps.gov")'
            if ror_id is not None:
                assert ror_id not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{ror_id}". {node_target} cannot accept blank values.'
                assert isinstance(ror_id, (int, str)), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(ror_id)}: {ror_id}.\Research Organization Registry (ROR) id must be type str or int.\nSee https://ror.org/ for more information.\nE.g., myemld.set_publisher(ror_id="abc123")'
                ror_id = str(ror_id) # type-cast if ror_id passes assertions

            node_xpath = LOOKUPS['publisher']['node_xpath']
            node_target= LOOKUPS['publisher']['node_target']
            dirty_vals = LOOKUPS['publisher']['values_dict']

            dirty_vals['publisher']['organizationName'] = org
            dirty_vals['publisher']['address']['deliveryPoint'] = street_address
            dirty_vals['publisher']['address']['city'] = city
            dirty_vals['publisher']['address']['administrativeArea'] = state
            dirty_vals['publisher']['address']['postalCode'] = zip
            dirty_vals['publisher']['address']['country'] = country
            dirty_vals['publisher']['onlineUrl'] = url
            dirty_vals['publisher']['electronicMailAddress'] = email
            dirty_vals['publisher']['electronicMailAddress'] = email
            if ror_id:
                dirty_vals['publisher']['directory'] = 'https://ror.org/'
                dirty_vals['publisher']['userId'] = 'https://ror.org/' + ror_id

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            cleanvals = self._delete_none(dirty_vals)
            self._set_node(values=cleanvals, node_target=node_target, node_xpath=node_xpath, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_publisher()
            
        except:
            print('error set_publisher')

    def delete_publisher(self):
        """Delete dataset publisher

        Args:
            None

        Examples:
            myemld.delete_publisher()
        """
        try:
            node_xpath = LOOKUPS['publisher']['node_xpath']
            node_target= LOOKUPS['publisher']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet)  

        except:
            print('error delete_publisher()')
    
    def get_pub_date(self):
        """Get the dataset's publication date 

        Args:
            None

        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_pub_date()
        """
        try:
            node_xpath = LOOKUPS['pub_date']['node_xpath']
            node_target= LOOKUPS['pub_date']['node_target']
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
            print('problem get_pub_date()')

    def set_pub_date(self, pub_date:str):
        """Set the dataset's publication date 

        Args:
            pub_date (str): The dataset's publication date. No specific date format is required)

        Examples:
            myemld.set_pub_date(pub_date:'2021')
            myemld.set_pub_date(pub_date:'2022-01-01')
            myemld.set_pub_date(pub_date:'Jan 2022')
        """
        try:
            node_xpath = LOOKUPS['pub_date']['node_xpath']
            node_target= LOOKUPS['pub_date']['node_target']
            values = LOOKUPS['pub_date']['values_dict']
            assert pub_date not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{pub_date}". `{node_target}` cannot be blank.'

            values['pubDate'] = pub_date
            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_pub_date()
        
        except AssertionError as a:
            print(a)

    def delete_pub_date(self):
        """Delete the dataset's publication date 
        
        Args:
            None

        Examples:
            myemld.delete_pub_date()
        """
        try:
            node_xpath = LOOKUPS['pub_date']['node_xpath']
            node_target= LOOKUPS['pub_date']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet)
        except:
            print('error delete_pub_date()')

    def _serialize(self, node:etree._Element, depth:int=0):
        """Starts at a given node, crawls all of its sub-nodes, pretty-prints tags and text to console

        Args:
            node (lxml.etree._Element): The parent node at which you want to start your element-tree crawl
            depth (int, optional): _description_. Defaults to 0.

        Examples:
            # crawl a single node
            node = myemld.root.find('./dataset/creator') # returns one lxml.etree._Element
            myemld._serialize(node)

            # crawl multiple nodes
            testroot = myemld.root.findall('./dataset') # returns a list of lxml.etree._Element
            for node in testroot:
                myemld._serialize(node)
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
            node_xpath (str): The xpath to the node to be deleted.
            node_target (str): A short text name for the node to be deleted. Used for f-string generation.
            quiet (bool): Toggles overwrite warnings and exception messaging.

        Raises:
            error_classes.MissingNodeException: Raises when a call tries to access a node that does not exist.

        Examples:
            myemld._delete_node(node_target='title', node_xpath='./dataset/title', quiet=False)
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
                        print(f'`{bcolors.BOLD}{node_target}{bcolors.ENDC}` deleted.')
                    else:
                        print(f'`{bcolors.BOLD}{node_target}{bcolors.ENDC}` deletion cancelled.')

        except MissingNodeException as e:
            if quiet == False:
                print(e.msg)
            
    def _get_node(self, node_xpath:str, node_target:str, pretty:bool, quiet:bool):
        """Get the value(s) at a node

        Args:
            node_xpath (str): The xpath to the node to be deleted.
            node_target (str): A short text name for the node to be deleted. Used for f-string generation.
            pretty (bool): True prints serialized nodes to console. False returns lxml.etree._Element.
            quiet (bool): Toggles exception messaging for interactive sessions.

        Raises:
            error_classes.MissingNodeException: Raises when a call tries to access a node that does not exist.

        Returns:
            str: when pretty == True; prints serialized nodes to console
            lxml.etree._Element: when pretty == False

        Examples:
            myemld._get_node(node_target='title', node_xpath='./dataset/title', pretty=True, quiet=False)
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
            values (dict): A dictionary of values to serialize into xml tags and text.
            node_target (str): A short text name for the node to be deleted. Used for f-string generation.
            node_xpath (str): The xpath to the node to be set.
            quiet (bool): Toggles exception messaging for interactive sessions.

        Raises:
            AssertionError: There must be at least one False in node_check.values() or program will duplicate xml tags

        Examples:
            myemld.delete_title()
            values_dict={'title': 'my new title'}
            myemld._set_node(values_dict, node_target='title', node_xpath='./dataset/title', quiet=False)
            myemld.get_title()
        """
        try:
            # if there's already a node at `node_target`, delete it
            if quiet == True:
                self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet)
            else:
                node = self._get_node(node_xpath=node_xpath, node_target=node_target, pretty=False, quiet=True)
                if node is None or len(node) == 0:
                    pass
                else:
                    if len(node) == 1:
                        print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nYour dataset has a `{bcolors.BOLD}{node_target}{bcolors.ENDC}` node:')
                    elif len(node) > 1:
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
            
            parent_node = nodeset[0]
            self._serialize_nodes(_dict = values, target_node=parent_node)

        except AssertionError as a:
            print(a)
    
    def _find_parents(self, node_xpath:str):
        """Traverse upstream in an element tree to find xpath of each parent node above a `node_target`

        Args:
            node_xpath (str): an xpath to a node in an element tree

        Returns:
            list: list of xpaths for each possible parent-node upstream from the `node_target`

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
        """Recursively builds xpaths from a list of node names

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
        try:
            for key, value in list(_dict.items()):
                if isinstance(value, (float, int, str)):
                    child_node = etree.SubElement(target_node, key)
                    child_node.text = _dict[key]
                elif isinstance(value, dict):
                    child_node = etree.SubElement(target_node, key)
                    self._serialize_nodes(value, child_node)
                elif isinstance(value, (list, tuple)):
                    for v_i in value:
                        child_node = etree.SubElement(target_node, key)
                        if isinstance(v_i, (float, int, str)):
                            child_node.text = v_i
                        elif isinstance(v_i, dict):
                            self._serialize_nodes(v_i, child_node)
                        else:
                            raise InvalidDataStructure(target_node) # a non-serializable data structure (e.g., a list of lists of lists of lists...)
        
        except InvalidDataStructure as e:
            print(e.msg)
    
    def _delete_none(self, _dict):
        """Delete None values recursively from all of the dictionaries"""
        # adapted from https://stackoverflow.com/questions/33797126/proper-way-to-remove-keys-in-dictionary-with-none-values-in-python
        for key, value in list(_dict.items()):
            if isinstance(value, dict):
                if len(value) == 0:
                    del _dict[key]
                if len(value) > 0:
                    none_check = []
                    for v in value.values():
                        if v is None:
                            none_check.append(True)
                        else:
                            none_check.append(False)
                    if all(none_check):
                        del _dict[key]
                    else:
                        self._delete_none(value)
            elif value in ('', None, 'None'):
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