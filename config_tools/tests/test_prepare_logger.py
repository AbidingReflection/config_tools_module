import pytest
import os
from modules.config.prepare_logger import prepare_logger

@pytest.fixture
def temp_log_dir(tmp_path):
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    return log_dir

def test_logger_creation(temp_log_dir):
    # Test that the logger is created and logs are written to the correct location
    logger = prepare_logger(str(temp_log_dir))
    assert logger is not None

    log_file = next(temp_log_dir.glob("*.log"))
    assert log_file.exists()
