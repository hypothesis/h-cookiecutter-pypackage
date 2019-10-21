import json

# Save the cookie cutter config to replay later
with open('.cookiecutter.json', 'w') as fh:
    json.dump({{ cookiecutter }}, fh, indent=4)