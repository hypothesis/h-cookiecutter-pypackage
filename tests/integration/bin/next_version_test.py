import os
from unittest.mock import create_autospec

import pytest
from bin.next_version import VersionSuggester
from packaging import version


class TestVersionSuggester:
    def test_it_fails_without_setup_cfg(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            VersionSuggester.major_minor_version()

    def test_it_can_read_setup_cfg(self, project_dir):
        assert VersionSuggester.major_minor_version() == version.parse("1.3")

    def test_it_can_read_git_tag(self, check_output):
        check_output.return_value = b"v1.0.4\nv1.0.3\nv1.0.2"

        assert VersionSuggester.last_tag() == version.parse("1.0.4")

    def test_it_can_fail_to_read_git_tag_returning_None(self, check_output):
        check_output.return_value = b""

        assert VersionSuggester.last_tag() is None

    def test_it_suggests_zero_with_no_tag(self, project_dir, VersionSuggester):
        VersionSuggester.last_tag.return_value = None

        assert VersionSuggester.suggest_tag() == "v1.3.0"

    def test_it_increments_a_matching_tag(self, project_dir, VersionSuggester):
        VersionSuggester.last_tag.return_value = version.parse("1.3.4")

        assert VersionSuggester.suggest_tag() == "v1.3.5"

    def test_it_jumps_if_tag_is_old(self, project_dir, VersionSuggester):
        VersionSuggester.last_tag.return_value = version.parse("1.2.4")

        assert VersionSuggester.suggest_tag() == "v1.3.0"

    def test_it_crashes_if_tag_is_newer(self, project_dir, VersionSuggester):
        VersionSuggester.last_tag.return_value = version.parse("1.5.4")

        with pytest.raises(ValueError):
            VersionSuggester.suggest_tag()

    @pytest.fixture
    def check_output(self, patch):
        return patch("bin.next_version.check_output")

    @pytest.fixture()
    def VersionSuggester(self, patch):
        class TestableSuggester(VersionSuggester):
            last_tag = create_autospec(VersionSuggester.last_tag)

        return TestableSuggester

    @pytest.fixture
    def project_dir(self, tmpdir):
        current_dir = os.getcwd()

        try:
            tmpdir.join("setup.cfg").write("[metadata]\nversion = 1.3\n")

            os.chdir(tmpdir)
            yield tmpdir
        finally:
            os.chdir(current_dir)
