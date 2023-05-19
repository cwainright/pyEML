
import metapype.eml.names as names

LOOKUPS = {
    'title': {
        'path': [
            names.DATASET,
            names.TITLE
        ],
        'parent': [
            names.DATASET
        ],
        'target': 'title',
        'values_dict': {
            'title': None
            }
    },
    'creator': {
        'path': [
            names.DATASET,
            names.CREATOR
        ],
        'parent': [
            names.DATASET
        ],
        'target': 'creator',
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
    }
}
