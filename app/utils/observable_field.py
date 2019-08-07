from utils.observable import Observable


class Descriptor:
    def __init__(self):
        self.label = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.label, None)

    def __set__(self, instance, value):
        instance.__dict__[self.label] = value


class ObservableField(Descriptor, Observable):
    @property
    def observers(self):
        return f"{self.label}_observers"

    def register(self, instance, observer):
        instance.__dict__.setdefault(self.observers, [])
        instance.__dict__[self.observers].append(observer)

    def delete_observer(self, instance, observer):
        observers = instance.__dict__.get(self.observers, [])
        observers.remove(observer)

    def notify_observers(self, instance):
        for observer in instance.__dict__.get(self.observers, []):
            observer.update(instance.__dict__.get(self.label, None))

    def __set__(self, instance, value):
        super().__set__(instance, value)
        self.notify_observers(instance)


class DescriptorOwner(type):
    def __new__(cls, name, bases, attrs):
        for name, attr in attrs.items():
            if isinstance(v, Descriptor):
                attr.label = name
        return super(DescriptorOwner, cls).__new__(cls, name, bases, attrs)
