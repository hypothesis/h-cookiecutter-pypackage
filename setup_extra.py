import os


class Package:
    def __init__(self, name, version):
        self.name = name
        self.version = version

    @classmethod
    def read_string(cls, filename):
        with open(filename) as fh:
            return fh.read()

    @classmethod
    def read_list(cls, filename):
        with open(filename) as fh:
            return [
                line
                for line in (raw_line.strip() for raw_line in fh)
                if line and not line.startswith("#")
            ]

    def read_egg_version(self):
        pkg_info_file = self.name + ".egg-info/PKG-INFO"
        if not os.path.isfile(pkg_info_file):
            return None

        with open(pkg_info_file) as fh:
            for line in fh:
                if line.startswith("Version"):
                    return line.strip().split("Version: ")[-1]

    def get_version(self, build_var="BUILD"):
        # If we have a build argument we should honour it no matter what
        build = os.environ.get(build_var)
        if build:
            return self.version + "." + build

        # If not, we should try and read it from the .egg-info/ data

        # We need to do this for source distributions, as setup.py is re-run when
        # installed this way, and we would always get 'dev0' as the version
        # Wheels and binary installs don't work this way and read from PKG-INFO
        # for them selves
        egg_version = self.read_egg_version()
        if egg_version:
            return egg_version

        # Otherwise create a 'dev' build which will be counted by pip as 'later'
        # than the major version no matter what
        return self.version + ".dev0"
