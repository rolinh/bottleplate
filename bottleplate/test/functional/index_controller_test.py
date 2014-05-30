import unittest
from webtest import TestApp

import test_helper


class IndexControllerTests(unittest.TestCase):

    def test_index(self):
        app = TestApp(test_helper.get_app())
        assert app.get('/').status == '200 OK'
