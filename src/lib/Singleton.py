class Singleton(type):
    """
    Example
        def class Config(metaclass=Singleton):
            pass
    """
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance