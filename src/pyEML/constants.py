"""Holds constants for Emld objects"""

#: `LOOKUPS` holds abstracted EML-schema information that an `Emld`'s get, set, and delete methods needs.
LOOKUPS = {
    'title': {
        'node_xpath': './dataset/title',
        'node_target': 'title',
        'parent': './dataset',
        'values_dict': {
            'title': None
            }
    },
    'creator': {
        'node_xpath': './dataset/creator',
        'node_target': 'creator',
        'parent': './dataset',
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
        'parent': './dataset',
        'values_dict': {
            'keywordSet': {
                'keyword': None
            }
        }
    },
    'publisher': {
        'node_xpath': './dataset/publisher',
        'node_target': 'publisher',
        'parent': './dataset',
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
        'parent': './dataset',
        'values_dict': {
            'pubDate': None
        }
    },
    'temporal_coverage': {
        'node_xpath': './dataset/coverage/temporalCoverage',
        'node_target': 'temporal coverage',
        'parent': './dataset/coverage',
        'values_dict': {
            'temporalCoverage': {
                'rangeOfDates': {
                    'beginDate': {
                        'calendarDate': None
                    },
                    'endDate': {
                        'calendarDate': None
                    }
                }
            }
        }
    },
    'cui': {
        'node_xpath': './additionalMetadata/metadata/CUI',
        'node_target': 'cui',
        'parent': './additionalMetadata/metadata',
        'values_dict': {
            'CUI': None
        }
    }
}

#: `CUI_CHOICES` is pick-list of controlled unclassified information (CUI) options used in `describe_cui()`, `get_cui()`, and `set_cui()`.
CUI_CHOICES = {
    'PUBLIC': 'Contains CUI. Only federal employees should have access (similar to "internal only" in DataStore)',
    'NOCON': 'Contains  CUI. Federal, state, local, or tribal employees may have access, but contractors cannot.',
    'DL_ONLY': 'Contains CUI. Should only be available to a names list of individuals (where and how to list those individuals TBD)',
    'FEDCON': 'Contains CUI. Only federal employees and federal contractors should have access (also very much like current "internal only" setting in DataStore)',
    'FED_ONLY': 'Contains CUI. Only federal employees should have access (similar to "internal only" in DataStore)'
    }

#: `LICENSE_TEXT` is pick list of intellectual rights choics used in `describe_int_rights()`, `get_int_rights()`, `set_int_rights()`.
LICENSE_TEXT = {
    'CCzero': 'This product is released to the "public domain" under Creative Commons CC0 1.0 No Rights Reserved (see: https://creativecommons.org/publicdomain/zero/1.0/).',
    'public_domain': 'This product is released to the "public domain" under U.S. Government Works No Rights Reserved (see: http://www.usa.gov/publicdomain/label/1.0/).',
    'restrict': 'This product has been determined to contain Controlled Unclassified Information (CUI) by the National Park Service, and is intended for internal use only. It is not published under an open license. Unauthorized access, use, and distribution are prohibited.'
    }

#: `INT_RIGHTS_CHOICES` is pick list of intellectual rights choics used in `describe_int_rights()`, `get_int_rights()`, `set_int_rights()`
INT_RIGHTS_CHOICES = LICENSE_TEXT.keys() 
#: The current release version of {APP_NAME}
CURRENT_RELEASE = '0.0.1'
#: The name of this EML pipeline application
APP_NAME = 'pyEML' # the name of the app; to be used in `pip install pyEML` or similar
#: `NPS_DOI_ADDRESS` is the National Park Service data package url prefix; to make a valid url, this must be suffixed with a valid DOI number
NPS_DOI_ADDRESS = 'https://doi.org/10.57830/'
#: `CITATION_STYLES` is pick list of citation styles into which `Emld` nodes can be deparsed; used in `make_citation()`.
CITATION_STYLES = {
    "chicago": "https://www.chicagomanualofstyle.org/tools_citationguide.html"
}




