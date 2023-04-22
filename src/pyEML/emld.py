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
from src.pyEML.constants import LOOKUPS, CUI_CHOICES, LICENSE_TEXT, CURRENT_RELEASE, APP_NAME, NPS_DOI_ADDRESS, CITATION_STYLES, AVAILABLE_ATTRIBUTES
from datetime import datetime
import iso639
import urllib
import pandas as pd
import xmltodict
import gc
import sys
import json

class Emld():
    """An object that holds data parsed from an EML-formatted xml file."""

    def __init__(self, filepath:str, INTERACTIVE:bool=True):
        """Constructor for class Emld
        
        Args:
            filepath (str): Filepath and name for the source-xml that is parsed to an element tree.
            INTERACTIVE (bool): Turns on status messages and overwrite detection. True is for interactive sessions. Shows status messages, asks user for permission before overwriting.
                False is for automated scripting. Silences status messages and writes metadata verbatim as scripted. Default is True.
        
        Attributes:
            xml_src (str): Filepath and name for the source-xml that is parsed to an element tree.
            interactive (bool): Turns on status messages and overwrite detection. True is for interactive sessions. Show status messages, ask user for permission before overwriting.
                False is for automated scripting. Silence status messages and write metadata verbatim as scripted.
            tree (lxml.etree._ElementTree): an lxml element tree containing data parsed from self.xmlstring.
            root (lxml.etree._Element): the root node of self.tree.
        """
        try:
            assert filepath.endswith('.xml'), print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.{bcolors.ENDC}\nYou provided "{bcolors.BOLD}{filepath}{bcolors.ENDC}".\nYou must create an`{bcolors.BOLD}Emld{bcolors.ENDC}` from an xml document.\nFilename should end in "{bcolors.BOLD}.xml{bcolors.ENDC}".')
            self.xml_src = filepath
            self.interactive = INTERACTIVE
            
            # filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/2023/20230210_iss135_emleditor/sandbox/testinput.xml'
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(filepath, parser)
            root = tree.getroot()
            self.tree = tree
            self.root = root
            self._set_version()

            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}Emld{bcolors.ENDC}` created and interactive session started.')

        except TypeError as t:
            print(t)
        except ValueError as v:
            print(v)
        except AssertionError as a:
            print(a)
        except:
            print(f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}\n{bcolors.BOLD}`Emld`{bcolors.ENDC} not created.')

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
            parent = LOOKUPS['title']['parent']
            values = LOOKUPS['title']['values_dict']
            assert title not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{title}". `{node_target}` cannot be blank.'
            assert len(title) >= 3, f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{title}". {bcolors.BOLD}`{node_target}`{bcolors.ENDC} must be at least three characters.'

            values['title'] = title
            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
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
            print('problem get_creator()')

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
            parent= LOOKUPS['creator']['parent']
            dirty_vals = LOOKUPS['creator']['values_dict']
            
            entries = []
            if first not in (None, ''):
                assert isinstance(first, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(first)}: {first}.\nFirst name must be of type str.\nE.g., myemld.set_creator(first="Albus")'
                dirty_vals['creator']['individualName']['givenName'] = first
                entries.append(True)
            if last not in (None, ''):
                assert isinstance(last, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(last)}: {last}.\Last name must be of type str.\nE.g., myemld.set_creator(last="Fumblesnore")'
                dirty_vals['creator']['individualName']['surName'] = last
                entries.append(True)
            if org not in (None, ''):
                assert isinstance(org, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(org)}: {org}.\Organization name must be of type str.\nE.g., myemld.set_creator(org="House Gryffinsnore")'
                dirty_vals['creator']['organizationName'] = org
                entries.append(True)
            if email not in (None, ''):
                assert isinstance(email, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(email)}: {email}.\Email must be of type str.\nE.g., myemld.set_creator(email="wellsley.r@gryffinsnore.edu")'
                dirty_vals['creator']['electronicMailAddress'] = email
                entries.append(True)

            assert any(entries), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided no values to set.'
            
            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            cleanvals = self._delete_none(dirty_vals)
            self._set_node(values=cleanvals, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_creator()
            
        except AssertionError as a:
            print(a)
        except:
            print('error set_creator()')

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
            parent= LOOKUPS['keywords']['parent']
            values = LOOKUPS['keywords']['values_dict']
            values['keywordSet']['keyword'] = keywords

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)

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
            parent= LOOKUPS['publisher']['parent']
            
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
            self._set_node(values=cleanvals, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
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
            parent= LOOKUPS['pub_date']['parent']
            values = LOOKUPS['pub_date']['values_dict']
            assert pub_date not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{pub_date}". `{node_target}` cannot be blank.'
            assert isinstance(pub_date, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(pub_date)}: {pub_date}.\Publication date must be of type str.\nE.g., myemld.set_pub_date(pub_date="2022-01-01") or myemld.set_pub_date(pub_date="Jan 2022")'

            values['pubDate'] = pub_date
            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
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

    def get_author(self):
        """Get information about the dataset's author

        Note: EML 'author' and 'creator' are the same thing.

        Args:
            None

        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_author()
        """
        try:
            self.get_creator()
        except:
            print('error get_author()')

    def set_author(self, first:str=None, last:str=None, org:str=None, email:str=None):
        """Specify the dataset author's name, organization, and email

        Note: EML 'author' and 'creator' are the same thing.

        Args:
            first (str, optional): The dataset creator's first name. Defaults to None.
            last (str, optional): The dataset creator's last name. Defaults to None.
            org (str, optional): The dataset creator's organization (e.g., company, government agency). Defaults to None.
            email (str, optional): The dataset creator's email address. Defaults to None.

        Examples:
            myemld.set_author(first='Albus', last='Fumblesnore')
        """
        try:
            self.set_creator(first=first, last=last, org=org, email=email)
        except:
            print('error set_author()')

    def delete_author(self):
        """Delete information about the dataset creator

        Args:
            None

        Examples:
            myemld.delete_author()
        """
        try:
            self.delete_creator()
        except:
            print('error delete_author()')

    def get_temporal_coverage(self):
        """Get the dataset's temporal coverage

        EML temporal coverage is the date range (i.e., min and max date) of the dataset.

        Args:
            None

        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_temporal_coverage()
        """
        try:
            node_xpath = LOOKUPS['temporal_coverage']['node_xpath']
            node_target= LOOKUPS['temporal_coverage']['node_target']
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
            print('problem get_temporal_coverage()')

    def set_temporal_coverage(self, begin_date:str=None, end_date:str=None):
        try:
            assert begin_date not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{begin_date}". `{node_target}` cannot be blank.'
            assert isinstance(begin_date, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(begin_date)}: {begin_date}.\Dates must be of type str.\nE.g., myemld.set_temporal_coverage(begin_date="2021")'
            assert end_date not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{end_date}". `{node_target}` cannot be blank.'
            assert isinstance(end_date, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(end_date)}: {end_date}.\Dates must be of type str.\nE.g., myemld.set_temporal_coverage(end_date="2021")'

            node_xpath = LOOKUPS['temporal_coverage']['node_xpath']
            node_target= LOOKUPS['temporal_coverage']['node_target']
            parent= LOOKUPS['temporal_coverage']['parent']
            dirty_vals = LOOKUPS['temporal_coverage']['values_dict']
            dirty_vals['temporalCoverage']['rangeOfDates']['beginDate']['calendarDate'] = begin_date
            dirty_vals['temporalCoverage']['rangeOfDates']['endDate']['calendarDate'] = end_date

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            cleanvals = self._delete_none(dirty_vals)
            self._set_node(values=cleanvals, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_temporal_coverage()
            
        except:
            print('error set_temporal_coverage()')

    def delete_temporal_coverage(self):
        """Delete dataset temporal coverage

        Args:
            None

        Examples:
            myemld.delete_temporal_coverage()
        """
        try:
            node_xpath = LOOKUPS['begin_end_date']['node_xpath']
            node_target= LOOKUPS['begin_end_date']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet)  

        except:
            print('error delete_temporal_coverage()')

    def get_cui(self):
        """Get the dataset's controlled unclassified information (CUI) status 

        Args:
            None

        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_cui()
        """
        try:
            node_xpath = LOOKUPS['cui']['node_xpath']
            node_target= LOOKUPS['cui']['node_target']
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
            print('problem get_cui()')

    def set_cui(self, cui:str):
        """Set the dataset's controlled unclassified information (CUI) status
        
        Args:
            cui (str): The value you want to assign as the dataset's CUI status. `cui` is validated against `src.pyEML.constants.CUI_CHOICES.keys()`.

        Examples:
            myemld.set_cui(cui='PUBLIC')
        """
        try:
            node_xpath = LOOKUPS['cui']['node_xpath']
            node_target= LOOKUPS['cui']['node_target']
            parent = LOOKUPS['cui']['parent']
            values = LOOKUPS['cui']['values_dict']
            assert cui in CUI_CHOICES.keys(), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}"{cui}" is an invalid `{bcolors.BOLD}{node_target}{bcolors.ENDC}`.\n{bcolors.OKBLUE}Find valid choices for `{bcolors.BOLD}{node_target}{bcolors.ENDC}` {bcolors.OKBLUE}by calling `myemld.describe_{node_target}()`{bcolors.ENDC}.'

            values['CUI'] = cui
            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_cui()
        
        except AssertionError as a:
            print(a)

    def delete_cui(self):
        """Delete dataset's controlled unclassified information (CUI) status
        
        Args:
            None

        Examples:
            myemld.delete_cui()
        """
        try:
            node_xpath = LOOKUPS['cui']['node_xpath']
            node_target= LOOKUPS['cui']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet) 
        except:
            print('error delete_cui()') 
    
    def get_int_rights(self):
        """Get the dataset's intellectual rights status

        Args:
            None

        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_int_rights()
        """
        try:
            node_xpath = LOOKUPS['int_rights']['node_xpath']
            node_target= LOOKUPS['int_rights']['node_target']
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
            print('problem get_int_rights()')

    def set_int_rights(self, license:str=LICENSE_TEXT):
        """Set the dataset's intellectual rights status
        
        Args:
            cui (str): The value you want to assign as the dataset's intellectual rights status. `license` is validated against `src.pyEML.constants.CUI_CHOICES`.

        Examples:
            myemld.set_int_rights(cui='CCzero')
            myemld.set_int_rights(cui='public_domain')
            myemld.set_int_rights(cui='restrict')
        """
        try:
            node_xpath = LOOKUPS['int_rights']['node_xpath']
            node_target= LOOKUPS['int_rights']['node_target']
            parent = LOOKUPS['int_rights']['parent']
            values = LOOKUPS['int_rights']['values_dict']
            assert license in LICENSE_TEXT, f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}"{license}" is an invalid `{bcolors.BOLD}{node_target}{bcolors.ENDC}`.\n{bcolors.OKBLUE}Find valid choices for `{bcolors.BOLD}{node_target}{bcolors.ENDC}` {bcolors.OKBLUE}by calling `myemld.describe_{node_target}()`{bcolors.ENDC}.'

            values['intellectualRights']['para'] = LICENSE_TEXT[license]
            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_int_rights()
        
        except AssertionError as a:
            print(a)

    def delete_int_rights(self):
        """Delete the dataset's intellectual rights status
        
        Args:
            None

        Examples:
            myemld.delete_int_rights()
        """
        try:
            node_xpath = LOOKUPS['int_rights']['node_xpath']
            node_target= LOOKUPS['int_rights']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet) 
        except:
            print('error delete_int_rights()') 
    
    def get_status(self):
        """Get the dataset's maintenance status status
        
        Args:
            None

        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_status()
        """
        try:
            node_xpath = LOOKUPS['status']['node_xpath']
            node_target= LOOKUPS['status']['node_target']
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
            print('problem get_status()')

    def set_status(self, status:str):
        """Set the dataset's maintenance status status

        Args:
            status (str): The dataset's maintenance status; 'complete' or 'incomplete'.

        Examples:
            myemld.set_status(status='complete')
            myemld.set_status(status='incomplete')
        """
        try:
            node_xpath = LOOKUPS['status']['node_xpath']
            node_target= LOOKUPS['status']['node_target']
            parent = LOOKUPS['status']['parent']
            values = LOOKUPS['status']['values_dict']
            assert status in ('complete', 'incomplete'), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}"{status}" is an invalid `{bcolors.BOLD}{node_target}{bcolors.ENDC}`.\n{bcolors.OKBLUE}Valid choices for `{bcolors.BOLD}{node_target}{bcolors.ENDC}` {bcolors.OKBLUE}are "complete" or "incomplete"{bcolors.ENDC}.'

            values['maintenance']['description'] = status
            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_status()
        
        except AssertionError as a:
            print(a)

    def delete_status(self):
        """Delete the dataset's maintenance status
        
        Args:
            None

        Examples:
            myemld.delete_status()
        """
        try:
            node_xpath = LOOKUPS['status']['node_xpath']
            node_target= LOOKUPS['status']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet) 
        except:
            print('error delete_status()') 
    
    def describe_cui(self):
        """Print the controlled unclassified information status pick-list to console

        Args:
            None

        Examples:
            myemld.describe_cui()

        """
        try:
            if self.interactive == True:
                print(f'`{bcolors.BOLD}CUI{bcolors.ENDC}` means controlled unclassified information. The following `{bcolors.BOLD}CUI{bcolors.ENDC}` choices are available in v. {CURRENT_RELEASE} of {APP_NAME}:')
                print('----------')
                for k, v in CUI_CHOICES.items():
                    print(f'\'{bcolors.BOLD}{k}{bcolors.ENDC}\': {v}\n')
        except:
            print('error describe_cui()')
    
    def describe_int_rights(self):
        """Print the intellectual rights pick-list to console

        Args:
            None

        Examples:
            myemld.describe_int_rights()

        """
        try:
            if self.interactive == True:
                print(f'The following `{bcolors.BOLD}intellectual rights{bcolors.ENDC}` license choices are available in v. {CURRENT_RELEASE} of {APP_NAME}:')
                print('----------')
                for k, v in LICENSE_TEXT.items():
                    print(f'\'{bcolors.BOLD}{k}{bcolors.ENDC}\': {v}\n')
        except:
            print('error descrbe_int_rights()')
    
    def describe_citation(self):
        """Print the citation choices pick-list to console

        Args:
            None

        Examples:
            myemld.describe_citation()

        """
        try:
            if self.interactive == True:
                print(f'The following `{bcolors.BOLD}citation styles{bcolors.ENDC}` choices are available in v. {CURRENT_RELEASE} of {APP_NAME}:')
                print('----------')
                for k, v in CITATION_STYLES.items():
                    print(f'\'{bcolors.BOLD}{k}{bcolors.ENDC}\': {v}\n')
        except:
            print('error descrbe_int_rights()')
    
    def get_doi(self):
        """Get the dataset's doi (digital object identifier)

        Args:
            None
        
        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_doi()
        """
        try:
            node_xpath = LOOKUPS['doi']['node_xpath']
            node_target= LOOKUPS['doi']['node_target']
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
            print('problem get_doi()')

    def set_doi(self, doi):
        """Set the dataset's doi (digital object identifier)

        Args:
            doi (str or int): A digital object identifier (doi); 7-digit unique identifier for a dataset. https://www.doi.org/

        Examples:
            myemld.set_doi(doi='1234567')
            myemld.set_doi(doi=1234567)
        """
        try:
            node_xpath = LOOKUPS['doi']['node_xpath']
            node_target= LOOKUPS['doi']['node_target']
            parent = LOOKUPS['doi']['parent']
            values = LOOKUPS['doi']['values_dict']
            assert isinstance(doi, (str, int)), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}"{doi}" is {type(doi)} which is invalid for `{bcolors.BOLD}{node_target}{bcolors.ENDC}`.\n{bcolors.OKBLUE}Valid `{bcolors.BOLD}{node_target}{bcolors.ENDC}`{bcolors.OKBLUE} values are of type str or int. E.g., "1234567" or 1234567{bcolors.ENDC}.'
            doi = str(doi)
            assert len(doi) == 7, f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}"{doi}" is an invalid `{bcolors.BOLD}{node_target}{bcolors.ENDC}`.\n{bcolors.OKBLUE}Valid `{bcolors.BOLD}{node_target}{bcolors.ENDC}`{bcolors.OKBLUE} values are seven characters long. E.g., "1234567" or 1234567{bcolors.ENDC}.'

            values['alternateIdentifier'] = doi # doi
            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_doi()
        
        except AssertionError as a:
            print(a)

    def delete_doi(self):
        """Delete the dataset's doi (digital object identifier)

        Args:
            None

        Examples:
            myemld.delete_doi()
        """
        try:
            node_xpath = LOOKUPS['doi']['node_xpath']
            node_target= LOOKUPS['doi']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet) 
        except:
            print('error delete_doi()') 
    
    def get_contact(self):
        """Get information about the dataset contact

        Args:
            None

        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_contact()
        """
        try:
            node_xpath = LOOKUPS['contact']['node_xpath']
            node_target= LOOKUPS['contact']['node_target']
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
            print('problem get_contact()')

    def set_contact(self, first:str=None, last:str=None, org:str=None, email:str=None):
        """Set information about the dataset contact

        Args:
            first (str, optional): The dataset contact's first name.. Defaults to None.
            last (str, optional): The dataset contact's last name.. Defaults to None.
            org (str, optional): The dataset contact's organization (e.g., company, government agency). Defaults to None.
            email (str, optional): The dataset creator's email address. Defaults to None.

        Examples:
            myemld.set_contact(first='Albus', last='Fumblesnore')
        """
        try:
            node_xpath = LOOKUPS['contact']['node_xpath']
            node_target= LOOKUPS['contact']['node_target']
            parent= LOOKUPS['contact']['parent']
            dirty_vals = LOOKUPS['contact']['values_dict']
            
            if first not in (None, ''):
                assert isinstance(first, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(first)}: {first}.\nFirst name must be of type str.\nE.g., myemld.set_contact(first="Albus")'
                dirty_vals['contact']['individualName']['givenName'] = first
            if last not in (None, ''):
                assert isinstance(last, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(last)}: {last}.\Last name must be of type str.\nE.g., myemld.set_contact(last="Fumblesnore")'
                dirty_vals['contact']['individualName']['surName'] = last
            if org not in (None, ''):
                assert isinstance(org, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(org)}: {org}.\Organization name must be of type str.\nE.g., myemld.set_contact(org="House Gryffinsnore")'
                dirty_vals['contact']['organizationName'] = org
            if email not in (None, ''):
                assert isinstance(email, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(email)}: {email}.\Email must be of type str.\nE.g., myemld.set_contact(email="wellsley.r@gryffinsnore.edu")'
                dirty_vals['contact']['electronicMailAddress'] = email

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            cleanvals = self._delete_none(dirty_vals)
            self._set_node(values=cleanvals, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_contact()
            
        except AssertionError as a:
            print(a)
        except:
            print('error set_contact()')

    def delete_contact(self):
        """Delete information about the dataset contact

        Args:
            None

        Examples:
            myemld.delete_creator()
        """
        try:
            node_xpath = LOOKUPS['contact']['node_xpath']
            node_target= LOOKUPS['contact']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet)  

        except:
            print('error delete_contact()')
    
    def get_usage_citation(self):
        """Get the dataset's usage citation

        Args:
            None
        
        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_usage_citation()
        """
        try:
            node_xpath = LOOKUPS['usage_citation']['node_xpath']
            node_target= LOOKUPS['usage_citation']['node_target']
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
            print('problem get_usage_citation()')

    def set_usage_citation(self, alt_id:str=None, title:str=None, creator:str=None, report:str=None, id:str=None):
        """Set the dataset's usage citation

        Args:
            alt_id (str, optional): The url to the dataset. E.g., https://doi.org/10.36967/1234567. Defaults to None.
            title (str, optional): The title given to the dataset at `alt_id`. Defaults to None.
            creator (str, optional): The metadata creator's name. Usually the same first and last name as `myemld.get_creator()`. Defaults to None.
            report (str, optional): Dataset's digital object identifier. Usually the same as `myemld.get_doi()`. Defaults to None.
            id (str, optional): A unique identifier for the usage citation so it can be referenced as a unit from within the metadata package. Defaults to None.

        Examples:
            myemld.set_usage_citation(alt_id='https://doi.org/10.36967/1234567', title='My data product', creator='Albus', report='1234567', id='associatedDRR')
            myemld.set_usage_citation(alt_id='https://doi.org/10.36967/1234567')
        """
        try:
            node_xpath = LOOKUPS['usage_citation']['node_xpath']
            node_target= LOOKUPS['usage_citation']['node_target']
            parent= LOOKUPS['usage_citation']['parent']
            dirty_vals = LOOKUPS['usage_citation']['values_dict']
            
            if alt_id not in (None, ''):
                assert isinstance(alt_id, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(alt_id)}: {alt_id}.\nDOI (digital object identifier) url name must be of type str.\nE.g., myemld.set_{node_target}(alt_id="https://doi.org/10.36967/1234567")'
                dirty_vals['usageCitation']['alternateIdentifier'] = alt_id
            if title not in (None, ''):
                assert isinstance(title, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(title)}: {title}.\nTitle name must be of type str.\nE.g., myemld.set_{node_target}(title="My dataset title")'
                dirty_vals['usageCitation']['title'] = title
            if creator not in (None, ''):
                assert isinstance(creator, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(creator)}: {creator}.\nCreator name must be of type str.\nE.g., myemld.set_{node_target}(creator="Albus")'
                dirty_vals['usageCitation']['creator'] = creator
            if report not in (None, ''):
                assert isinstance(report, (str, int)), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(report)}: {report}.\nReport must be of type str or int.\nE.g., myemld.set_{node_target}(report="1234567") or myemld.set_{node_target}(report=1234567)'
                report = str(report)
                dirty_vals['usageCitation']['report'] = report
            if id not in (None, ''):
                assert isinstance(id, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(id)}: {id}.\ID must be of type str.\nE.g., myemld.set_{node_target}(id="associatedDRR")'
                dirty_vals['usageCitation']['id'] = id

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            cleanvals = self._delete_none(dirty_vals)
            self._set_node(values=cleanvals, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_usage_citation()
        except AssertionError as a:
            print(a)
        except:
            print('error set_usage_citation()')
        
    def delete_usage_citation(self):
        """Delete the dataset's usage citation

        Args:
            None

        Examples:
            myemld.delete_usage_citation()
        """
        try:
            node_xpath = LOOKUPS['usage_citation']['node_xpath']
            node_target= LOOKUPS['usage_citation']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet) 
        except:
            print('error usage_citation()') 

    def get_protocol_citation(self):
        """Get the dataset's protocol citation

        Args:
            None
        
        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_protocol_citation()
        """
        try:
            node_xpath = LOOKUPS['protocol_citation']['node_xpath']
            node_target= LOOKUPS['protocol_citation']['node_target']
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
            print('problem get_protocol_citation()')

    def set_protocol_citation(self, authors:list=None, title:str=None, date:str=None, version:str=None, doc_type:str=None, url:str=None, etc:str=None, style:str=None):
        """Set the dataset's protocol citation

        Takes in pieces of a citation and formats those pieces into a paragraph citation matching the specified citation `style`.

        Args:
            authors (list of dicts, optional): A list of dictionaries. Each dictionary contains author names. See Examples. Defaults to None.
            title (str, optional): The protocol title. Defaults to None.
            date (str, optional): The protocol publication date in YYYY-MM-DD format. Defaults to None.
            version (str, optional): The protocol version number. Defaults to None.
            doc_type (str, optional): The document type of the protocol. Defaults to None.
            url (str, optional): The url of the protocol. Defaults to None.
            etc (str, optional): Additional information to append to the end of the citation. Defaults to None.
            style (str, optional): The style of the citation to be generated. Defaults to None.

        Examples:
            myauthors = [
                    {
                        'first': 'First author's first name',
                        'last': 'First author's last name'
                    },
                    {
                        'first': 'Second author's first name',
                        'middle': 'Second author's middle name',
                        'last': 'Second author's last name'
                    },
                    {
                        'last': 'Third author's last name'
                    }
                ]
            myemld.set_protocol_citation(
                authors=myauthors,
                title='My dataset protocol title',
                version='1.0',
                date='2021-01-01',
                style='chicago'
                )
        """
        try:
            # validate
            if authors is not None:
                assert isinstance(authors, (list, tuple)), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(authors)}: {authors}.\Author names must be a list of dicts or tuple of dicts.\nE.g.,\nmyemld.set_{node_target}(authors=[{"first": "Albus", "last": "Fumblesnore"}, {"first": "Ronaldus", "middle": "Albert", "last": "Weaslee"}])'   
                for element in authors:
                    assert isinstance(element, dict), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(element)}: {element}.\Author names must be a list of dicts or tuple of dicts.\nE.g.,\nmyemld.set_{node_target}(authors=[{"first": "Albus", "last": "Fumblesnore"}, {"first": "Ronaldus", "middle": "Albert", "last": "Weaslee"}])'   
                    for name in element:
                        assert isinstance(name, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(name)}: {name}.\Author first and last name must type str.\nE.g.,\nmyemld.set_{node_target}(authors=[{"first": "Albus", "last": "Fumblesnore"}, {"first": "Ronaldus", "middle": "Albert", "last": "Weaslee"}])'       
                        assert name not in ('', 'None', 'NA', 'na', 'NaN'), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {name}.\Author first and last name cannot be blank.\nE.g.,\nmyemld.set_{node_target}(authors=[{"first": "Albus", "last": "Fumblesnore"}, {"first": "Ronaldus", "middle": "Albert", "last": "Weaslee"}])'       
            
            if title is not None:
                assert isinstance(title, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(title)}: {title}.\Title must be of type str.\nE.g., myemld.set_{node_target}(title="Monitoring data 2022")'
                assert title not in ('', 'None', 'NA', 'na', 'NaN'), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {title}.\Title cannot be blank.\nE.g.,\nmyemld.set_{node_target}(title="Monitoring data 2022")'  
            
            if date is not None:
                assert isinstance(date, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(date)}: {date}.\Date must be of type str.\nE.g., myemld.set_{node_target}(date="2022-01-01")'
                assert date not in ('', 'None', 'NA', 'na', 'NaN'), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {date}.\Date cannot be blank.\nE.g.,\nmyemld.set_{node_target}(date="2022-01-01")'  
                newdate = datetime.strptime(date, "%Y-%m-%d").date()

            if version is not None:
                assert isinstance(version, (str, int, float)), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(version)}: {version}.\Version must be of type str.\nE.g., myemld.set_{node_target}(version="1.1")'
                version = str(version)
                assert version not in ('', 'None', 'NA', 'na', 'NaN'), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {version}.\Version cannot be blank.\nE.g.,\nmyemld.set_{node_target}(version="1.1")'  
            
            if doc_type is not None:
                assert isinstance(doc_type, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(doc_type)}: {doc_type}.\Document type must be of type str.\nE.g., myemld.set_{node_target}(doc_type="document reference report)'
                assert doc_type not in ('', 'None', 'NA', 'na', 'NaN'), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {doc_type}.\Document type cannot be blank.\nE.g.,\nmyemld.set_{node_target}(doc_type="document reference report")'  
            
            if url is not None:
                assert isinstance(url, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(url)}: {url}.\nURL must be of type str.\nE.g., myemld.set_{node_target}(url="doi.org/1234567")'
                assert url not in ('', 'None', 'NA', 'na', 'NaN'), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {url}.\nURL cannot be blank.\nE.g.,\nmyemld.set_{node_target}(url="doi.org/1234567")'  
            
            assert style in CITATION_STYLES.keys(), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {style} for `style`.\nYou must choose a citation `style` from the pick-list.\nCall `myemld.describe_citation()` to view the pick-list.'  
            # `style` validated against src.pyEML.constants.CITATION_STYLES

            # assemble variables
            node_xpath = LOOKUPS['protocol_citation']['node_xpath']
            node_target= LOOKUPS['protocol_citation']['node_target']
            parent= LOOKUPS['protocol_citation']['parent']
            values = LOOKUPS['protocol_citation']['values_dict']

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            dirty_vals = {}
            if authors:
                dirty_vals['authors'] = authors
            if title:
                dirty_vals['title'] = title
            if date:
                dirty_vals['date'] = newdate
            if version:
                dirty_vals['version'] = version
            if doc_type:
                dirty_vals['doc_type'] = doc_type
            if url:
                dirty_vals['url'] = url
            
            # clean varaibles
            cleanvals = self._delete_none(dirty_vals) # delete empty nodes

            # generate citation paragraph
            values['para'] = self._make_citation(citation_parts=cleanvals, style=style) # make paragraph from `cleanvals` dict

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_protocol_citation()

        except AssertionError as a:
            print(a)
        except ValueError as e:
            print(e)
            print('Dates must be in YYYY-MM-DD format.')
        except:
            print('problem set_protocol_citation()')

    def delete_protocol_citation(self):
        """Delete the dataset's protocol citation

        Args:
            None

        Examples:
            myemld.delete_protocol_citation()
        """
        try:
            node_xpath = LOOKUPS['protocol_citation']['node_xpath']
            node_target= LOOKUPS['protocol_citation']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet) 
        except:
            print('error delete_protocol_citation()') 
    
    def get_abstract(self):
        """Get the dataset's abstract

        Args:
            None
        
        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_abstract()
        """
        try:
            node_xpath = LOOKUPS['abstract']['node_xpath']
            node_target= LOOKUPS['abstract']['node_target']
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
            print('problem get_abstract()')

    def set_abstract(self, abstract:str):
        """Set the dataset's abstract
        
        Args:
            title (str): The title that you want to assign to your dataset.

        Examples:
            myemld.set_title(title='my new title')
        """
        try:
            node_xpath = LOOKUPS['abstract']['node_xpath']
            node_target= LOOKUPS['abstract']['node_target']
            parent = LOOKUPS['abstract']['parent']
            values = LOOKUPS['abstract']['values_dict']
            assert abstract not in ('', None, 'NA', 'na', 'NaN'), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{abstract}". `{node_target}` cannot be blank.'

            values['abstract']['para'] = abstract
            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_abstract()
        
        except AssertionError as a:
            print(a)

    def delete_abstract(self):
        """Delete the dataset's protocol citation

        Args:
            None

        Examples:
            myemld.delete_abstract()
        """
        try:
            node_xpath = LOOKUPS['abstract']['node_xpath']
            node_target= LOOKUPS['abstract']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet) 
        except:
            print('error delete_abstract()') 
    
    def get_attributes(self):
        """Get the dataset's xml attributes

        Args:
            None
        
        Returns:
            str: xml attribute names and values printed to console

        Examples:
            myemld.get_abstract()
        """
        try:
            if self.interactive == True:
                for attribute in self.root.keys():
                    if attribute in AVAILABLE_ATTRIBUTES: # stops program from showing namespaces
                        print(f'{attribute}={self.root.get(attribute)}')

        except:
            print('error get_attributes()')

    def set_attribute(self, attribute:str, value:str):
        """Set the dataset's xml attributes

        Args:
            attribute (str): The name of the attribute to set.
            value (str): The value to assign at `attribute`.

        Examples:
            myemld.set_attribute(
                attribute='packageId',
                value='newvalue'
            )
        """
        try:
            assert attribute in AVAILABLE_ATTRIBUTES.keys(), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided `attribute` "{attribute}".\nOnly valid attributes can be set.\nUse `myemld.get_attributes()` to see which attributes your dataset has or delete all attributes:\nmyemld.delete_attribute(attribute="all").\nCall `myemld.describe_attributes()` for a pick-list of attributes and their descriptions.'
            assert value not in (None, '', 'NA', 'Na', 'NaN'), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided `attribute` "{attribute}".\nAttributes cannot be blank.\nYou can delete attributes via:\nmyemld.delete_attribute().\nCall `myemld.describe_attributes()` for a pick-list of attributes and their descriptions.'

            if self.interactive == True:
                if attribute in self.root.keys():
                    print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nYou are about to overwrite a metadata `{bcolors.BOLD}attribute{bcolors.ENDC}`:')
                    print(f'{attribute}={self.root.get(attribute)}\n')
                    overwrite = input(f'{bcolors.BOLD}Do you want to delete this attribute?\n{bcolors.ENDC}("{bcolors.BOLD}y{bcolors.ENDC}" to delete, "{bcolors.BOLD}n{bcolors.ENDC}" to cancel.)\n\n')
                    print(f'User input: {overwrite}\n')
                    if overwrite.lower() == 'y':
                        force=True
                    else:
                        print(f'`{bcolors.BOLD}attribute{bcolors.ENDC}` deletion cancelled.')
                        force=False
            else:
                force = True

            if force == True:
                self.root.set(attribute, value)
                if self.interactive == True:
                    print(f'`{bcolors.BOLD}{attribute}{bcolors.ENDC}` set:')
                    print(f'{attribute}={self.root.get(attribute)}')

        except AssertionError as a:
            print(a)
        except:
            print('problem set_attributes()')

    def delete_attribute(self, attribute:str):
        """Delete one or more of the dataset's xml attributes

        Args:
            attribute (str): The name of the attribute to delete.
        """
        try:
            newlist = AVAILABLE_ATTRIBUTES.keys().copy()
            newlist.append('all')
            assert attribute in (newlist), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided `attribute` "{attribute}".\nOnly valid attributes or "all" attributes can be deleted.\nUse `myemld.get_attributes()` to see which attributes your dataset has or delete all attributes:\nmyemld.delete_attribute(attribute="all").\nCall `myemld.describe_attributes()` for a pick-list of attributes and their descriptions.'
            assert attribute in self.root.keys(), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided `attribute` "{attribute}".\nYour dataset does not have an `attribute` {attribute}.\nUse `myemld.get_attributes()` to see which attributes your dataset has or delete all attributes:\nmyemld.delete_attribute(attribute="all").\nCall `myemld.describe_attributes()` for a pick-list of attributes and their descriptions.'

            if self.interactive == True:
                if attribute == 'all':
                    print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nYou are about to delete all of your metadata `{bcolors.BOLD}attributes{bcolors.ENDC}`:')
                    self.get_attributes()
                    overwrite = input(f'{bcolors.BOLD}Do you want to delete all attributes?\n{bcolors.ENDC}("{bcolors.BOLD}y{bcolors.ENDC}" to delete, "{bcolors.BOLD}n{bcolors.ENDC}" to cancel.)\n\n')
                else:
                    print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nYou are about to delete a metadata `{bcolors.BOLD}attribute{bcolors.ENDC}`:')
                    print(f'{attribute}={self.root.get(attribute)}')
                    overwrite = input(f'{bcolors.BOLD}Do you want to delete this attribute?\n{bcolors.ENDC}("{bcolors.BOLD}y{bcolors.ENDC}" to delete, "{bcolors.BOLD}n{bcolors.ENDC}" to cancel.)\n\n')
                print(f'User input: {overwrite}')
                if overwrite.lower() == 'y':
                    force=True
                else:
                    print(f'`{bcolors.BOLD}attribute{bcolors.ENDC}` deletion cancelled.')
                    force=False
            else:
                force=True

            if force == True:
                deleted_attributes = []
                if attribute == 'all':
                    for attribute in self.root.keys():
                        if attribute in AVAILABLE_ATTRIBUTES.keys(): # don't delete namespaces
                            del self.root.attrib[attribute]
                            deleted_attributes.append(attribute)
                else:
                    del self.root.attrib[attribute]
                    deleted_attributes.append(attribute)
                if self.interactive == True:
                    print(f'`{bcolors.BOLD}attributes{bcolors.ENDC}` deleted:')
                    for att in deleted_attributes:
                        print(att)
            
        except AssertionError as a:
            print(a)
        except:
            print('problem delete_attribute()')

    def get_lit_cited(self):
        """Get the dataset's cited literature

        Args:
            None
        
        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_lit_cited()
        """
        try:
            node_xpath = LOOKUPS['lit_cited']['node_xpath']
            node_target= LOOKUPS['lit_cited']['node_target']
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
            print('problem get_lit_cited()')

    def set_lit_cited(self, citations:list):
        """Set the dataset's cited literature

        Args:
            citations (list): A list strings. Each string is one pre-formatted citation.

        Examples:
            mycitations = [
                '
                @BOOK{Person2021,
                title="This is another article title",
                author="Person",
                year="2021"
                '
                ]
            myemld.set_lit_cited(self, citations=mycitations)
        """
        try:
            node_xpath = LOOKUPS['lit_cited']['node_xpath']
            node_target= LOOKUPS['lit_cited']['node_target']
            parent= LOOKUPS['lit_cited']['parent']

            assert isinstance(citations, list), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{citations}". {node_target} must be a list.'
            for citation in citations:
                assert citation not in ('', None), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{citation}". Citations cannot be blank.'
                assert isinstance(citation, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(citation)}: {citation}.\nEach citation must be type str.'
            
            values = LOOKUPS['lit_cited']['values_dict']
            values['literatureCited']['bibtex'] = citations

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)

            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_lit_cited()

        except AssertionError as a:
            print(a)

    def delete_lit_cited(self):
        """Delete the dataset's cited literature

        Args:
            None

        Examples:
            myemld.delete_lit_cited()
        """
        try:
            node_xpath = LOOKUPS['lit_cited']['node_xpath']
            node_target= LOOKUPS['lit_cited']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet) 
        except:
            print('error delete_lit_cited()') 
    
    def get_language(self):
        """Get the dataset's language

        Args:
            None
        
        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_language()
        """
        try:
            node_xpath = LOOKUPS['language']['node_xpath']
            node_target= LOOKUPS['language']['node_target']
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
            print('problem get_language()')

    def set_language(self, language:str):
        """Set the dataset's language
        
        Args:
            languge (str): The language that you want to assign to your dataset. Example: 'english' or 'spanish'

        Examples:
            myemld.set_language(language='english')
            myemld.set_language(language='spanish')
        """
        try:
            node_xpath = LOOKUPS['language']['node_xpath']
            node_target= LOOKUPS['language']['node_target']
            parent = LOOKUPS['language']['parent']
            values = LOOKUPS['language']['values_dict']
            assert language not in ('', None, 'NA', 'Na', 'NaN'), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{language}". `{node_target}` cannot be blank.'
            assert isinstance(language, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(language)}: "{language}". `{node_target}` must be type str.'
            assert len(language) >= 3, f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{language}". {bcolors.BOLD}`{node_target}`{bcolors.ENDC} must be at least three characters.'

             # API call to retrieve ISO 3-letter abbreviation for a language
            language_obj = iso639.languages.get(name=language.title()) # api call
            language_title = language_obj.part3 # parse api result
            assert len(language_title) == 3, f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}"{language}" was not found in the `{bcolors.BOLD}ISO 639-2 language database{bcolors.ENDC}`.\nExamples of valid languages: "english", "spanish".\nA full list of valid languages is at https://www.loc.gov/standards/iso639-2/php/code_list.php'

            values['language'] = language_title

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_language()
        
        except AssertionError as a:
            print(a)

    def delete_language(self):
        """Delete the dataset's language

        Args:
            None

        Examples:
            myemld.delete_language()
        """
        try:
            node_xpath = LOOKUPS['language']['node_xpath']
            node_target= LOOKUPS['language']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet) 
        except:
            print('error delete_language()') 
    
    def get_geographic_coverage(self):
        """Get the dataset's geographic coverage

        Args:
            None
        
        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_geographic_coverage()
        """
        try:
            node_xpath = LOOKUPS['geographic_coverage']['node_xpath']
            node_target= LOOKUPS['geographic_coverage']['node_target']
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
            print('problem get_geographic_coverage()')

    def set_nps_geographic_coverage(self, *unit_codes:str):
        """Retrieve bounding box coordinates for NPS parks and assign coordinates as geographic coverage

        Args:
            *unit_codes (str, arbitrary argument): `set_nps_geographic_coverage()` accepts any number of comma-separated arguments. Each argument is one four-character USNPS park code. E.g., set_nps_geographic_coverage("GLAC", "ACAD")

        Examples:
            myemld.set_nps_geographic_coverage('GLAC', 'ACAD')
        """
        try:
            for unit in unit_codes:
                assert unit not in ('', None, 'NA', 'Na', 'NaN'), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{unit}". `{node_target}` cannot be blank.'
                assert isinstance(unit, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(unit)}: "{unit}". `{node_target}` must be type str.'
                assert len(unit) == 4, f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{unit}". {bcolors.BOLD}`{node_target}`{bcolors.ENDC} must be four characters.\nE.g., "GLAC", "ACAD"'

            # API call
            geog_cov = self._content_units_api(unit_codes)

            node_xpath = LOOKUPS['geographic_coverage']['node_xpath']
            node_target= LOOKUPS['geographic_coverage']['node_target']
            parent= LOOKUPS['geographic_coverage']['parent']
            values = LOOKUPS['geographic_coverage']['values_dict']
            values['geographicCoverage'] = geog_cov

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)

            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_geographic_coverage()


        except AssertionError as a:
            print(a)

    def set_geographic_coverage(self, coverage:list):
        """Set the dataset's geographic coverage

        Args:
            coverage (dict): A dict of dicts. Each interior dict key is a unique ID for a geographic coverage area.
                Each interior dict contains the decimal degree bounding box coordinates and description for one geographic coverage area.
                'geographicDescription' is type str. Individual 'boundingCoordinates' can be type str, int, or float.

        Examples:
            mycoverage = {
                'area1': {
                    'geographicDescription': 'A box around sampling area1',
                    'boundingCoordinates': {
                        'westBoundingCoordinate': '-78.7348',
                        'eastBoundingCoordinate': '-76.758602',
                        'northBoundingCoordinate': 39.6924,
                        'southBoundingCoordinate': 38.545057
                    }
                }
            }

            myemld.set_geographic_coverage(coverage=mycoverage)
        """
        try:
            assert isinstance(coverage, dict), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(coverage)}: "{coverage}". `coverage` must be type dict.\nSee examples for details.'
            for unit in coverage.values():
                assert isinstance(unit, dict), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(unit)}: "{unit}". Each element in `coverage` must be type dict.\nSee examples for details.'
                assert len(unit) == 2, f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}Element {unit} has keys {unit.keys()}. Each element in `coverage` must be type dict with two keys: "geographicDescription" and "boundingCoordinates".\nSee examples for details.'
                assert 'geographicDescription' in unit.keys(), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}Element {unit} has keys {unit.keys()}. Each element in `coverage` must be type dict with two keys: "geographicDescription" and "boundingCoordinates".\nSee examples for details.'
                assert 'boundingCoordinates' in unit.keys(), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}Element {unit} has keys {unit.keys()}. Each element in `coverage` must be type dict with two keys: "geographicDescription" and "boundingCoordinates".\nSee examples for details.'
                assert isinstance(unit['geographicDescription'], str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(unit["geographicDescription"])}: "geographicDescription" must be type str.\nSee examples for details.'
                assert isinstance(unit['boundingCoordinates'], dict), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(unit["boundingCoordinates"])}: "boundingCoordinates" must be type dict.\nSee examples for details.'
                assert 'westBoundingCoordinate' in unit['boundingCoordinates'].keys(), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}Element {unit["boundingCoordinates"]} has keys {unit["boundingCoordinates"].keys()}. Each element in `boundingCoordinates` must be type dict with four keys: "westBoundingCoordinate", "eastBoundingCoordinate", "northBoundingCoordinate", and "southBoundingCoordinate".\nSee examples for details.'
                assert 'eastBoundingCoordinate' in unit['boundingCoordinates'].keys(), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}Element {unit["boundingCoordinates"]} has keys {unit["boundingCoordinates"].keys()}. Each element in `boundingCoordinates` must be type dict with four keys: "westBoundingCoordinate", "eastBoundingCoordinate", "northBoundingCoordinate", and "southBoundingCoordinate".\nSee examples for details.'
                assert 'northBoundingCoordinate' in unit['boundingCoordinates'].keys(), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}Element {unit["boundingCoordinates"]} has keys {unit["boundingCoordinates"].keys()}. Each element in `boundingCoordinates` must be type dict with four keys: "westBoundingCoordinate", "eastBoundingCoordinate", "northBoundingCoordinate", and "southBoundingCoordinate".\nSee examples for details.'
                assert 'southBoundingCoordinate' in unit['boundingCoordinates'].keys(), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}Element {unit["boundingCoordinates"]} has keys {unit["boundingCoordinates"].keys()}. Each element in `boundingCoordinates` must be type dict with four keys: "westBoundingCoordinate", "eastBoundingCoordinate", "northBoundingCoordinate", and "southBoundingCoordinate".\nSee examples for details.'
                assert isinstance(unit['boundingCoordinates']['westBoundingCoordinate'], (str, float, int)), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(unit["boundingCoordinates"]["westBoundingCoordinate"])}: "westBoundingCoordinate" must be type str, int, or float.\nSee examples for details.'
                unit['boundingCoordinates']['westBoundingCoordinate'] = str(unit['boundingCoordinates']['westBoundingCoordinate'])
                assert isinstance(unit['boundingCoordinates']['eastBoundingCoordinate'], (str, float, int)), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(unit["boundingCoordinates"]["eastBoundingCoordinate"])}: "eastBoundingCoordinate" must be type str, int, or float.\nSee examples for details.'
                unit['boundingCoordinates']['eastBoundingCoordinate'] = str(unit['boundingCoordinates']['eastBoundingCoordinate'])
                assert isinstance(unit['boundingCoordinates']['northBoundingCoordinate'], (str, float, int)), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(unit["boundingCoordinates"]["northBoundingCoordinate"])}: "northBoundingCoordinate" must be type str, int, or float.\nSee examples for details.'
                unit['boundingCoordinates']['northBoundingCoordinate'] = str(unit['boundingCoordinates']['northBoundingCoordinate'])
                assert isinstance(unit['boundingCoordinates']['southBoundingCoordinate'], (str, float, int)), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(unit["boundingCoordinates"]["southBoundingCoordinate"])}: "southBoundingCoordinate" must be type str, int, or float.\nSee examples for details.'
                unit['boundingCoordinates']['southBoundingCoordinate'] = str(unit['boundingCoordinates']['southBoundingCoordinate'])

            node_xpath = LOOKUPS['geographic_coverage']['node_xpath']
            node_target= LOOKUPS['geographic_coverage']['node_target']
            parent= LOOKUPS['geographic_coverage']['parent']
            values = LOOKUPS['geographic_coverage']['values_dict']
            values['geographicCoverage'] = coverage

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)

            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_geographic_coverage()
            
        except AssertionError as a:
            print(a)
    
    def delete_geographic_coverage(self):
        """Delete the dataset's geographic coverage

        Args:
            None

        Examples:
            myemld.delete_geographic_coverage()
        """
        try:
            node_xpath = LOOKUPS['geographic_coverage']['node_xpath']
            node_target= LOOKUPS['geographic_coverage']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet) 
        except:
            print('error delete_geographic_coverage()') 
    
    def get_metadata_provider(self):
        """Get the dataset's metadata provider

        This is usually the same person as the dataset creator. (i.e., myemld.get_creator())

        Args:
            None
        
        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_metadata_provider()
        """
        try:
            node_xpath = LOOKUPS['metadata_provider']['node_xpath']
            node_target= LOOKUPS['metadata_provider']['node_target']
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
            print('problem get_metadata_provider()')

    def set_metadata_provider(self, first:str=None, last:str=None, org:str=None, email:str=None):
        """Specify the metadata provider's name, organization, and email

        Args:
            first (str, optional): The dataset metadata provider's first name. Defaults to None.
            last (str, optional): The dataset metadata provider's last name. Defaults to None.
            org (str, optional): The dataset metadata provider's organization (e.g., company, government agency). Defaults to None.
            email (str, optional): The dataset metadata provider's email address. Defaults to None.

        Examples:
            myemld.set_metadata_provider(first='Albus', last='Fumblesnore')
        """
        try:
            node_xpath = LOOKUPS['metadata_provider']['node_xpath']
            node_target= LOOKUPS['metadata_provider']['node_target']
            parent= LOOKUPS['metadata_provider']['parent']
            dirty_vals = LOOKUPS['metadata_provider']['values_dict']
            
            entries = []
            if first not in (None, ''):
                assert isinstance(first, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(first)}: {first}.\nFirst name must be of type str.\nE.g., myemld.set_metadata_provider(first="Albus")'
                dirty_vals['metadataProvider']['individualName']['givenName'] = first
                entries.append(True)
            if last not in (None, ''):
                assert isinstance(last, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(last)}: {last}.\Last name must be of type str.\nE.g., myemld.set_metadata_provider(last="Fumblesnore")'
                dirty_vals['metadataProvider']['individualName']['surName'] = last
                entries.append(True)
            if org not in (None, ''):
                assert isinstance(org, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(org)}: {org}.\Organization name must be of type str.\nE.g., myemld.set_metadata_provider(org="House Gryffinsnore")'
                dirty_vals['metadataProvider']['organizationName'] = org
                entries.append(True)
            if email not in (None, ''):
                assert isinstance(email, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(email)}: {email}.\Email must be of type str.\nE.g., myemld.set_metadata_provider(email="wellsley.r@gryffinsnore.edu")'
                dirty_vals['metadataProvider']['electronicMailAddress'] = email
                entries.append(True)

            assert any(entries), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided no values to set.'

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            cleanvals = self._delete_none(dirty_vals)
            self._set_node(values=cleanvals, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)
            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_metadata_provider()
            
        except AssertionError as a:
            print(a)
        except:
            print('error set_metadata_provider()')

    def delete_metadata_provider(self):
        """Delete the dataset's metadata provider

        This is usually the same person as the dataset creator. (i.e., myemld.get_creator())

        Args:
            None

        Examples:
            myemld.delete_metadata_provider()
        """
        try:
            node_xpath = LOOKUPS['metadata_provider']['node_xpath']
            node_target= LOOKUPS['metadata_provider']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet) 
        except:
            print('error delete_metadata_provider()') 
    
    def get_nps_producing_units(self):
        """Get park codes as metadata providers

        Args:
            None
        
        Returns:
            str: If pretty == True
            lxml.etree.Element: If pretty == False

        Examples:
            myemld.get_nps_producing_units()
        """
        try:
            node_xpath = LOOKUPS['nps_producing_units']['node_xpath']
            node_target= LOOKUPS['nps_producing_units']['node_target']
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
            print('problem get_nps_producing_units()')
    
    def set_nps_producing_units(self, *unit_codes:str):
        """Set park codes as metadata providers

        Args:
            *unit_codes (str, arbitrary argument): `set_nps_producing_units()` accepts any number of comma-separated arguments. Each argument is one four-character USNPS park code. E.g., set_nps_geographic_coverage("GLAC", "ACAD")

        Examples:
            myemld.set_nps_producing_units('GLAC', 'ACAD')
        """
        try:
            for unit in unit_codes:
                assert unit not in ('', None, 'NA', 'Na', 'NaN'), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{unit}". `{node_target}` cannot be blank.'
                assert isinstance(unit, str), f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided {type(unit)}: "{unit}". `{node_target}` must be type str.'
                assert len(unit) == 4, f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{unit}". {bcolors.BOLD}`{node_target}`{bcolors.ENDC} must be four characters.\nE.g., "GLAC", "ACAD"'

            node_xpath = LOOKUPS['nps_producing_units']['node_xpath']
            node_target= LOOKUPS['nps_producing_units']['node_target']
            parent= LOOKUPS['nps_producing_units']['parent']
            values = LOOKUPS['nps_producing_units']['values_dict']

            values['metadataProvider']['unit'] = unit_codes

            if self.interactive == True:
                quiet=False
            else:
                quiet=True

            self._set_node(values=values, node_target=node_target, node_xpath=node_xpath, parent=parent, quiet=quiet)

            if self.interactive == True:
                print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!\n\n{bcolors.ENDC}`{bcolors.BOLD}{node_target}{bcolors.ENDC}` updated.')
                self.get_nps_producing_units()


        except AssertionError as a:
            print(a)
    
    def delete_nps_producing_units(self):
        """Delete park codes as metadata providers

        Args:
            None

        Examples:
            myemld.delete_nps_producing_units()
        """
        try:
            node_xpath = LOOKUPS['nps_producing_units']['node_xpath']
            node_target= LOOKUPS['nps_producing_units']['node_target']
            if self.interactive == True:
                quiet=False
            else:
                quiet=True
            self._delete_node(node_xpath=node_xpath, node_target=node_target, quiet=quiet) 
        except:
            print('error delete_nps_producing_units()') 
    
    def get_file_info(self):
        try:
            # define structure of final object
            myfile = {
                'title': None,
                'abstract': None,
                'size': None,
                'begin_date': None,
                'end_date': None
            }

            # assemble info to loop over
            objs_to_get = {
                'title': LOOKUPS['title'],
                'abstract': LOOKUPS['abstract'],
                'begin_date': LOOKUPS['temporal_coverage'],
                'end_date': LOOKUPS['temporal_coverage']
            }

            # loop to extract each node
            for k, v in objs_to_get.items():
                if k == 'abstract':
                    node_xpath = v['node_xpath'] + '/para'
                elif k == 'begin_date':
                    node_xpath = v['node_xpath'] + '/rangeOfDates/beginDate/calendarDate'
                elif k == 'end_date':
                    node_xpath = v['node_xpath'] + '/rangeOfDates/endDate/calendarDate'
                else:
                    node_xpath = v['node_xpath']
                node_target = v['node_target']
                node = self._get_node(node_xpath=node_xpath, node_target=node_target, pretty=False, quiet=True)
                if len(node) == 0:
                    if self.interactive == True:
                        print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nYour dataset does not have a `{bcolors.BOLD}{node_target}{bcolors.ENDC}` node.\nCall `set_{node_target}` to assign a value to {node_target}.')
                assert len(node) < 2, print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nYour dataset has {len(node)} `{bcolors.BOLD}{node_target}{bcolors.ENDC}` nodes.\nCall `get_{node_target} for more information.')
                myfile[k] = node[0]

            
            myfile['title'] = myfile['title'].text
            myfile['abstract'] = myfile['abstract'].text
            myfile['size'] = str(self._get_size()) + ' bytes'
            myfile['begin_date'] = myfile['begin_date'].text
            myfile['end_date'] = myfile['end_date'].text

            if self.interactive == True:
                print(json.dumps(myfile, indent=4))

        except AssertionError as a:
            print(a)
        except:
            print('error get_file_info()')
    
    def _get_size(self):
        """Get the size of an `Emld` element tree

        Returns:
            int: The size, in bytes, of the `Emld` element tree

        Examples:
            myemld._get_size()
        """
        # adapted from: https://stackoverflow.com/questions/449560/how-do-i-determine-the-size-of-an-object-in-python
        seen_ids = set()
        size = 0
        objects = [self.root]
        while objects:
            need_referents = []
            for obj in objects:
                if id(obj) not in seen_ids:
                    seen_ids.add(id(obj))
                    size += sys.getsizeof(obj)
                    need_referents.append(obj)
            objects = gc.get_referents(*need_referents)
        return size

    def describe_attributes(self):
        """Print the xml attribute pick-list

        Args:
            None

        Examples:
            myemld.describe_attributes()

        """
        try:
            if self.interactive == True:
                print(f'The following xml `{bcolors.BOLD}attributes{bcolors.ENDC}` can be edited in v. {CURRENT_RELEASE} of {APP_NAME}:')
                print('----------')
                for k, v in AVAILABLE_ATTRIBUTES.items():
                    print(f'\'{bcolors.BOLD}{k}{bcolors.ENDC}\': {v}\n')
        except:
            print('error describe_attributes()')

    def make_nps(self):
        """Update EML fields to match NPS spec

        Args:
            None

        Examples:
            myemld.make_nps()
        """
        try:
            updated_fields = {}
            missing_fields = []
            
            node_xpath = LOOKUPS['usage_citation']['node_xpath']
            node_target= LOOKUPS['usage_citation']['node_target']
            values = LOOKUPS['usage_citation']['values_dict']
            node = self._get_node(node_xpath=node_xpath, node_target=node_target, pretty=False, quiet=True)
            if node is not None and len(node) == 1:
                node = node[0]
                for child in node:
                    # change dataset['alternateIdentifier'] from {doi} to f'DRR: https://doi.org/10.36967/{doi}'
                    if child.tag == 'alternateIdentifier':
                        old = child.text
                        values['usageCitation']['alternateIdentifier'] = f'DRR: {old}' # doi
                        updated_fields['alternateIdentifier'] = {
                            'old': old,
                            'new': values['usageCitation']['alternateIdentifier']
                        }
                        child.text = values['usageCitation']['alternateIdentifier']
                    # change dataset['usageCitation']['id'] to 'associatedDRR'
                    if child.tag == 'id':
                        old = child.text
                        values['usageCitation']['id'] = 'associatedDRR'
                        updated_fields['id'] = {
                            'old': old,
                            'new': values['usageCitation']['id']
                        }
                        child.text = values['usageCitation']['id']
                    # change usage_citation['usageCitation']['report'] to {doi}
                    if child.tag == 'report':
                        old = child.text
                        values['usageCitation']['report'] = 'associatedDRR'
                        updated_fields['report'] = {
                            'old': old,
                            'new': values['usageCitation']['report']
                        }
                        child.text = values['usageCitation']['report']

                if 'alternateIdentifier' not in updated_fields.keys():
                    missing_fields.append('alternateIdentifier')
                if 'id' not in updated_fields.keys():
                    missing_fields.append('id')
                if 'report' not in updated_fields.keys():
                    missing_fields.append('report')
                
            else:
                missing_fields.append(f'{node_target}/alternateIdentifier')
                missing_fields.append(f'{node_target}/report')
                missing_fields.append(f'{node_target}/id')

            if self.interactive == True:
                if len(updated_fields) == 0:
                    if len(node) > 1:
                        print(f'\n{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}Your dataset has {len(node)} usage citations.')
                        print('Use `get_usage_citation()` and `set_usage_citation()` to resolve this problem.')
                    else:
                        print(f'\n{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}Your dataset is missing all required fields to comply with NPS spec:')
                        for field in missing_fields:
                            print(f'`{bcolors.BOLD}{field}{bcolors.ENDC}` resolve with `{bcolors.BOLD}myemld.set_{node_target}(){bcolors.ENDC}`')
                else:
                    print(f'\n{bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE}Success!{bcolors.ENDC}\n\nThe following fields were updated to NPS spec:{bcolors.ENDC}\n')
                    for k, v in updated_fields.items():
                        print(f'`{bcolors.BOLD}{k}{bcolors.ENDC}`:')
                        print(f'{bcolors.BOLD}{json.dumps(v, indent=4)}{bcolors.ENDC}')
                    if len(missing_fields) > 0:
                        print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nYour dataset is missing some fields to be fully in-line with NPS spec:')
                        for field in missing_fields:
                            if field == 'alternateIdentifier':
                                print(f'`{bcolors.BOLD}{field}{bcolors.ENDC}` resolve with `{bcolors.BOLD}myemld.set_{node_target}(alt_id=){bcolors.ENDC}`')
                            else:
                                print(f'`{bcolors.BOLD}{field}{bcolors.ENDC}` resolve with `{bcolors.BOLD}myemld.set_{node_target}({field}=){bcolors.ENDC}`')
                    
        except:
            print('error_make_nps()')
        
    def _content_units_api(self, unit_codes:tuple):
        try:
            # An API call to NPS Rest Services to get
            polygon_holder = dict() # decimal degrees of all polygon points for each `unit`
            bbox_holder = dict() # bounding box (max & min lat & lon) for each `unit`
            geog_cov = dict() # the bounding box(es) in the format that EML requires
            for unit in unit_codes:
                # loop over each `unit` in `unit_codes`
                api_url = 'https://irmaservices.nps.gov/v2/rest/unit/' + str(unit) + '/geography'
                if self.interactive == True:
                    print(f'API call for {str(unit)}... {api_url}')
                contents = urllib.request.urlopen(api_url).read()
                contents = xmltodict.parse(urllib.request.urlopen(api_url).read())
                contents = contents["ArrayOfUnitGeography"]["UnitGeography"]["Geography"]
                contents = contents.replace(',', '').replace('\']', '').replace('[\'', '').replace('POLYGON ((', '').replace('))', '').split()
                park_geom = pd.DataFrame()
                park_geom["lat"] = contents[1::2] # Elements from list1 starting from 1 iterating by 2
                park_geom["lon"] = contents[::2]
                polygon_holder[unit] = park_geom
                # split into decimal degree bounding box
                bbox_holder[unit] = {
                'N': max(polygon_holder[unit]["lat"]),
                'E': min(polygon_holder[unit]["lon"]),
                'S': min(polygon_holder[unit]["lat"]),
                'W': max(polygon_holder[unit]["lon"])
                }
                # build EML geographic coverage dict for each unit
                geog_cov[unit] = {
                    'geographicDescription': 'NPS Content Unit Link: ' + unit,
                    'boundingCoordinates': {
                        'northBoundingCoordinate': bbox_holder[unit]["N"],
                        'eastBoundingCoordinate': bbox_holder[unit]["E"],
                        'southBoundingCoordinate': bbox_holder[unit]["S"],
                        'westBoundingCoordinate': bbox_holder[unit]["W"]
                    }
                }
            return geog_cov
        except:
            print('API call failed')
    
    def _set_version(self):
        # 1. create a <emlEditor> node at self.emld['additionalMetadata']["metadata"]["emlEditor"]
        # 2. assign value src.pyEML.constants.CURRENT_RELEASE to emlEditor.text
        # 3. assign value src.pyEML.constants.APP_NAME to <emlEditor> attribute 'id'
        node_xpath = LOOKUPS['version']['node_xpath']
        parent = LOOKUPS['version']['parent']
        values = LOOKUPS['version']['values_dict']
        
        app = values['emlEditor']['app']

        self._append_node(values=values, node_xpath=node_xpath, parent=parent)
        
        node = self.root.findall(node_xpath)
        mynode = node[len(node)-1]
        mynode.set('id', app)

        # if self.interactive == True:
        #     self._get_version()

    def _get_version(self):
        node_xpath = LOOKUPS['version']['node_xpath']
        node = self.root.findall(node_xpath)

        if self.interactive == True:
            for elm in node:
                self._serialize(node=elm)
    
    def _serialize(self, node:etree._Element, depth:int=0):
        """Starts at a given node, crawls all of its sub-nodes, pretty-prints tags, attributes, and text to console

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
            if len(node.attrib) == 0:
                print(f'<{node.tag}>')
                print(f'    {node.text}')
                print(f'</{node.tag}>')
            else:
                attrib_str = []
                for k,v in node.attrib:
                    attrib_str.append(f'{k}="{v}"')
                if len(attrib_str) >1:
                    att_final = ' '.join(attrib_str)
                else:
                    att_final = attrib_str[0]
                print(f'<{node.tag} {att_final}>')
                print(f'    {node.text}')
                print(f'</{node.tag}>')
        else:
            spaces = depth * '    '
            if len(node.attrib) == 0:
                print(f'{spaces}<{node.tag}>')
                for elm in node:
                    if len(elm) == 0:
                        print(f'{spaces}    <{elm.tag}>')
                        print(f'{spaces}        {elm.text}')
                        print(f'{spaces}    </{elm.tag}>')
                    else:
                        self._serialize(elm, depth+1)
                print(f'{spaces}</{node.tag}>')
            else:
                attrib_str = []
                for k,v in node.attrib.items():
                    attrib_str.append(f'{k}="{v}"')
                if len(attrib_str) >1:
                    att_final = ' '.join(attrib_str)
                else:
                    att_final = attrib_str[0]
                print(f'{spaces}<{node.tag} {att_final}>')
                for elm in node:
                    if len(elm.attrib) == 0:
                        if len(elm) == 0:
                            print(f'{spaces}    <{elm.tag}>')
                            print(f'{spaces}        {elm.text}')
                            print(f'{spaces}    </{elm.tag}>')
                        else:
                            self._serialize(elm, depth+1)
                    else:
                        attrib_str = []
                        for k,v in elm.attrib:
                            attrib_str.append(f'{k}="{v}"')
                        if len(attrib_str) >1:
                            att_final = ' '.join(attrib_str)
                        else:
                            att_final = attrib_str[0]
                        if len(elm) == 0:
                            print(f'{spaces}    <{elm.tag} {att_final}>')
                            print(f'{spaces}        {elm.text}')
                            print(f'{spaces}    </{elm.tag}>')
                        else:
                            self._serialize(elm, depth+1)
                print(f'{spaces}</{node.tag}>')
    
    def _make_citation(self, citation_parts:dict, style:str):
        """Makes a citation paragraph from a dictionary of pieces

        Args:
            citation_parts (dict): A dictionary of citation pieces. E.g., author names, date, title.
            style (str, optional): The style of citation to generate. E.g., 'chicago'. `style` validated against src.pyEML.constants.CITATION_STYLES
        """
        try:
            if style == 'chicago':
                citation = self._make_chicago(citation_parts=citation_parts)
                return citation
        except:
            print('error _make_citation()')
    
    def _make_chicago(self, citation_parts:dict):
        try:
            new_citation_parts = {}
            if 'authors' in citation_parts.keys():
                author_list = []
                for element in citation_parts['authors']:
                    author = []
                    if 'first' in element.keys():
                        firstname = element['first'].capitalize()
                        author.append(firstname)
                    if 'middle' in element.keys():
                        middleinitial = element['middle'][0].upper()
                        middleinitial = middleinitial + '.'
                        author.append(middleinitial)
                    if 'last' in element.keys():
                        lastname = element['last'].capitalize()
                        author.append(lastname)
                    author_list.append(author)
                finalnames = []
                for name in author_list:
                    finalname = ' '.join(name)
                    finalnames.append(finalname)
                new_citation_parts['authors'] = ', '.join(finalnames)
            if 'date' in citation_parts.keys():
                citation_date = citation_parts.get('date').strftime("%Y")
                new_citation_parts['date'] = citation_date
            if 'title' in citation_parts.keys():
                citation_title = citation_parts.get('title')
                new_citation_parts['title'] = citation_title
            if 'doc_type' in citation_parts.keys():
                citation_doc_type = citation_parts.get('doc_type')
                new_citation_parts['doc_type'] = citation_doc_type
            if 'version' in citation_parts.keys():
                citation_version = citation_parts.get('version')
                new_citation_parts['version'] = f'Version {citation_version}'
            if 'url' in citation_parts.keys():
                citation_url = citation_parts.get('url')
                new_citation_parts['url'] = f'version {citation_url}'
            if 'etc' in citation_parts.keys():
                citation_etc = citation_parts.get('etc')
                new_citation_parts['etc'] = citation_etc
            new_citation = '. '.join(map(str, new_citation_parts.values()))
            return new_citation
        except:
            print('error _make_chicago()')
    
    def _old_serialize(self, node:etree._Element, depth:int=0):
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
                    for child in node:
                        child.getparent().remove(child)
                    # if len(node) == 1:
                    #     for child in node:
                    #         child.getparent().remove(child)
                    # else:
                    #     for child in node:
                    #         for elm in child:
                    #             elm.getparent().remove(elm)
                else:
                    if len(node) == 1:
                        print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nMetadata package contains one `{bcolors.BOLD}{node_target}{bcolors.ENDC}` node:')
                    if len(node) > 1:
                        print(f'{bcolors.WARNING + bcolors.BOLD + bcolors.UNDERLINE}Warning!{bcolors.ENDC}\nMetadata package contains {len(node)} `{bcolors.BOLD}{node_target}{bcolors.ENDC}` nodes:')
                    counter = 1
                    for elm in node:
                        if len(node) <=1:
                            self._serialize(elm)
                        if len(node) >1:
                            print(f'{counter}.')
                            self._serialize(elm)
                            counter += 1
                            print('\n')

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
                        print(f'Metadata package contains {len(node)} `{bcolors.BOLD}{node_target}{bcolors.ENDC}` nodes:')
                        print('----------')
                        counter=1
                        for child in node:
                            print(f'{counter}.')
                            self._serialize(child)
                            print('\n')
                            counter += 1
                else:
                    return node
        except MissingNodeException as e:
            if quiet == False:
                print(e.msg)
        
    def _set_node(self, values:dict, node_target:str, node_xpath:str, parent:str, quiet:bool):
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
            myemld._set_node(values_dict, node_target='title', node_xpath='./dataset/title', parent = './dataset', quiet=False)
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
            
            # make sure all required parent nodes exist
            parent_node_xpath = self._parent_node_finder(_dict=node_check, is_present=True) # find parent node that exists to check against the parent node we need `parent`
            parent_node = self.root.findall(parent_node_xpath)
            assert len(parent_node) == 1, 'Returned multiple parent nodes. Ambiguous data structure.'
            parent_node = self.root.findall(parent_node_xpath)[0]

            if parent_node_xpath == parent: # if the parent node the program found is the parent node the program is expecting, proceed
                self._serialize_nodes(_dict = values, target_node=parent_node)
            else: # otherwise, build missing nodes
                possible_nodes = node_check.copy()
                del possible_nodes[node_xpath]
                nodes_to_build = self._parent_node_finder(_dict=possible_nodes, is_present=False)
                nodes_to_build = nodes_to_build.replace(parent_node_xpath, '')
                nodes_to_build = nodes_to_build.split('/')
                nodes_to_build = [x for x in nodes_to_build if x != '']
                newvalues = {}
                newvalues = self._rebuild_values(new_values=newvalues, values=values, nodes_to_build=nodes_to_build)
                self._serialize_nodes(_dict = newvalues, target_node=parent_node)

        except AssertionError as a:
            print(a)
    
    def _rebuild_values(self, new_values:dict, values:dict, nodes_to_build:list):
        """Add missing parent keys upstream in a `values` dictionary when etree.root is missing parent nodes

        `_rebuild_values()` allows a user to set values for which parent nodes are missing.
        E.g., An `Emld` with no `coverage` node would be valid EML because `coverage` has minOccurs=0. https://eml.ecoinformatics.org/schema/
        In that case, calling `set_temporal_coverage()` would error because its parent node, `coverage` doesn't exist,
        and would be unrecoverable for a user because `Emld` doesn't let users assign empty ('', None, 'None') values at nodes.
        For data integrity reasons, it doesn't make sense for users to ever create empty nodes; users can simply delete nodes instead.
        `_rebuild_values()` adds missing parents to the `values` dictionary, which lets users `set...()` despite missing parent nodes.

        Args:
            new_values (dict): The dictionary containing parent node keys that were missing 
            values (dict): A dictionary in the `values_dict` format of `LOOKUPS` that contains values that the user wants to set.
            nodes_to_build (list): A list of xpath pieces (pieces of an xpath between each '/') that will become keys in `new_values`

        Returns:
            dict: A dictionary containing the values the user provided to their `set...()` call nested inside whatever parent nodes were missing
        """
        if len(nodes_to_build) == 1:
            new_values[nodes_to_build[0]] = values
            return new_values
        elif len(nodes_to_build) > 1:
            new_values[nodes_to_build[0]] = None
            self._rebuild_values(new_values=new_values, values=values, nodes_to_build=nodes_to_build[-nodes_to_build[0]])

    def _parent_node_finder(self, _dict:dict, is_present:bool):
        """Find the most downstream parent node that exists in an element tree

        Args:
            _dict (dict): A dictionary where keys are xpaths of nodes in an element tree and values are True or False.
                True means there is an element at that xpath. False means there is no element at that xpath.
            is_present (bool): If True, function looks for the furthest downstream node that does exist.
                If False, function looks for furthest downstream that does *not* exist.

        Returns:
            str: the xpath of the furthest downstream parent that exists (if `is_present == True`) or does not exist (if `is_present == False`).
        """
        mylist = list(_dict.values())
        minidices = []
        for i in range(0, len(mylist)):
            if mylist[i] == is_present:
                minidices.append(i)
        myval = min(minidices)
        finalval = list(_dict.keys())[myval]
        return finalval
    
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
                if len(value) == 0:
                    del _dict[key]
                else:
                    for v_i in value:
                        if isinstance(v_i, dict):
                            self._delete_none(v_i)
        
        return _dict
    
    def _append_node(self, values:dict, node_xpath:str, parent:str):
        # if there's not a node at `node_target`, need to find crawl xpath to add missing nodes
        node_list = self._find_parents(node_xpath=node_xpath)
        node_check = {}
        for element in node_list:
            nodeset = self.root.findall(element)
            if len(nodeset) == 0:
                node_check[element]=False
            else:
                node_check[element]=True

        # assert False in node_check.values(), 'Node deletion failed' # there must be at least one False in node_check or program will duplicate tags
        
        # make sure all required parent nodes exist
        parent_node_xpath = self._parent_node_finder(_dict=node_check, is_present=True) # find parent node that exists to check against the parent node we need `parent`
        parent_node = self.root.findall(parent_node_xpath)
        assert len(parent_node) == 1, 'Returned multiple parent nodes. Ambiguous data structure.'
        parent_node = self.root.findall(parent_node_xpath)[0]

        if parent_node_xpath == parent: # if the parent node the program found is the parent node the program is expecting, proceed
            self._serialize_nodes(_dict = values, target_node=parent_node)
        elif parent_node_xpath == node_xpath:
            parent_node = self.root.findall(parent)
            assert len(parent_node) == 1, 'Returned multiple parent nodes. Ambiguous data structure.'
            parent_node = parent_node[0]
            self._serialize_nodes(_dict = values, target_node=parent_node)
        else: # otherwise, build missing nodes
            possible_nodes = node_check.copy()
            del possible_nodes[node_xpath]
            nodes_to_build = self._parent_node_finder(_dict=possible_nodes, is_present=False)
            nodes_to_build = nodes_to_build.replace(parent_node_xpath, '')
            nodes_to_build = nodes_to_build.split('/')
            nodes_to_build = [x for x in nodes_to_build if x != '']
            newvalues = {}
            newvalues = self._rebuild_values(new_values=newvalues, values=values, nodes_to_build=nodes_to_build)
            self._serialize_nodes(_dict = newvalues, target_node=parent_node)

    def show_overview(self, node_xpath:str=None):
        """Pretty-print up to three levels of xml tags and text

        This method pretty-prints to console the tag structure to a max depth of three levels of tags (depth = 0, 1, 2).
        This shows a user their element tree structure without details like deeply-nested nodes, namespaces, and attributes.
        `show_overview()` is good for simply checking an element tree's structure or confirming that a `set` or `delete` method worked.
        If you want the full-detail of your element tree, use `_serialize()` or `save_xml()`.

        Args:
            node_xpath (str, optional): The xpath to the node you want to overview from. E.g. './dataset'. Defaults to None.
        """
        if self.interactive == True:
            quiet = False
        else:
            quiet = True
        
        if node_xpath is None:
            node = self.root
        else:
            node = self._get_node(node_xpath=node_xpath, node_target='na', pretty=False, quiet=quiet)
        self.__show_overview(node=node, depth=0)
    
    def __show_overview(self, node:etree._Element, depth:int):
        if depth < 2:
            spaces = '    ' * depth
            if depth == 0:
                print(f'{spaces}<{node.tag}>')
            if len(node.children) == 0:
                print(f'{spaces}    {node.text}')
            else:
                for child in node.children:
                    print(f'{spaces}    <{child.tag}>')
                    self.__show_overview(child, depth+1)
            print(f'{spaces}</{node.tag}>')
    
    def write_eml(self, filename:str):
        """Write EML-formatted xml file
        
        Args:
            filename (str): the filename and filepath where you want to save your EML-formatted xml.

        Examples:
            myemld.write_eml(filename='test_output.xml')
        """
        try:
            assert filename.endswith('.xml'),  f'{bcolors.FAIL + bcolors.BOLD + bcolors.UNDERLINE}Process execution failed.\n{bcolors.ENDC}You provided "{filename}".\n`filename` must end in ".xml".'
        
            self.tree.write(filename, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        
        except AssertionError as a:
            print(a)

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