"""rgapps.tests.domain.units.length module

Unit test for rgapps.domain.units.length module
"""
import logging
import os
import unittest

from rgapps.config import ini_config
from rgapps.domain.units.length import Length


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"


class LengthUnitTestCase(unittest.TestCase):

    LOG_FILE_PATH = ini_config.get("Logging","LOG_FILE")

    def setUp(self):
        return

    def tearDown(self):
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler(handler)
        if os.path.isfile(LengthUnitTestCase.LOG_FILE_PATH):
            os.remove(LengthUnitTestCase.LOG_FILE_PATH)
        return

    def test_length_convert(self):
        logging.debug("testing length convert")
        result = Length.convert(1800, "meter", "mile")
        self.assertIsNotNone(result)
        return

