import pytest
from api import YaUploader

@pytest.fixture(scope="function")
def clear():
    """Fixture"""
    yield
    data_from_yd = YaUploader()
    data_from_yd.delete_folder('test_folder')
