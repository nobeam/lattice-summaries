from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def test_output_dir():
    test_dir = Path(__file__).parent / "tests"
    test_output_dir = test_dir / "results"
    test_output_dir.mkdir(exist_ok=True)
    return test_output_dir


@pytest.fixture(scope="session")
def test_lattice():
    # TODO: add test lattice
    raise Exception("test is currently broken!")
    return {
        "simulation": ...,
        "energy": ...,
    }
