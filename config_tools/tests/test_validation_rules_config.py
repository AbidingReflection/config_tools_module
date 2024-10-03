import pytest
from modules.config.validation_rules_config import config_rules
from modules.config.config_validator import ConfigValidator

def test_valid_config():
    config = {
        "qTest_domain": "https://example.com/",
        "authentication_path": "auth/non-prd.yaml",
        "timeout": 60,
        "retry_attempts": 3,
        "max_concurrent_requests": 3
        }
    validator = ConfigValidator(config, config_rules)
    validator.validate()

def test_invalid_config():
    # config = {'qTest_domain': 'http://example.com/'}
    config = {
        "qTest_domain": "http://example.com/",
        "authentication_path": "auth/non-prd.yaml",
        "timeout": 60,
        "retry_attempts": 3,
        "max_concurrent_requests": 5
    }
    validator = ConfigValidator(config, config_rules)
    
    with pytest.raises(ValueError, match="must start with 'HTTPS://'"):
        validator.validate()
