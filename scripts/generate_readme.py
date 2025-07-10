# scripts/generate_readme.py
# Script version: 1.0.0

"""
Generate the README.md file from the template.
- Automatically replace the placeholders with the actual values.
- Started by running the script manually or setting up a pre-commit hook.
"""

import json

# Read variables from config.yaml
with open("scripts/config.json", "r") as f:
    variables = json.load(f)

def flatten_dict(d, parent_key='', sep='.'):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

variables = flatten_dict(variables)

# Read the template
with open("README.template.md", "r") as f:
    content = f.read()

# Replace placeholders with actual values
for key, value in variables.items():
    content = content.replace(f"{{{{{key}}}}}", str(value))

# Write the final README.md
with open("README.md", "w") as f:
    f.write(content)