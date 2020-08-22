# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pkg_resources
from xml.etree import ElementTree as ET

from odenet.odenet_class import *
from odenet.odenet_change import *


__version__ = '0.1.0'

__author__ = 'Melanie Siegel'
__license__ = "None"


class OdeNetReadOnly:
    """
    This class provides read-only access to the wordnet. The interface should
    be easy to use. Modifications of the wordnet are TBD.
    """

    def __init__(self):
        # the following code needs that the odenet package
        # is importable (i.e. no errors during import).
        # So either the package has to be installed via pip
        # or the Python interpreter has to be started from
        # the root directory of the package.

        self.file_contents = pkg_resources.resource_string(
            "odenet",
            "wordnet/deWordNet.xml"
        ).decode("utf-8")  # transform bytes into string
        self.file_lines = self.file_contents.splitlines()
        # access to linewise xml file
        self.file_root = ET.fromstring(self.file_contents)
        # access to xml root
        self.lexicon = self.file_root.find("Lexicon")
        # access to lexicon (error checks later)
