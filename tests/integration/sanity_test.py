import os


class TestSanity:
    """
    Some basic 'the world isn't falling down' tests. These do not ensure
    anything is fine, but if any of these break you definitely have trouble.
    """

    def test_all_files_in_root_accounted_for(self, template):
        template_dir = "{{ cookiecutter.project_slug }}"
        expected_files = set(os.listdir(template))
        templated_files = set(os.listdir(os.path.join(template, template_dir)))

        missing = expected_files - templated_files

        # Remove a bunch of files we expect to see around, but do not come
        # from the template
        missing -= {
            # OS specific noise
            ".DS_store",
            # General development waffle
            ".git",
            ".idea",
            ".tox",
            ".pytest_cache",
            ".eggs",
            "dist",
            "build",
            "__pycache__",
            "h_cookiecutter_pypackage.egg-info",
            ".coverage",
            # Expected resources that shouldn't be there
            ".cookiecutter.json",
            "cookiecutter.json",
            "hooks",
            "h_cookiecutter_pypackage",
            template_dir,
        }

        # Coverage produces files with un-predictable names. Strip them out
        missing = {name for name in missing if not name.startswith(".coverage.")}

        assert not missing
