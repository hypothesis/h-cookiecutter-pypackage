import os
import os.path
import pytest

from bin.replay_cookie_cutter import CookieCutter


class TestCookieCutter:
    @classmethod
    def _get_project_root(cls):
        this_file = os.path.realpath(__file__)
        return os.path.abspath(
            os.path.join(os.path.basename(this_file), "../../../../")
        )

    def test_it_can_get_template_from_config(self, config):
        template = CookieCutter.get_template_from_config(config)

        assert template == config["_template"]

    def test_it_can_render_template(self, tmp_path, config):
        package_name = CookieCutter.render_template(
            project_dir=tmp_path, config=config, template=self._get_project_root()
        )

        assert package_name == config["project_slug"]

        self.assert_file_exists(tmp_path, config["project_slug"], "Makefile")
        self.assert_file_exists(
            tmp_path, config["project_slug"], config["pkg_name"], "__init__.py"
        )

    def test_it_can_replay_template(self, tmp_path, config):
        # Render out the project
        package_name = CookieCutter.render_template(
            project_dir=tmp_path, config=config, template=self._get_project_root()
        )
        project_dir = os.path.join(tmp_path, package_name)

        # Mess with it
        setup_py = os.path.join(project_dir, "setup.py")
        os.unlink(setup_py)
        makefile = self.write_string(project_dir, "Makefile", "Nonsense")
        another_file = self.write_string(project_dir, "something_new.txt", "Nonsense 2")

        # Replay and check
        CookieCutter.replay(
            project_dir=project_dir, config=config, template=self._get_project_root()
        )

        self.assert_file_exists(setup_py)
        self.assert_file_exists(makefile)
        self.assert_file_exists(another_file)

        self.assert_file_contains(makefile, "tox")

    @pytest.fixture
    def config(self):
        return {
            "project_slug": "h-test-lib",
            "pkg_name": "h_test_lib",
            "_template": self._get_project_root(),
        }

    def write_string(self, directory, filename, content):
        filename = os.path.join(directory, filename)
        with open(filename, "w") as fh:
            fh.write(content)

        return filename

    def assert_file_contains(self, path, content):
        with open(path) as fh:
            text = fh.read()

        assert content in text

    def assert_file_exists(self, parent_dir, *parts):
        assert os.path.isfile(os.path.join(parent_dir, *parts))
