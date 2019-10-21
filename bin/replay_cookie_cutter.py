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
parser.add_argument('-t', '--template')
parser.add_argument('-o', '--output-directory')


class CookieCutter:
    @classmethod
    def replay(cls, template, config, project_dir):
        project_dir = os.path.abspath(project_dir)

        temp_dir = mkdtemp()

        try:
            project_name = cls.render_template(template, config, target_dir=temp_dir)
            current_name = os.path.basename(project_dir)

            if project_name != current_name:
                raise EnvironmentError(
                    'The project created does not match the project directory: '
                    f'Created {project_name}, existing {current_name}')

            copy_tree(os.path.join(temp_dir, project_name), project_dir)

            return project_name

        finally:
            shutil.rmtree(temp_dir)

    @classmethod
    def render_template(cls, template, config, target_dir=None):
        cookiecutter(
            template=template, no_input=True,
            extra_context=config, output_dir=target_dir)

        items = os.listdir(target_dir)
        assert len(items) == 1, 'There is a unique file in the output dir'
        return items[0]

    @classmethod
    def read_config(cls, config_file):
        with open(config_file) as fh:
            config = json.load(fh)

        return config['_template'], config


def run():
    args = parser.parse_args()

    template, config = CookieCutter.read_config(args.config)
    template = args.template or template

    project_name = CookieCutter.replay(
        template=template,
        config=args.config,
        project_dir=args.directory or os.getcwd()
    )

    print(f"Recreated {project_name} from {template}")
    print("You should now check for updated files...")


if __name__ == '__main__':
    run()


