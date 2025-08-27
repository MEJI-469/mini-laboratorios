from labs.lab3.src.operaciones import suma, division
import pytest


def test_suma():
    assert suma(2, 3) == 5.0


def test_division_ok():
    assert division(10, 2) == 5.0


def test_division_cero():
    with pytest.raises(ValueError):
        division(1, 0)
