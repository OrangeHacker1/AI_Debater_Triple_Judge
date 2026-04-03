# Run this comand to install yaml.
# py -m pip install PyYAML


import yaml

# Load the configuration  variables
def load_config(path="config/config.yaml"):
    with open(path, "r") as file:
        config = yaml.safe_load(file)

    return config
