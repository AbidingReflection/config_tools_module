from pathlib import Path
from typing import Union, Optional, Dict
import yaml
from .config_validator import ConfigValidator
from .prepare_logger import prepare_logger
import json
import logging

class ConfigLoader:
    def __init__(self, config_path: Union[str, Path], config_rules=None, auth_rules=None):
        try:
            # Convert string to path if needed
            self.config_path: Path = self.convert_str_to_path(config_path)
            self.validate_yaml_path(self.config_path)
            self.config: Optional[Dict] = self.extract_config_from_yaml(self.config_path)

            # Store the validation rules provided by the project using the module
            self.config_rules = config_rules or {}
            self.auth_rules = auth_rules or {}

            # Check self.config for log_path or "log path"
            log_path = self.get_log_path()

            # Get log_name_prefix or "log name prefix" from config, default to ""
            log_name_prefix = self.get_log_name_prefix()

            # Pass the logger to prepare_logger to add final handlers
            self.logger = prepare_logger(log_path, log_name_prefix)
            self.logger.info(f"Logger initialized with log output directory: '{log_path}'")
            
            self.config["logger"] = self.logger

            # Validate the extracted config based on the config rules
            if self.config is not None:
                self.validate_config(self.config)
                self.logger.info("Config validated successfully")
            
            # Check for 'authentication_path' in the config
            if 'authentication_path' in self.config:
                auth_path = self.config['authentication_path']
                self.load_authentication_config(auth_path)
                self.logger.info(f"Authentication config loaded from '{auth_path}'")
                self.logger.info(f'Config loaded successfully. Loaded config:\n {json.dumps(self.config, indent=4, cls=SensitiveDictEncoder)}')
        
        except (FileNotFoundError, IsADirectoryError, ValueError, yaml.YAMLError) as e:
            raise e
        
    def get_config(self) -> Dict:
        return self.config

    def get_log_path(self) -> str:
        """Check for log_path in the config and validate it. Return 'logs/' folder as default if not valid."""
        log_path = self.config.get('log_path', 'logs') if self.config else 'logs'
        log_path = Path(log_path)

        if log_path.exists():
            if log_path.is_file():
                log_path = Path('logs')
                log_path.mkdir(parents=True, exist_ok=True)
        else:
            log_path.mkdir(parents=True, exist_ok=True)

        if log_path.is_dir():
            return str(log_path)
        else:
            default_log_path = Path('logs')
            default_log_path.mkdir(parents=True, exist_ok=True)
            return str(default_log_path)

    def get_log_name_prefix(self) -> str:
        """Get the log name prefix from the config. Check for 'log_name_prefix' or 'log name prefix'."""
        return self.config.get('log_name_prefix', self.config.get('log name prefix', ''))

    def convert_str_to_path(self, path_string_or_path: Union[str, Path]) -> Path:
        """Convert a string to a Path object."""
        if isinstance(path_string_or_path, str):
            return Path(path_string_or_path)
        elif isinstance(path_string_or_path, Path):
            return path_string_or_path
        else:
            raise ValueError("Provided path must be a string or Path object")

    def validate_yaml_path(self, path: Path) -> None:
        """Validate that the path is a valid YAML file."""
        if not path.exists():
            raise FileNotFoundError(f"The file '{path}' does not exist.")
        if not path.is_file():
            raise IsADirectoryError(f"'{path}' is a directory, not a file.")
        if not path.suffix == ".yaml":
            raise ValueError(f"'{path}' is not a YAML file. Must end with .yaml.")

    def extract_config_from_yaml(self, path: Path) -> Optional[Dict]:
        """Extract configuration from YAML file."""
        try:
            with open(path, 'r') as file:
                config_data = yaml.safe_load(file)

                if not isinstance(config_data, dict):
                    raise ValueError("YAML file content is not a valid dictionary.")
                
                return config_data

        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

    def validate_config(self, config: Dict) -> None:
        """Validate the config using the ConfigValidator and the provided config_rules."""
        try:
            validator = ConfigValidator(config, self.config_rules)
            validator.validate()
        except ValueError as e:
            self.logger.error(f"Config validation error: {e}")
            raise ValueError(f"Config validation error: {e}")

    def load_authentication_config(self, auth_path: str) -> None:
        """Load the authentication YAML file into CONFIG["auth"] using the extract_config_from_yaml method."""
        auth_path_obj = Path(auth_path)
        if not auth_path_obj.exists() or not auth_path_obj.is_file():
            raise FileNotFoundError(f"Authentication path '{auth_path}' does not exist or is not a valid file.")
        
        auth_config = self.extract_config_from_yaml(auth_path_obj)
        if auth_config:
            self.config["auth"] = SensitiveDict(auth_config)
            self.logger.info("Authentication data loaded into config")
        
        # Validate authentication config using the provided auth_rules
        validator = ConfigValidator(self.config['auth'].get_data(), self.auth_rules)
        validator.validate()
        self.logger.info("Authentication data validated successfully")


class SensitiveDict:
    def __init__(self, data):
        self._data = data

    def __repr__(self):
        return "<SensitiveDict>"

    def __str__(self):
        return self.__repr__()

    def get_data(self):
        return self._data
    

class SensitiveDictEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SensitiveDict):
            return str(obj)
        if isinstance(obj, logging.Logger):
            return "<Logger>"
        return super().default(obj)
