from .config_validator import ConfigValidator

auth_rules  = {
    'bearer_token': {
        'required': True,
        'validator': ConfigValidator.validate_qTest_bearer_token
    }
}
