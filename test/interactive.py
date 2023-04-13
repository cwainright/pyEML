import src.pyEML.emld
from importlib import reload
reload(src.pyEML.emld)
from src.pyEML.emld import Emld



filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/pyEML/data/long_input.xml'
# filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/pyEML/data/short_input.xml'
myemld = Emld(filepath=filename, INTERACTIVE=True)

# myemld.interactive
# myemld.nps
# myemld.tree
# myemld.root

myemld.get_title(pretty=True)
myemld.get_title()
myemld.set_title(title='my second title')
myemld.get_title(pretty=True)
myemld.delete_title(quiet=True)

# myemld.write_eml(filename='data/testout.xml')
myemld.get_creator(pretty=True)
myemld.get_creator()
myemld.delete_creator(quiet=True)

node_xpath = './dataset/creator/individualName/givenName'
myemld._find_parents(node_xpath)


