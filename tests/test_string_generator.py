import string

import pytest

from app.string_generator import StringGenerator


@pytest.mark.parametrize(
    "length,symbols", [
        [5, 'a'],
        [5, 'ab'],
        [10, string.ascii_letters],
        [10, string.ascii_letters + string.digits],
        [32, 'abc']
    ]
)
def test_generate_string(length: int, symbols: str):
    generator = StringGenerator(length, symbols)
    random_string = generator.generate_string()
    assert len(random_string) == length
    assert set(symbols).issuperset(set(random_string))


@pytest.mark.parametrize('count', [10000])
@pytest.mark.parametrize('length', [5, 10, 15, 20, 100])
@pytest.mark.parametrize('symbols', ['a', 'abc', string.ascii_letters])
def test_stress_generation(length, symbols, count):
    generator = StringGenerator(length, symbols)
    for _ in range(count):
        random_string = generator.generate_string()
        assert len(random_string) == length
        assert set(symbols).issuperset(set(random_string))
