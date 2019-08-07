class Observable:
    def register(self, *args, **kwargs):
        raise NotImplemented

    def delete_observer(self, *args, **kwargs):
        raise NotImplemented

    def notify_observers(self, *args, **kwargs):
        raise NotImplemented
