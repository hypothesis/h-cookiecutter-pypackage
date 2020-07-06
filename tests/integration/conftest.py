import os

import pytest

from bin.replay_cookie_cutter import CookieCutter


@pytest.fixture
def template():
    this_file = os.path.realpath(__file__)
    root = os.path.abspath(os.path.join(os.path.dirname(this_file), "../../"))

    return root


@pytest.fixture
def config(template):
    return {
        "project_slug": "h-test-lib",
        "pkg_name": "h_test_lib",
        "_template": template,
    }


@pytest.fixture
def existing_project(tmp_path, config):
    project_name = CookieCutter.render_template(project_dir=tmp_path, config=config)

    return os.path.join(tmp_path, project_name)
