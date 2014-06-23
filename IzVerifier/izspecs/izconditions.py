from bs4 import BeautifulSoup
import re
from IzVerifier.izspecs.izcontainer import IzContainer
from IzVerifier.izspecs.izproperties import *


KEY_PATTERN = 'get_key_pattern'
REF_ID_ATTRIBUTES_LIST = 'ref_id_attributes_list'
IGNORE_KEY_PATTERN = 'ignore_key_pattern'

class IzConditions(IzContainer):
    """ Container for parsing and storing IzPack conditions from conditions.xml. """

    properties = {
        NAME: "conditions",
        DEFINITION_SPEC_FILES: ['conditions.xml'],
        REFERENCE_SPEC_FILES: ["install.xml", "userInputSpec.xml", "ProcessPanel.Spec.xml", "core-packs.xml"],
        IGNORE_KEY_PATTERN: '^izpack.*',  # used by izpack internal vars
        SOURCE_SEARCH_PATTERN: 'isConditionTrue(',
        CHECK_KEY_PATTERN: "isConditionTrue\(\"(.*?)\"\)",
        KEY_PATTERN: "getCondition\(\"(.*?)\"\)",
        ATTRIBUTES: ['condition', 'conditionid', 'refid'],
        REF_ID_ATTRIBUTES_LIST: ['refid'],
        SPEC_ELEMENT: "<condition type=\"{0}\" id=\"{1}\">",
        PARENT_OPENING_TAG: '<conditions>',
        PARENT_CLOSING_TAG: '</conditions>',
        WHITE_LIST: ['izpack.linuxinstall'],
        WHITE_LIST_PATTERNS: [],
        PATTERNS: [('isConditionTrue({0}', "isConditionTrue\(({0})\)"),
                     ("getCondition({0}", "getCondition\(({0})\)")]
    }


    def __init__(self, spec_path):
        self.conditions = {}
        self.soup = BeautifulSoup(open(spec_path))
        self.parse_conditions(self.soup)

    def parse_conditions(self, soup):
        """ Extracts all conditions from conditions.xml document. """
        conds = soup.find_all(self.has_condition_definition)
        for cond in conds:
            self.conditions[str(cond['id'])] = cond


    def get_keys(self):
        """
        Returns a set of all the keys for defined conditions.
        """
        return set(self.conditions.keys()) | set(self.properties[WHITE_LIST])

    def referenced_variables(self):
        """
        Returns the ids for all variables referenced by variable type conditions.
        """
        variables = set()
        for cond in self.conditions.itervalues():
            if self.has_def_by_variable_ref(cond):
                if cond.find('name'):
                    var = cond.find('name').get_text()
                    variables.add((var, cond['id']))
                else:
                    variables.add(("no_var_defined", cond['id']))
        return variables

    def print_keys(self):
        for cond in self.conditions.keys():
            print(cond)

    def count(self):
        return len(self.conditions.keys())

    def get_spec_elements(self):
        """
        Returns a set of xml elements defining each condition.
        """
        return set(self.conditions.values())

    def to_string(self):
        return str(self.conditions)

    def ref_transformer(self, reference):
        """ Given a compound condition id returns a list of the conditions contained in it.
            ie. "cond1+cond2+!cond3" = [cond1, cond2, cond3]"""
        cids = re.split("\+|\|", reference)
        return set([cid.replace("!", "") for cid in cids if not \
            re.match(self.properties['ignore_key_pattern'], cid.replace("!", ""))])

    def has_condition_definition(self, element):
        """
        Returns true if this element is a condition definition.
        """
        return element.name == 'condition' and element.has_attr('id')

    def has_reference(self, element):
        """
        Return true if the given element contains an izpack cond reference.
        """
        for atty in self.properties['attributes']:
            if element.has_attr(atty): return True

        return False

    def has_def_by_condition_ref(self, ele):
        """
        Function to determine if element contains a ref id for conditions.
        """
        return ele.has_attr('refid')

    def has_def_by_variable_ref(self, ele):
        """
        Does this element define a 'variable' type condition?
        """
        return ele.has_attr('type') and ele['type'] == 'variable'

    def extract_variable_from_definition(self, element):
        """
        Given an element containing a variable type condition, return the variable name.
        """
        return element.select('name').get_text()

    @staticmethod
    def get_identifier(element):
        """
        Returns the identifying value for this element.
        """
        return element['id']

    @staticmethod
    def get_value(element):
        """
        Returns the main 'value' for this element.
        In the case of conditions, its value is the entire definition, or element.
        """
        return element

    @staticmethod
    def element_sort_key(element):
        """
        Returns the key to use when sorting elements of this container.
        """
        return element['id'].lower()


