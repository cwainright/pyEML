"""An example interactive workflow demonstration for pyEML"""
from src.pyEML.emld import Emld

# -----Step 1. Create EML xml.-------------------------------
filename = 'data/short_input.xml'

# -----Step 2. Instantiate an `Emld`.-------------------------------
myemld = Emld(filepath=filename, INTERACTIVE=True)

# since `myemld.root` and all of `root`'s nodes are lxml `Element`s,
# all lxml `Element` methods are available to you
print(type(myemld.root))

# `pyeml.emld.Emld._serialize()` prints any `Emld` node to console and is the basis of `pyeml.emld.Emld.get()` methods
myemld._serialize(myemld.root) # prints your whole xml to console; only helpful for short EML files

# if you like xpath syntax:
my_additional_metadata = myemld.root.findall('./additionalMetadata') # from lxml; search for node(s) by xpath; https://lxml.de/tutorial.html
for node in my_additional_metadata:
  myemld._serialize(node) # prints all 'additionalMetadata' nodes to console; there is no print-to-console method in lxml

# -----Step 3. Determine what changes to make to your EML.-------------------------------

myemld.get_title()

myemld.get_keywords()

myemld.get_geographic_coverage()

myemld.get_language()

# -----Step 4. Edit EML and view changes.-------------------------------
myemld.set_language('english') # calls API, returns ISO language abbreviation

myemld.delete_title() # pyEML will warn a user before overwriting or deleting values at a node.
myemld.set_title('my new title')

myemld.set_keywords('first keyword', 'second keyword') # pyEML will warn a user before overwriting or deleting values at a node.

myemld.get_geographic_coverage()
myemld.set_nps_geographic_coverage('GWMP', 'GLAC', 'ACAD') # pyEML will warn a user before overwriting or deleting values at a node.

# -----Step 5. Write xml.-------------------------------
myemld.write_eml('data/my_metadata.xml')