from h_cookiecutter_pypackage.dummy import get_dummy


class TestSanity:
    def test_we_can_import_from_package(self):
        assert get_dummy()
