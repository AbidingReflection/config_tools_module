import pytest
from modules.config.validation_rules_auth import auth_rules
from modules.config.config_validator import ConfigValidator

def test_valid_auth_config():
    auth_config = {'bearer_token': 'Bearer 550e8400-e29b-41d4-a716-446655440000'}
    validator = ConfigValidator(auth_config, auth_rules)
    validator.validate()

def test_missing_auth_key():
    auth_config = {}
    validator = ConfigValidator(auth_config, auth_rules)
    
    with pytest.raises(ValueError, match="Missing required config key"):
        validator.validate()
