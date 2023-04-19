"""Holds constants for Emld objects"""

#: The current release version of {APP_NAME}
CURRENT_RELEASE = '0.0.1'
#: The name of this EML pipeline application
APP_NAME = 'pyEML' # the name of the app; to be used in `pip install pyEML` or similar

#: `LOOKUPS` holds abstracted EML-schema information that an `Emld`'s get, set, and delete methods need.
#: `node_xpath` is the xpath to the node that a `get` method retrieves, a `delete` method removes, and a `set` method assigns value(s) to
#: `node_target` is a str used to generate f-strings in warning and error messages
#: `parent` is the node to which a `set` method appends new values; used to validate that all required nodes upstream from `node_xpath` (i.e., parent nodes) exist
#: `values_dict` is an empty dictionary that has the key-value (xml tag-text) structure for the node at `node_xpath`
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
    },
    'int_rights': {
        'node_xpath': './dataset/intellectualRights',
        'node_target': 'int_rights',
        'parent': './dataset',
        'values_dict': {
            'intellectualRights': {
                'para': None
            }
        }
    },
    'status': {
        'node_xpath': './dataset/maintenance',
        'node_target': 'status',
        'parent': './dataset',
        'values_dict': {
            'maintenance': {
                'description': None
            }
        }
    },
    'doi': { # the digital object identifier; https://www.doi.org/
        'node_xpath': './dataset/alternateIdentifier',
        'node_target': 'doi',
        'parent': './dataset',
        'values_dict': {
            'alternateIdentifier': None
        }
    },
    'contact': {
        'node_xpath': './dataset/contact',
        'node_target': 'contact',
        'parent': './dataset',
        'values_dict': {
            'contact': {
                'individualName': {
                'givenName': None,
                'surName': None
            },
            'organizationName': None,
            'electronicMailAddress': None
            }
        }
    },
    'usage_citation': { # For NPS users, this is the NPS DataStore reference ID for the data release report (DRR); https://irma.nps.gov/DataStore/
        'node_xpath': './dataset/usageCitation',
        'node_target': 'usage_citation',
        'parent': './dataset',
        'values_dict': {
            'usageCitation': {
                'alternateIdentifier': None, # for NPS: 'https://doi.org/10.36967/' + './dataset/alternateIdentifier'
                'title': None, # for NPS: DataStore DRR title
                'creator': None, # for NPS: self.get_creator()
                'report': None, # for NPS: './dataset/alternateIdentifier'
                'id': None # for NPS: 'associatedDRR'
            }
        }
    },
    'version': {
        'node_xpath': './additionalMetadata/metadata/emlEditor',
        'node_target': 'version',
        'parent': './additionalMetadata/metadata',
        'values_dict': {
            'emlEditor': {
                'app': APP_NAME,
                'release': CURRENT_RELEASE
            }
        }
    },
    'protocol_citation': {
        'node_xpath': './dataset/additionalInfo/para',
        'node_target': 'protocol_citation',
        'parent': './dataset/additionalInfo',
        'values_dict': {
            'para': None
        }
    },
    'abstract': {
        'node_xpath': './dataset/abstract',
        'node_target': 'abstract',
        'parent': './dataset',
        'values_dict': {
            'abstract': {
                'para': None
            }
        }
    },
    'lit_cited': {
        'node_xpath': './dataset/literatureCited',
        'node_target': 'lit_cited',
        'parent': './dataset',
        'values_dict': {
            'literatureCited': {
                'bibtex': None
            }
        }
    },
    'language': {
        'node_xpath': './dataset/language',
        'node_target': 'language',
        'parent': './dataset',
        'values_dict': {
                'language': None
        }
    },
    'geographic_coverage': {
        'node_xpath': './dataset/coverage/geographicCoverage',
        'node_target': 'geographic_coverage',
        'parent': './dataset/coverage',
        'values_dict': {
                'geographicCoverage': None
        }
    },
    'metadata_provider': {
        'node_xpath': './dataset/metadataProvider',
        'node_target': 'metadata_provider',
        'parent': './dataset',
        'values_dict': {
            'metadataProvider': {
                'individualName': {
                'givenName': None,
                'surName': None
            },
            'organizationName': None,
            'electronicMailAddress': None
            }
        }
    },
    'nps_producing_units': {
        'node_xpath': './dataset/metadataProvider',
        'node_target': 'nps_producing_units',
        'parent': './dataset',
        'values_dict': {
            'metadataProvider': {
                'unit': None
            }
        }
    }
}

#: `AVAILABLE_ATTRIBUTES` is a list of the available top-line attributes for EML https://eml.ecoinformatics.org/schema/
AVAILABLE_ATTRIBUTES = {
    'packageId': "A globally unique identifier for the data package described by this EML metadata document that can be used to cite it elsewhere. example: https://doi.org/10.5063/F17P8WGK",
    'scope': 'The scope of the identifier. Scope is generally set to either "system", meaning that it is scoped according to the "system" attribute, or "document" if it is only to be in scope within this single document instance. example: "system"',
    'system': 'Always assigned value of "unknown". No additional information available at https://eml.ecoinformatics.org/schema/'
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

#: `NPS_DOI_ADDRESS` is the National Park Service data package url prefix; to make a valid url, this must be suffixed with a valid DOI number
NPS_DOI_ADDRESS = 'https://doi.org/10.57830/'
#: `CITATION_STYLES` is pick list of citation styles into which `Emld` nodes can be deparsed; used in `make_citation()`.
CITATION_STYLES = {
    "chicago": "https://www.chicagomanualofstyle.org/tools_citationguide.html"
}




