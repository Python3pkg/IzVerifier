__author__ = 'fcanas'

import unittest
from IzVerifier.izverifier import IzVerifier
from IzVerifier.izspecs.verifiers.dependencies import test_verify_all_dependencies
from IzVerifier.izspecs.izproperties import *


path1 = 'data/sample_installer_iz5/izpack/install.xml'
source_path2 = 'data/sample_code_base'


class TestDependencies(unittest.TestCase):
    """
    Basic testing of verifier class.
    """

    def setUp(self):
        args = {
            'installer': path1,
            'sources': [source_path2],
            'specs': ['conditions', 'strings', 'variables']
        }
        self.izv = IzVerifier(args)

    def test_verifyAllDependencies(self):
        """
        Run the full dependency verification test.
        """
        test_verify_all_dependencies(self.izv)

