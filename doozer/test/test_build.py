import unittest

from ..build import Buildfile


class ManifestTestCase(unittest.TestCase):

    def setUp(self):
        self.data = {
            "image": "my-image",
            "build": [
                "echo hello"
            ]
        }



class BuiltfileTestCase(unittest.TestCase):

    def setUp(self):
        self.buildfile = Buildfile()

    # starting with it, ensure, should, must, spec, example, deve)

    # test <that it> should|must|

    def test_should_have_a_shebang_at_the_start(self):
        output = self.buildfile.build()
        self.assertTrue(output.startswith("#!/bin/bash"))

    def test_sums_up_all_commands(self):
        self.buildfile.cmd("echo 1")
        self.buildfile.cmd("echo 2")
        output = self.buildfile.build()
        self.assertTrue("echo 1\n" in output)
        self.assertTrue("echo 2\n" in output)
        
