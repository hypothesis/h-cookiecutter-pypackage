import json
# Looks like cookiecutter has started using an OrderedDict for the
# `cookiecutter` object. If we don't import this first we will fail when
# that is included in our script.
from collections import OrderedDict

# Save the cookie cutter config to replay later
with open(".cookiecutter.json", "w") as fh:
    json.dump({{cookiecutter}}, fh, indent=4)
