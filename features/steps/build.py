import yaml
import os

import behave

from mockito import mock, when, verify, any

from doozer import script


@behave.given('a manifest with build step "{command}"')
def step(ctx, command):
    manifest = dict(image="image", build=[command])
    with open(os.path.join(ctx.dir, '.doozer.yaml'), 'w') as fp:
        fp.write(yaml.dump(manifest))


@behave.when('I build my software')
def step(ctx):
    script._main(ctx.dir, ctx.runner)


@behave.then('doozer exits with exit code {code}')
def step(ctx, code):
    verify(script.sys).exit(int(code))
