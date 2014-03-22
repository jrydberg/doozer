import tempfile
import shutil
from functools import partial

from mockito import mock, when, any

from doozer import runner, script, container


def before_all(ctx):
    ctx.dir = tempfile.mkdtemp()
    ctx.docker = mock()
    ctx.container_factory = partial(container.Container, ctx.docker)
    ctx.manifest = {}
    ctx.runner = runner.Runner(ctx.container_factory)
    when(script.sys).exit(any()).thenReturn(0)


def after_all(ctx):
    shutil.rmtree(ctx.dir)
