import argparse
import os
import sys
import yaml

from .build import Manifest

def _main(dir, runner):
    if not os.path.exists(os.path.join(dir, '.doozer.yaml')):
        sys.exit("no doozer (.doozer.yml) manifest in directory")

    with open(os.path.join(dir, '.doozer.yaml')) as fp:
        manifest = Manifest(yaml.load(fp.read()))

    result = runner.execute(manifest)
    sys.exit(result)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", default=os.getcwd(),
        help="directory where to perform the build",
        nargs='?')
    args = parser.parse_args()
    _main(args.dir)

if __name__ == '__main__':
    main()
