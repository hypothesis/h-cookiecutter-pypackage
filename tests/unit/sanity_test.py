from h_cookiecutter_pypackage.dummy import data_exists, get_dummy


class TestSanity:
    def test_we_can_import_from_package(self):
        assert get_dummy()

    def test_we_are_not_running_from_local_directory(self):
        # This requires a data file to exist which we don't package up
        assert not data_exists("data_missing.txt")

    def test_we_have_expected_packaged_files(self):
        # This requires a data file to exist which we don't package up
        assert data_exists("data_present.txt")
