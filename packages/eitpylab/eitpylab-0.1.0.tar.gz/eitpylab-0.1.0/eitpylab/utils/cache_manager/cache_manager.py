class CacheManager:
    """
    A class for managing a simple cache store.

    This class provides functionality to set and retrieve key-value pairs in a cache store.

    Attributes:
        _instance (CacheManager): An instance of the CacheManager class (singleton pattern).
        _cache_store (list): A list to store key-value pairs as tuples.
    """

    _instance = None
    _cache_store = []

    def __init__(self):
        """
        Raises:
            RuntimeError: This class follows the singleton pattern, so direct instantiation is not allowed.
                Use get_instance() instead.
        """
        raise RuntimeError("Call get_instance() instead")

    @classmethod
    def get_instance(cls):
        """
        Get an instance of the CacheManager class.

        Returns:
            CacheManager: An instance of the CacheManager class.

        Notes:
            This method implements the singleton pattern, ensuring that only one instance of the
            CacheManager class is created and reused throughout the application.
        """
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def set(self, key, value):
        """
        Set a key-value pair in the cache store.

        Args:
            key: The key to set.
            value: The value corresponding to the key.

        Returns:
            None

        Notes:
            If the key already exists in the cache store, the previous value associated with
            the key will be overwritten with the new value.
        """
        self._cache_store.append((key, value))

    def get(self, key):
        """
        Retrieve the value associated with a given key from the cache store.

        Args:
            key: The key to retrieve.

        Returns:
            object: The value associated with the key, or None if the key is not found.

        Notes:
            If multiple values are associated with the same key, this method returns the last
            value encountered while iterating through the cache store.
        """
        value = None
        for item in self._cache_store:
            if key in item:
                value = item[1]
        return value
