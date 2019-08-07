import time
import random
import string

from utils import DescriptorOwner, ObservableField

__all__ = [
    'StringGenerator',
]


class StringGenerator:
    __SYMBOLS = string.ascii_letters + string.digits

    data = ObservableField()

    def __init__(self):
        data = None

    def register(self, observer):
        StringGenerator.data.register(self, observer)

    def delete_observer(self, observer):
        StringGenerator.data.delete_observer(self, observer)

    @staticmethod
    def update_string(updating_string, length, interval):
        while True:
            updating_string.data = StringGenerator.__generate_string(length)
            time.sleep(interval)

    @staticmethod
    def __generate_string(length):
        return ''.join(random.choices(StringGenerator.__SYMBOLS, k=length))
