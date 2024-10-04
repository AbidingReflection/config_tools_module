import sys
from pathlib import Path
import yaml

# Add the correct path to sys.path to ensure the config_tools module is found
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root / 'config_tools_module'))

# Now we can import from config_tools
from config_tools.validation_rules_config import config_rules

def generate_max_config(config_rules, output_path):
    """Generate a maximal YAML configuration file with None values for all fields."""
    config_template = {}

    for key, rules in config_rules.items():
        # Set all fields to None by default (including both required and optional)
        config_template[key] = None

    # Write the template to a YAML file
    with open(output_path, 'w') as yaml_file:
        yaml.dump(config_template, yaml_file)

    print(f"Generated maximal config file at: {output_path}")

if __name__ == "__main__":
    # Set the output path for the example YAML file
    output_path = Path('scripts/example_max_config.yaml')

    # Generate the maximal configuration file
    generate_max_config(config_rules, output_path)
