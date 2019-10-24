import json
import os
import os.path
import shutil
from unittest import mock

import pytest

from bin.replay_cookie_cutter import CookieCutter, run


class TestScript:
    def test_sanity(self, CookieCutter, config):
        # This is unfortunately kind of a one and done test
        # It hits everything it needs to in one go (json, args, calls)
        run()

        CookieCutter.replay.assert_called_once_with(
            project_dir=mock.sentinel.output_directory, config=config
        )

    @pytest.fixture
    def config(self):
        return {"some_config_here": True, "_template": "config_template"}

    @pytest.fixture
    def config_file(self, config, tmp_path):
        filename = os.path.join(tmp_path, ".cookiecutter.json")
        with open(filename, "w") as handle:
            json.dump(config, handle)

        return filename

    @pytest.fixture(autouse=True)
    def PARSER(self, patch, config_file):
        PARSER = patch("bin.replay_cookie_cutter.PARSER")

        args = PARSER.parse_args()
        args.config = config_file
        args.output_directory = mock.sentinel.output_directory

        return PARSER

    @pytest.fixture
    def CookieCutter(self, patch):
        return patch("bin.replay_cookie_cutter.CookieCutter")


class TestCookieCutter:
    def test_it_can_get_template_from_config(self, config):
        template = CookieCutter.get_template_from_config(config)

        assert template == config["_template"]

    def test_it_can_render_template(self, tmp_path, config, template):
        package_name = CookieCutter.render_template(
            project_dir=tmp_path, config=config, template=template
        )

        assert package_name == config["project_slug"]

        self.assert_file_exists(tmp_path, config["project_slug"], "Makefile")
        self.assert_file_exists(
            tmp_path, config["project_slug"], "src", config["pkg_name"], "__init__.py"
        )

    def test_render_will_read_template_from_config(self, tmp_path, cookiecutter):
        config = {"_template": mock.sentinel.template}

        CookieCutter.render_template(tmp_path, config=config)

        cookiecutter.assert_called_once_with(
            template=mock.sentinel.template,
            no_input=True,
            extra_context=config,
            output_dir=tmp_path,
        )

    def test_it_can_replay_template(self, existing_project, config):
        # Mess with it
        setup_py = os.path.join(existing_project, "setup.py")
        os.unlink(setup_py)
        makefile = self.write_string(existing_project, "Makefile", "Nonsense")
        another_file = self.write_string(
            existing_project, "something_new.txt", "Nonsense 2"
        )

        # Replay and check
        CookieCutter.replay(project_dir=existing_project, config=config)

        self.assert_file_exists(setup_py)
        self.assert_file_exists(makefile)
        self.assert_file_exists(another_file)

        self.assert_file_contains(makefile, "tox")

    def test_it_can_replay_ignoring_files(self, tmp_path, config):
        # If we disable replay on a file
        config["options"] = {"disable_replay": ["Makef*", "setup.cfg"]}

        # ... and render out the project
        package_name = CookieCutter.render_template(project_dir=tmp_path, config=config)
        project_dir = os.path.join(tmp_path, package_name)

        # ... and add some custom nonsense in that file
        makefile = self.write_string(project_dir, "Makefile", "Nonsense")
        # ... and remove a file
        setup_cfg = os.path.join(project_dir, "setup.cfg")
        os.unlink(setup_cfg)

        # Then when we replay the project
        CookieCutter.replay(project_dir=project_dir, config=config)

        # The nonsense is still in the file
        self.assert_file_contains(makefile, "Nonsense")
        self.assert_file_exists(setup_cfg)

    def test_if_fails_when_template_does_not_match_project(
        self, tmp_path, existing_project, config
    ):
        new_name = os.path.join(tmp_path, "something_new")
        shutil.move(existing_project, new_name)

        with pytest.raises(ValueError):
            CookieCutter.replay(project_dir=new_name, config=config)

    @pytest.fixture
    def cookiecutter(self, patch, tmp_path):
        cookiecutter = patch("bin.replay_cookie_cutter.cookiecutter")
        # If we are called, make it look like we produced a directory in tmp
        cookiecutter.side_effect = os.mkdir(os.path.join(tmp_path, "example_project"))
        return cookiecutter

    def write_string(self, directory, filename, content):
        filename = os.path.join(directory, filename)
        with open(filename, "w") as handle:
            handle.write(content)

        return filename

    def assert_file_contains(self, path, content):
        with open(path) as handle:
            text = handle.read()

        assert content in text

    def assert_file_exists(self, parent_dir, *parts):
        assert os.path.isfile(os.path.join(parent_dir, *parts))
