# copyright

from contextlib import contextmanager


class Manifest(object):

    def __init__(self, data):
        self.data = data

    @property
    def image(self):
        return self.data.get('image')

    @property
    def build(self):
        return self.data.get('build', [])

    def check(self):
        """Check and validate the manifest file"""
        if 'image' not in self.data:
            return "manifest missing 'image' directive"

    def realize(self, buildfile):
        pass


class Buildfile(object):
    """Representation of the shell script that will run inside of
    the container to perform the build.
    """

    def __init__(self):
        self._cmds = []
        self._cmd('#!/bin/bash')

    def _cmd(self, line):
        self._cmds.append(line)

    def cmd(self, fmt, *args):
        text = fmt.format(args)
        self._cmd(text)

    def build(self):
        return ''.join([line + '\n'
            for line in self._cmds])


def _service_image_and_name(service):
    names = service.split('/')
    return service, names[-1]


class Builder(object):
    """Takes a `Build` and makes it happen."""

    HOMEDIR = '/home/doozer'

    def __init__(self, eventbus, docker, build):
        self.eventbus = eventbus
        self.docker = docker
        self.build = build
        self._env = build.env.copy()
        self._services = []
        self._workdir = tempfile.mkdtemp()
        self._dotdir = os.path.join(self._workdir, '.doozer')
        self._buildfile = BuildFile()

    def _write_script(self):
        # start with writing all environment variables.
        for var, val in self._env.items():
            self._buildfile.export(var, val)
        self.build.realize(self._buildfile)
        with file(os.path.join(self._dotdir, 'script.sh')) as fp:
            fp.write(self._buildfile.build())

    def _setup_workdir(self):
        os.makedir(self._dotdir)
        # FIXME: write out SSH keys

    def _link_env(self, env, name, privport, proto, addr, pubport):
        name = name.upper()
        env[name + '_PORT_{}_{}'.format(privport, proto.upper)] = '{}://{}:{}'.format(
            proto, addr, pubport)

    def _update_env(self, name, container):
        addr = container.get('IPAddress')
        ports = container.get('NetworkSettings', {}).get('Ports', {})
        for priv_name, pubport in ports.items():
            privport, proto = priv_name.split('/', 1)
            self._link_env(self._env, name, int(privport),
                proto, addr, int(pubport))

    def _start_services(self):
        """Start the services that this build depends on.

        Will update `_env` to hold information on how to talk
        to the service.
        """
        for service in self.build.services:
            image, name = _service_image_and_name(service)
            c = self.docker.create_container(image)
            self.docker.start(c, publish_all_ports=True)
            inspect = self.docker.inspect_container(c)
            self._update_env(name, inspect)
            self._services.append(c)

    def _start(self):
        """Start the actual container."""
        self._container = self.docker.create_container(
            command=os.path.join(self._dotdir, 'script.sh'),
            environment=_make_environment(self._env),
            working_dir=self.HOMEDIR)
        binds = {self.HOMEDIR: self._workdir}
        self.docker.start(self._container, binds=binds)
        self.docker.wait(self._container)

    def start(self):
        """Start the build."""
        self._setup_workdir()
        self._start_services()
        self._write_script()
        self._start()


class Build(object):
    """
    """

    def __init__(self, name, image, env, services):
        self.name = name
        self.image = image
        self.env = env
        self.services = services
        self.created_at = None
        self.finished_at = None





class Commit(object):
    """

    A commit may result in multiple builds, depending on the configuration.
    """

    def __init__(self):
        self._script_data = None



class Repository(object):
    """

    """
