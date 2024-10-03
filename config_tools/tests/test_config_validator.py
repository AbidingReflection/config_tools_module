import pytest
from modules.config.config_validator import ConfigValidator

def test_valid_config():
    config = {
        "qTest_domain": "https://example.com/",
        "authentication_path": "auth/non-prd.yaml",
        "timeout": 60,
        "retry_attempts": 3,
        "max_concurrent_requests": 5
    }
    rules = {
        'qTest_domain': {'required': True, 'validator': ConfigValidator.validate_https_url},
        'timeout': {'required': True, 'validator': lambda key, value: ConfigValidator.validate_int_range(key, value, 1, 60)},
        'retry_attempts': {'required': True, 'validator': lambda key, value: ConfigValidator.validate_int_range(key, value, 0)}
    }
    validator = ConfigValidator(config, rules)
    validator.validate()

def test_missing_required_key():
    config = {
        'timeout': 30,
        'authentication_path': r'auth\prd_auth.yaml'
    }
    rules = {
        'api_url': {'required': True, 'validator': ConfigValidator.validate_https_url},
    }
    validator = ConfigValidator(config, rules)
    
    with pytest.raises(ValueError, match="Missing required config key: 'api_url'"):
        validator.validate()

def test_invalid_value():
    config = {
        'api_url': 'http://example.com/',  # Invalid URL (should be HTTPS)
    }
    rules = {
        'api_url': {'required': True, 'validator': ConfigValidator.validate_https_url},
    }
    validator = ConfigValidator(config, rules)
    
    with pytest.raises(ValueError, match="must start with 'HTTPS://'"):
        validator.validate()
