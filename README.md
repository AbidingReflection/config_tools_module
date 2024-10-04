# Config Tools Module

This project provides tools for loading, validating, and managing configuration from YAML files, including logging and validation mechanisms.

## Features

- **ConfigLoader**: Loads YAML configuration files, validates them based on rules, and provides logging capabilities.
- **ConfigValidator**: Validates configuration values based on defined rules (e.g., checking URLs, ranges, non-empty strings).
- **Logging**: Uses `RotatingFileHandler` for log rotation and supports custom log formatting.
- **SensitiveDict**: A wrapper for sensitive config data to prevent direct access while allowing manipulation.

## Project Structure

```
config_tools_module/
│
├── config_tools/
│   ├── __init__.py
│   ├── config_loader.py        # Handles YAML config loading and validation
│   ├── config_validator.py     # Validation rules for config keys
│   ├── prepare_logger.py       # Sets up a logger with file and console handlers
│   ├── utils.py                # Utility functions (e.g., SensitiveDict)
│   ├── validation_rules_auth.py
│   ├── validation_rules_config.py
│   ├── tests/                  # Pytest tests for the modules
│       └── conftest.py         # Test configuration and fixtures
│       └── test_data/          # Sample YAML files for testing
├── requirements.txt            # Dependencies
├── scripts/
│   ├── generate_file_tree.py
│   ├── generate_max_config.py  # Generates max config YAML template
│   └── generate_min_config.py  # Generates minimal config YAML template
├── setup.py                    # Installation and packaging
```

## Usage

### Loading Configuration

```python
from config_tools.config_loader import ConfigLoader

config_loader = ConfigLoader(config_path="path/to/config.yaml")
config = config_loader.get_config()
```

### Validating Configuration

The `ConfigValidator` validates configurations against a set of defined rules:

```python
from config_tools.config_validator import ConfigValidator

validator = ConfigValidator(config, config_rules)
validator.validate()
```

### Logging

The logger is configured during initialization and supports both file and console logging:

```python
from config_tools.prepare_logger import prepare_logger

logger = prepare_logger(log_path="logs/")
logger.info("Logger initialized")
```

## Installation

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

To use the module in your project, add the following import:

```python
from config_tools.config_loader import ConfigLoader
```

## Running Tests

Tests are written using `pytest`. You can run the test suite as follows:

```bash
pytest
```

## License
This project is licensed under the MIT License.