import src.pyEML.emld
from importlib import reload
reload(src.pyEML.emld)
from src.pyEML.emld import Emld
from datetime import datetime

filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/pyEML/data/long_input.xml'
# filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/pyEML/data/short_input.xml'
myemld = Emld(filepath=filename, INTERACTIVE=True)
myemld.get_geographic_coverage()
myemld.delete_geographic_coverage()

mycoverage = {
    'area1': {
        'geographicDescription': 'A box around my sampling area',
        'boundingCoordinates': {
            'westBoundingCoordinate': '-78.7348',
            'eastBoundingCoordinate': '-76.758602',
            'northBoundingCoordinate': 39.6924,
            'southBoundingCoordinate': 38.545057
        }
    }
}
myemld.set_geographic_coverage(coverage=mycoverage)











myemld.get_language()
myemld.delete_language()
myemld.set_language(
    language='spanish'
)










































myemld.get_lit_cited()
myemld.delete_lit_cited()
mycitations = ['firsticitation', 'secondcitation']
myemld.set_lit_cited(
    citations=mycitations
)
























myemld.get_attributes()
myemld.set_attribute(
    attribute='wtf',
    value='newvalue'
)
myemld.delete_attribute(attribute="some")
myemld.delete_attribute(attribute="packageId")
myemld.get_attributes()
myemld.describe_attributes()




myemld.root.get("packageId")
myemld.root.set("packageId", 'mynewpackageid')
myemld.root.values()
del myemld.root.attrib['packageId']
myemld.root.keys()

myattribs = myemld.root.attrib
import json
print(json.dumps(myattribs, indent=4))
for k, v in myattribs:
    print(f'Key: {k}')
    print(f'Value: {v}')
type(myattribs)

'packageId' in myemld.root.keys()

for attribute in myemld.root.keys():
    print(f'{attribute}:')




attribute="all"
assert attribute in AVAILABLE_ATTRIBUTES
attribute in (AVAILABLE_ATTRIBUTES, 'all')
attribute in AVAILABLE_ATTRIBUTES

newlist = AVAILABLE_ATTRIBUTES.copy()
newlist.append('all')










mydate = '2021-01-01'
newdate = datetime.strptime(mydate, "%Y-%m-%d").date()
print(newdate.strftime("%Y"))

myemld.get_protocol_citation()
myemld.delete_protocol_citation()
myemld.get_keywords()
myemld.get_usage_citation()
myemld.delete_usage_citation()
myemld.set_usage_citation(doi_url='myurl', title='mytitle', creator='mycreator', doi='mydoi', id='myid')



myroot = myemld.root.findall('./dataset/additionalInfo/para')
counter=1
for elm in myroot:
    print(f'{counter}.')
    print(elm.text)
    counter+=1

myemld.describe_citation()
myvals = {
    'authors': [["JP", "Schmit"], ["GM", "Sanders"]]
}


new_citation_parts = {}
if myvals["authors"]:
    author_list = []
    for element in myvals['authors']:
        firstname = element[0].upper()
        lastname = element[1].capitalize()
        author = f'{lastname} {firstname}'
        author_list.append(author)
    new_citation_parts['authors'] = ', '.join(author_list)
new_citation_parts




myvals = {
    'authors': [
        {
            'first': 'John',
            'middle': 'Paul',
            'last': 'Schmit'
        },
        {
            'first': 'Elizabeth',
            'last': 'Matthews'
        }
    ]
}

new_citation_parts = {}
if myvals["authors"]:
    author_list = []
    for element in myvals['authors']:
        print(element)
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
    end_result = ', '.join(finalnames)
new_citation_parts['authors'] = end_result

[['John', 'P.', 'Schmit'], ['Elizabeth', 'Matthews']]

myname = [['John', 'P.', 'Schmit'], ['Elizabeth', 'Matthews']]
finalnames = []
for name in myname:
    finalname = ' '.join(name)
    finalnames.append(finalname)

', '.join(finalnames)








myemld.get_contact()
myemld.delete_contact()
myemld.set_contact(first='albus', last='dumbledore', org='hogwarts', email={'email':None})
myemld.set_contact(first='albus', last='dumbledore', org='hogwarts', email='wellsey.r@hogwarts.edu')

myemld.get_doi()
myemld.delete_doi()
myemld.set_doi(doi=1231231)













myemld.get_status()
myemld.delete_status()
myemld.set_status(status='complete')










myemld.get_int_rights()
myemld.delete_int_rights()
myemld.describe_int_rights()
myemld.set_int_rights(license='CCzero')







myemld.get_cui()
myemld.delete_cui()
myemld.describe_cui()
myemld.set_cui(cui='smoke')


myemld.describe_citation()
myemld.describe_cui()
myemld.describe_int_rights()


myemld.get_temporal_coverage()
myemld.delete_temporal_coverage()
myemld.set_temporal_coverage(begin_date='2020', end_date='2022')






node = myemld.root.findall('./dataset/coverage')
for child in node:
    child.getparent().remove(child)



























myemld.get_author()
myemld.delete_author()
myemld.set_author(first='newfirst')
myemld.get_pub_date()
myemld.set_pub_date(pub_date='2021')
myemld.delete_pub_date()






myemld.set_publisher(org='testorg')
myemld.get_publisher()
myemld.delete_publisher()

zip = '12312'
type(zip) in (str, int)


testval = {}
len(testval)






myemld.delete_keywords()
myemld.get_keywords()
myemld.set_keywords({'firstkeyword', 'secondkeyword'})
myemld.set_keywords('morekeywords', 'again')
myemld.get_keywords()







myemld.set_creator(first='newfirstname')
myemld.set_title(title='my second title')
# myemld.interactive
# myemld.nps
# myemld.tree
# myemld.root

myemld.get_title()
myemld.get_title()
myemld.set_title(title='my second title')
myemld.set_title(title='')
myemld.set_title(title=None)
myemld.get_title(pretty=True)
myemld.delete_title()

myemld.get_creator()
myemld.delete_creator()
myemld.get_creator()


myemld.get_title()
myemld.set_title(title='my second title')
myemld.delete_title()
myemld.get_title()





















































import src.pyEML.emld
from importlib import reload
reload(src.pyEML.emld)
from src.pyEML.emld import Emld

filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/pyEML/data/long_input.xml'
# filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/pyEML/data/short_input.xml'
myemld = Emld(filepath=filename, INTERACTIVE=True)

if values:
    del values
creator= {
        'node_xpath': './dataset/creator',
        'node_target': 'creator',
        'values_dict': {
            'individualName': {
                'givenName': None,
                'surName': None
            },
            'organizationName': None,
            'electronicMailAddress': None
        }
    }
values = creator['values_dict']

if first:
    del first
if last:
    del last
if org:
    del org
if email:
    del email


first = 'newfirst'
# last = 'newlast'
# org = 'neworg'
# email = ''

if first is not None or '':
    values['individualName']['givenName'] = first
if last is not None or '':
    values['individualName']['surName'] = last
if org is not None or '':
    values['organizationName'] = org
if email is not None or '':
    values['electronicMailAddress'] = email
values

def delete_none(_dict):
    """Delete None values recursively from all of the dictionaries"""
    for key, value in list(_dict.items()):
        if isinstance(value, dict):
            delete_none(value)
        elif value == '':
            del _dict[key]
        elif value is None:
            del _dict[key]
        elif isinstance(value, list):
            for v_i in value:
                if isinstance(v_i, dict):
                    delete_none(v_i)

    return _dict

newvalues = delete_none(values)
newvalues

titlevalues = {'title': 'mynewtitle'}

node_xpath = './dataset/title'
import lxml.etree as etree
parents = myemld._find_parents(node_xpath)
parent_node = myemld.root.xpath(parents[0])[0]
myemld.delete_title()
myemld.delete_creator(quiet=True)
def myfunc(_dict:dict, parent_node:etree._Element):
    for key, value in list(_dict.items()):
        if isinstance(value, (float, int, str)):
            new_node = etree.SubElement(parent_node, key)
            new_node.text = _dict[key]
        elif isinstance(value, dict):
            new_node = etree.SubElement(parent_node, key)
            print('got here')
            print(type(new_node))
            print(f'{new_node.tag}')

            # myfunc(value, new_node)
        # elif isinstance(value, list):
        #     for v_i in value:
        #         new_node = etree.SubElement(parent_node, key)
        #         if isinstance(v_i, dict):
        #             self._serialize_nodes(v_i, new_node)
myfunc(_dict=titlevalues, parent_node=parent_node)
myemld.get_creator(pretty=True)
myemld.get_title()
myemld.root.findall('./dataset/creator')