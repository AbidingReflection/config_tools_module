from typing import Dict, Any, Optional, Union, List
from datetime import datetime, date, timedelta
import re

class ConfigValidator:
    def __init__(self, config: Dict[str, Any], rules: Dict[str, Dict[str, Any]]):
        self.config = config
        self.rules = rules

    def validate(self) -> None:
        """Run validation on the config."""
        for key, rule in self.rules.items():
            value = self.config.get(key)
            if 'required' in rule and rule['required'] and value is None:
                raise ValueError(f"Missing required config key: '{key}'")
            
            if value is not None and 'validator' in rule:
                rule['validator'](key, value)

    @staticmethod
    def validate_https_url(key: str, value: str) -> None:
        """Validate that a URL starts with HTTPS:// (case-insensitive) and ends with /."""
        if not value.lower().startswith('https://'):
            raise ValueError(f"Config key '{key}' must start with 'HTTPS://'. Found: '{value}'")
        if not value.endswith('/'):
            raise ValueError(f"Config key '{key}' must end with '/'. Found: '{value}'")
        

    @staticmethod
    def validate_log_prefix(key: str, value: str) -> None:
        if not value.lower().endswith('_'):
            raise ValueError(f"log_name_prefix '{key}' must end with '_'. Found: '{value}'")


    @staticmethod
    def validate_int_range(key: str, value: int, min_value: Optional[int] = None, max_value: Optional[int] = None) -> None:
        """Validate that an integer falls within an optional range."""
        if min_value is not None and value < min_value:
            raise ValueError(f"Config key '{key}' must be greater than or equal to {min_value}. Found: {value}")
        if max_value is not None and value > max_value:
            raise ValueError(f"Config key '{key}' must be less than or equal to {max_value}. Found: {value}")

    @staticmethod
    def validate_non_empty_string(key: str, value: str) -> None:
        """Ensure that a string value is not empty."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Config key '{key}' must be a non-empty string. Found: '{value}'")

    @staticmethod
    def validate_qTest_bearer_token(key: str, value: str) -> None:
        """Ensure that a string value is not empty and matches a valid UUID pattern."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Config key '{key}' must be a non-empty string. Found: '{value}'")
        
        # UUID regex pattern
        bearer_token_pattern = re.compile(r'^Bearer [a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$')
        
        # Check if value matches the UUID pattern
        if not bearer_token_pattern.fullmatch(value):
            raise ValueError(f"Auth Config key '{key}' must be a Bearer Token in the format 'Bearer <UUID>'. Found: '{value}'")

    @staticmethod
    def validate_date(key: str, value: date, min_date: Optional[datetime] = None) -> None:
        """Validate that a date object falls within a valid range. Default min_date is 365 days before the current date."""
        
        if not isinstance(value, date):
            raise ValueError(f"Config key '{key}' must be a valid date object. Found: '{value}'")
        
        # Set default min_date to 365 days before current date if not provided
        if min_date is None:
            min_date = datetime.now().date() - timedelta(days=365)
        
        # Check if the value is before the minimum date
        if value < min_date:
            raise ValueError(f"Config key '{key}' must be on or after {min_date}. Found: {value}")


    @staticmethod
    def validate_string_in_list(key: str, value: Union[str, List[str]], target_list: List[str]) -> None:
        """Validate that a string or list of strings exists in a target list."""
        
        # Convert single string to a list for uniform processing
        if isinstance(value, str):
            value = [value]
        elif not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError(f"Config key '{key}' must be a string or a list of strings. Found: {value}")
        
        # Check if all strings in the list exist in the target list
        for item in value:
            if item not in target_list:
                raise ValueError(f"Config key '{key}' contains an invalid value '{item}'. Allowed values are: {target_list}")