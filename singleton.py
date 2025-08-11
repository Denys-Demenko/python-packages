import threading


class SingletonMeta(type):
    _instances = {}
    _locks = {}

    def __call__(cls, *args, **kwargs):
        inst = cls._instances.get(cls)
        if inst is not None:
            return inst
        lock = cls._locks.setdefault(cls, threading.Lock())
        with lock:
            inst = cls._instances.get(cls)
            if inst is not None:
                return inst
            obj = object.__new__(cls)
            cls._instances[cls] = obj
            super(cls, obj).__init__(*args, **kwargs)
            return obj
