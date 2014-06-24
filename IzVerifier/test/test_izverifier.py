__author__ = 'fcanas'

import unittest
from IzVerifier.izspecs.containers.izconditions import IzConditions
from IzVerifier.izspecs.containers.izstrings import IzStrings
from IzVerifier.izspecs.containers.izvariables import IzVariables
from IzVerifier.izverifier import IzVerifier
from IzVerifier.izspecs.izproperties import *


path1 = 'data/sample_installer_iz5'

class TestVerifier(unittest.TestCase):
    """
    Basic testing of verifier class.
    """

    def setUp(self):
        args = {
            'installer': path1,
            'sources': [],
            'specs': ['conditions', 'strings', 'variables']
        }
        self.izv = IzVerifier(args)

    def test_IzPaths(self):
        """
        Testing install.xml path parsing.
        """
        specs = [('variables', 'variables.xml'),
                 ('conditions', 'conditions.xml'),
                 ('dynamicvariables', 'dynamic_variables.xml'),
                 ('resources', 'resources.xml'),
                 ('panels', 'panels.xml'),
                 ('packs', 'packs.xml')]

        self.assertTrue(self.izv != None)
        for spec in specs:
            path = self.izv.paths.get_path(spec[0])
            self.assertTrue(spec[1] in path,
                            msg=path + "!=" + spec[1])

    def test_IzConditions(self):
        """
        Testing the strings container.
        """
        conditions = self.izv.paths.get_path('conditions')
        self.assertEquals(conditions,'data/sample_installer_iz5/izpack/conditions.xml')

        izc = IzConditions(conditions)
        self.assertTrue(izc != None)

        # Test for number of keys in conditions.xml plus white list
        num = len(izc.get_keys()) - len(izc.properties[WHITE_LIST])
        self.assertEquals(num, 2, str(num) + "!=2")

    def test_langpack_paths(self):
        """
        Test that we parsed the langpack paths from resources.xml
        """
        langpacks = [('CustomLangPack.xml', 'data/sample_installer_iz5/resources/langpacks/CustomLangPack.xml'),
                     ('CustomLangPack.xml_eng', 'data/sample_installer_iz5/resources/langpacks/CustomLangPack.xml')]

        for tpack, fpack in zip(langpacks, self.izv.paths.get_langpacks()):
            self.assertTrue(tpack[1] == fpack[1], msg=tpack[1] + '!=' + fpack[1])

    def test_IzStrings(self):
        """
        Testing the strings container.
        """
        langpacks = self.izv.paths.get_langpacks()

        langpack = langpacks[0]
        izs = IzStrings(langpack[1])
        self.assertTrue(izs != None)

        # Test for number of strings
        num = len(izs.get_keys())
        self.assertEquals(num, 4, str(num) + '!=4')

    def test_IzVariables(self):
        """
        Testing the variables container.
        """
        variables = self.izv.paths.get_path('variables')
        self.assertEquals(variables,'data/sample_installer_iz5/izpack/variables.xml')

        izv = IzVariables(variables)
        self.assertTrue(izv != None)
        num = len(izv.get_keys()) - len(izv.properties[WHITE_LIST])
        self.assertEquals(num, 3, str(num) + '!=3')


if __name__ == '__main__':
    unittest.main()

