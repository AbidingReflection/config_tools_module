import sys
from pathlib import Path
import yaml

# Add the correct path to sys.path to ensure the config_tools module is found
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root / 'config_tools_module'))

# Now we can import from config_tools
from config_tools.validation_rules_config import config_rules

def generate_min_config(config_rules, output_path):
    """Generate a minimal YAML configuration file with None values for all required fields."""
    config_template = {}

    for key, rules in config_rules.items():
        if rules.get('required', False):
            config_template[key] = None

    # Write the template to a YAML file
    with open(output_path, 'w') as yaml_file:
        yaml.dump(config_template, yaml_file)

    print(f"Generated minimal config file at: {output_path}")

if __name__ == "__main__":
    # Set the output path for the example YAML file
    output_path = Path('scripts/example_config.yaml')

    # Generate the minimal configuration file
    generate_min_config(config_rules, output_path)
