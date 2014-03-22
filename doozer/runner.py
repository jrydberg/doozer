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

import shutil
import tempfile
import os

from .build import Buildfile


class Runner(object):
    """The runner is responsible for taking a manifest and executing it."""

    def __init__(self, container_factory):
        self.container_factory = container_factory

    def _write_build_script(self, dir, manifest):
        """Write out script for the build phase."""
        buildfile = Buildfile()
        for step in manifest.build:
            buildfile.cmd(step)
        with open(os.path.join(dir, 'build.sh'), 'w') as fp:
            fp.write(buildfile.build())

    def execute(self, manifest):
        dir = tempfile.mkdtemp()
        try:
            self._write_build_script(dir, manifest)
            container = self.container_factory(
                manifest.image, binds={'/home/doozer': dir})
            container.start('/home/doozer/build.sh')
            return container.wait()
        finally:
            shutil.rmtree(dir)
