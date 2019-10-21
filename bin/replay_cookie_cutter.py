"""
A script for re-applying a cookiecutter template over a project
"""
import fnmatch
import json
import os
import os.path
import shutil
from argparse import ArgumentParser
from distutils.dir_util import mkpath
from tempfile import mkdtemp

from cookiecutter.main import cookiecutter

PARSER = ArgumentParser()
PARSER.add_argument("-c", "--config", required=True)
PARSER.add_argument("-t", "--template")
PARSER.add_argument("-o", "--output-directory")


class CookieCutter:
    """
    A collection of cookie cutter related functions
    """

    @classmethod
    def replay(cls, project_dir, config, template=None):
        """
        Replay a project based on the config provided. The value in '_template'
        will be used to decide which template to replay if none is provided.

        :param project_dir: The target directory
        :param config: The config to apply
        :param template: The template to apply
        :return: The name of the project created
        """
        project_dir = os.path.abspath(project_dir)
        disable_replay = config.get("options", {}).get("disable_replay")

        temp_dir = mkdtemp()

        try:
            project_name = cls.render_template(temp_dir, config, template)
            current_name = os.path.basename(project_dir)

            if project_name != current_name:
                raise EnvironmentError(
                    "The project created does not match the project directory: "
                    f"Created {project_name}, existing {current_name}"
                )

            # copy_tree(os.path.join(temp_dir, project_name), project_dir)
            cls._copy_tree(
                os.path.join(temp_dir, project_name),
                project_dir,
                skip_patterns=disable_replay,
            )

            return project_name

        finally:
            shutil.rmtree(temp_dir)

    @classmethod
    def _matches_pattern(cls, filename, skip_patterns):
        """
        Check if the filename matches any of the patterns in skip_patterns.
        These patterns are bash style globs like 'thing/*.txt'
        """
        for pattern in skip_patterns:
            if fnmatch.fnmatch(filename, pattern):
                print(f"Skipping: '{filename}' as it matched pattern '{pattern}'")
                return True

        return False

    @classmethod
    def _copy_tree(cls, source_dir, target_dir, skip_patterns=None):
        """
        Copy a directory over another one optionally skipping files which match
        the specified glob style patterns like 'thing/*.txt'
        """
        if not skip_patterns:
            skip_patterns = []

        all_files = []
        for parent_dir, _, filenames in os.walk(source_dir):
            for filename in filenames:
                rel_path = os.path.relpath(
                    os.path.join(parent_dir, filename), source_dir
                )

                if not cls._matches_pattern(rel_path, skip_patterns):
                    all_files.append(rel_path)

        for rel_path in all_files:
            source = os.path.join(source_dir, rel_path)
            target = os.path.join(target_dir, rel_path)

            mkpath(os.path.dirname(target))
            shutil.copyfile(source, target)

    @classmethod
    def render_template(cls, project_dir, config, template=None):
        """
        Create a project based on the config provided. The value in '_template'
        will be used to decide which template to replay if none is provided.

        :param project_dir: The target directory
        :param config: The config to apply
        :param template: The template to apply
        :return: The name of the project created
        """
        if template is None:
            template = cls.get_template_from_config(config)

        cookiecutter(
            template=template,
            no_input=True,
            extra_context=config,
            output_dir=project_dir,
        )

        items = os.listdir(project_dir)
        assert len(items) == 1, "There is a unique file in the output dir"
        return items[0]

    @classmethod
    def get_template_from_config(cls, config):
        """Read the template from a config file"""

        # This is basically here to hide the standard cookiecutter secret
        # location to read this from the consumer
        return config["_template"]


def run():
    """Main entry-point to run the script"""

    args = PARSER.parse_args()

    with open(args.config) as handle:
        config = json.load(handle)

    template = args.template or CookieCutter.get_template_from_config(config)

    project_name = CookieCutter.replay(
        project_dir=args.output_directory or os.getcwd(),
        config=config,
        template=template,
    )

    print(f"Recreated {project_name} from {template}")
    print("You should now check for updated files...")


if __name__ == "__main__":
    run()
