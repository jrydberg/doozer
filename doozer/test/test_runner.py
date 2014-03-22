# Copyright 2014 Johan Rydberg.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import shutil
import tempfile
import os

from mockito import when, verify, any, mock

from ..build import Manifest
from .. import runner


class RunnerTestCase(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        when(runner.tempfile).mkdtemp().thenReturn(self.dir)
        when(runner.shutil).rmtree(self.dir).thenReturn(None)
        self.container = mock()
        when(self.container).wait().thenReturn(1)
        self.factory = mock()
        when(self.factory).create('image', binds=any()).thenReturn(self.container)
        self.runner = runner.Runner(self.factory.create)
        self.manifest = Manifest(dict(image="image", build=["/bin/false"]))

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_execute_build_steps_and_return_result(self):
        result = self.runner.execute(self.manifest)
        self.assertEquals(result, 1)

    def test_creates_build_script_from_manifest(self):
        result = self.runner.execute(self.manifest)
        self.assertTrue(os.path.exists(os.path.join(self.dir,
            'build.sh')))

    def test_execute_build_script_in_container(self):
        self.runner.execute(self.manifest)
        verify(self.container).start(any(str))
