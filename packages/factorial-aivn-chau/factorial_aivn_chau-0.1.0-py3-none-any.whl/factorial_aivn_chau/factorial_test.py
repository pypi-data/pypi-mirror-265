import pytest
from factorial_aivn_chau.factorial import fact

def test_factorial_of_0() :
    assert fact(0) == 1
def test_factorial_of_1() :
    assert fact(1) == 1
def test_factorial_of_5() :
    assert fact(5) == 120
def test_factorial_of_10() :
    assert fact(10) == 3628800
def test_factorial_of_negative_number() :
    with pytest.raises(ValueError) :
        fact(-5)

if __name__ == " __main__ ":
    pytest.main()
