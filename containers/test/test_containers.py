import pytest
from ..containers import app


def test_container():
    with app.test_client() as client:
        assert False
