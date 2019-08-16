import dataclasses
import random

__all__ = [
    'StringGenerator',
]


@dataclasses.dataclass
class StringGenerator:
    length: int
    symbols: str

    def generate_string(self) -> str:
        return ''.join(random.choices(self.symbols, k=self.length))
