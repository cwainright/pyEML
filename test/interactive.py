import src.pyEML.emld
from importlib import reload
reload(src.pyEML.emld)
from src.pyEML.emld import Emld



filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/pyEML/data/long_input.xml'
# filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/pyEML/data/short_input.xml'
myemld = Emld(filepath=filename, INTERACTIVE=True)


myemld.set_creator(first='newfirstname')
# myemld.interactive
# myemld.nps
# myemld.tree
# myemld.root

myemld.get_title(pretty=True)
myemld.get_title()
myemld.set_title(title='my second title')
myemld.set_title(title='')
myemld.set_title(title=None)
myemld.get_title(pretty=True)
myemld.delete_title(quiet=True)

# myemld.write_eml(filename='data/testout.xml')
myemld.get_creator(pretty=True)
myemld.get_creator()
myemld.delete_creator(quiet=True)

node_xpath = './dataset/creator/individualName/givenName'
myemld._find_parents(node_xpath)





















































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

first = 'newfirst'
last = 'newlast'
org = 'neworg'
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