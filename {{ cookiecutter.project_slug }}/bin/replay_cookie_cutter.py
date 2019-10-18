import json
import os
import os.path
import shutil

from argparse import ArgumentParser
from cookiecutter.main import cookiecutter
from distutils.dir_util import copy_tree
from tempfile import mkdtemp


parser = ArgumentParser()
parser.add_argument('-c', '--config', required=True)
parser.add_argument('-d', '--directory')


def _replay_cookiecutter(config, target_dir):
    temp_dir = mkdtemp()
    target_dir = os.path.abspath(target_dir)

    try:
        template = config['_template']

        cookiecutter(template=template, no_input=True, extra_context=config, output_dir=temp_dir)

        # Check the directories have the same name
        items = os.listdir(temp_dir)
        assert len(items) == 1, 'There is a unique file in the output dir'
        project_name = items[0]
        current_name = os.path.basename(target_dir)
        if project_name != current_name:
            raise EnvironmentError(
                'The project created matches the target directory: '
                f'Created {project_name}, existing {current_name}')

        source_dir = os.path.join(temp_dir, items[0])
        copy_tree(source_dir, target_dir)

        print(f"Recreated {project_name} from {template}")
        print("You should now check for updated files...")

    finally:
        shutil.rmtree(temp_dir)


def run():
    args = parser.parse_args()

    with open(args.config) as fh:
        config = json.load(fh)

    _replay_cookiecutter(config, target_dir=args.directory or os.getcwd())


if __name__ == '__main__':
    run()


