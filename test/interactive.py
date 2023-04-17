import src.pyEML.emld
from importlib import reload
reload(src.pyEML.emld)
from src.pyEML.emld import Emld

filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/pyEML/data/long_input.xml'
# filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/pyEML/data/short_input.xml'
myemld = Emld(filepath=filename, INTERACTIVE=True)
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