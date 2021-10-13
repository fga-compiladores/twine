import pytest
import sys
import pathlib

TEST_PATH = pathlib.Path(__file__).parent
PROJECT_PATH = TEST_PATH.parent
SRC_PATH = PROJECT_PATH / "twine"

sys.path.append(".")
sys.path.append(str(PROJECT_PATH))


@pytest.fixture(scope="session")
def twine():
    import twine

    return twine
