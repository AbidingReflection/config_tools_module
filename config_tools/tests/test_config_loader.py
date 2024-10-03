import pytest
from modules.config.config_loader import ConfigLoader
from pathlib import Path
import os

@pytest.fixture
def valid_config_file(tmp_path):
    # Create a temporary YAML config file
    config_path = tmp_path / "test_config.yaml"
    config_content = """
    qTest_domain: "https://example.com/"
    authentication_path: "auth/non-prd.yaml"
    timeout: 60
    retry_attempts: 3
    max_concurrent_requests: 5
    """
    config_path.write_text(config_content)
    return config_path

def test_valid_config_loading(valid_config_file):
    # Test loading a valid config file
    loader = ConfigLoader(valid_config_file)
    assert loader.config is not None
    assert loader.config['qTest_domain'] == 'https://example.com/'
    assert loader.config['timeout'] == 60

def test_invalid_config_path():
    # Test loading an invalid config path
    with pytest.raises(FileNotFoundError):
        ConfigLoader(Path("non_existing_config.yaml"))

def test_invalid_yaml_content(tmp_path):
    # Create an invalid YAML file
    invalid_yaml = tmp_path / "invalid.yaml"
    invalid_yaml.write_text("this: is: not: valid")
    
    with pytest.raises(ValueError):
        ConfigLoader(invalid_yaml)
