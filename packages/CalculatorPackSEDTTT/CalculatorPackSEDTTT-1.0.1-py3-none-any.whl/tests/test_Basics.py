import pytest
from calc import add, subtract, multiply, divide, mod, stringParse, log, exp, abs, factorial, mean, median, mode, randomnumsrange, cubesurfacearea


def test_add():
    assert add(10, 5) == 15
    assert add(-1, 1) == 0
    assert add(-1, -1) == -2
    assert add(-2389, 29348) == 26959
    assert add(21987219, 8472134) == 30459353

def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(-1, 1) == -2
    assert subtract(-1, -1) == 0
    assert subtract(-2389, 29348) == -31737
    assert subtract(21987219, 8472134) == 13515085

def test_multiply():
    assert multiply(10, 5) == 50
    assert multiply(-1, 1) == -1
    assert multiply(-1, -1) == 1

def test_divide():
    assert divide(10, 5) == 2
    assert divide(-1, 1) == -1
    assert divide(-1, -1) == 1
    with pytest.raises(ValueError):
        divide(10, 0)

def test_mod():
    assert mod(10, 3) == 1, "C: 1"
    assert mod(10, 10) == 0, "C: 0"
    assert mod(0, 10) == 0, "C: 0"
    assert mod(-10, 3) == 2, "C: 2"
    with pytest.raises(ValueError):
        mod(10, 0), "Should raise ValueError for division by zero"

def test_stringParse_addition():
    assert stringParse("10 + 5") == 15, "C: 15"
    assert stringParse("39 + 27") == 66, "C: 66"    # Bible reference

def test_stringParse_subtraction():
    assert stringParse("10 - 5") == 5, "C: 5"
    assert stringParse("66 - 39") == 27, "C: 27"

def test_stringParse_multiplication():
    assert stringParse("10 * 5") == 50, "C: 50"
    assert stringParse("3 * 9") == 27, "C: 27"

def test_stringParse_division():
    assert stringParse("10 / 2") == 5, "C: 5"
    assert stringParse("39 / 3") == 13, "C: 13"
    with pytest.raises(ValueError):
        stringParse("10 / 0"), "C: raise ValueError for division by zero"

def test_stringParse_mod():
    assert stringParse("10 mod 3") == 1, "C: 1"
    assert stringParse("39 mod 27") == 12, "C: 12"
    with pytest.raises(ValueError):
        stringParse("10 mod 0"), "C: raise ValueError for mod by zero"

def test_stringParse_invalid_input():
    with pytest.raises(ValueError):
        stringParse("10"), "C: raise ValueError for invalid input format"
    with pytest.raises(ValueError):
        stringParse("10 ^ 2"), "C: raise ValueError for unsupported operation"
    with pytest.raises(ValueError):
        stringParse("one + two"), "C: raise ValueError for non-numeric input"

def test_log():
    assert log(10, 10) == 1
    assert log(100, 10) == 2
    assert log(1000, 10) == 3
    assert log(64, 2) == 6
    with pytest.raises(ValueError):
        log(-1,10), "Should raise ValueError"

def test_exp():
    assert exp(2, 3) == 8
    assert exp(1, 10) == 1
    assert exp(4, -1) == 0.25 

def test_stringParse_exp():
    assert stringParse("7 exp 3") == 343
    assert stringParse("4 exp 0") == 1
    assert stringParse("-4 exp 0") == -1
    assert stringParse("0 exp 0") == 1
    assert stringParse("-5 exp -3") == -0.008000000000000002
    

def test_abs():
    assert abs(0) == 0
    assert abs(-2) == 2
    assert abs(3) == 3

def test_factorial():
    assert factorial(0) == 1
    assert factorial(3) == 6
    assert factorial(10) == 3628800
    with pytest.raises(ValueError):
        factorial(-4), "Should raise ValueError"

def test_stringParse_log():
    assert stringParse("10 log 10") == 1, "C: 1"
    assert stringParse("64 log 2") == 6, "C: 6"
    with pytest.raises(ValueError):
        stringParse("-1 mod 10"), "C: raise ValueError"

def test_stringParse_log():
    assert stringParse("2 exp 3") == 8, "C: 8"
    assert stringParse("1 exp 10") == 1, "C: 1"
    assert stringParse("4 exp -1") == 0.25, "C: 0.25"

def test_mean():
    assert mean([1, 2, 3, 4, 5]) == 3
    assert mean([0, 10, 20, 30]) == 15
    assert mean([-1, 1]) == 0
    assert mean([1]) == 1

def test_median():
    assert median([1, 3, 2]) == 2
    assert median([1, 2, 3, 4]) == 2.5
    assert median([7, 8, 3, 1]) == 5
    assert median([-2, -1, -3]) == -2
    assert median([1]) == 1

def test_mode():
    assert mode([1, 2, 2, 3, 4]) == [2]
    assert mode([1, 1, 2, 3, 3]) == [1, 3]  
    assert mode([1, 2, 3, 4, 5]) == "No mode"  
    assert mode([7, 7, 7]) == [7]  
    assert mode([1]) == [1]  

def test_randomnumsrange():
    with pytest.raises(ValueError):
        stringParse("-6 randomnumsrange -8"), "C: raise ValueError"
    with pytest.raises(ValueError):
        stringParse("-40 randomnumsrange 7"), "C: raise ValueError"
    with pytest.raises(ValueError):
        stringParse("2 randomnumsrange -30"), "C: raise ValueError"

def test_randomnumsrange_stringParse():
    assert stringParse("0 randomnumsrange 0") == []
    assert stringParse("0 randomnumsrange 1") == [0]
    assert stringParse("1 randomnumsrange 0") == []

def test_cubesurfacearea():
    assert cubesurfacearea(2) == 24
    with pytest.raises(ValueError):
        stringParse("-5"), "C: raise ValueError"
    with pytest.raises(ValueError):
        stringParse("0"), "C: raise ValueError"

