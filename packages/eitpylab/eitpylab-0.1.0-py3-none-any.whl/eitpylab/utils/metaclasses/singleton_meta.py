from threading import Lock, Thread


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.

    Attributes:
        _instances (dict): A dictionary to store the instances of the Singleton classes.
        _lock (Lock): A lock object used to synchronize threads during first access to the Singleton.

    Methods:
        __call__(*args, **kwargs) -> object:
            Creates and returns the Singleton instance, ensuring thread safety.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            object: The Singleton instance.
        """
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
