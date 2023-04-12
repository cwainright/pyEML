import lxml.etree as etree
from src.pyEML.emld import Emld
import src.pyEML.error_classes as error_classes
filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/pyEML/data/long_input.xml'
# filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/2023/20230210_iss135_emleditor/sandbox/testinput2.xml'
# filename = 'C:/Users/cwainright/OneDrive - DOI/Documents/data_projects/2023/20230210_iss135_emleditor/sandbox/2022_NCRN_forest_vegetation_metadata.xml'
myemld = Emld(filepath=filename, INTERACTIVE=True)

# myemld.interactive
# myemld.nps
# myemld.tree
# myemld.root

myemld.get_title(pretty=True)
mynode = myemld.get_title(pretty=False)
myemld.set_title(title='my new title')
myemld.get_title(pretty=True)
myemld.delete_title(quiet=False)

# myemld.write_eml(filename='data/testout.xml')
myemld.get_creator(pretty=True)
myemld.get_creator()
myemld.delete_creator(quiet=False)


node_text = './dataset/title'
myemld._find_parents(node_text)


