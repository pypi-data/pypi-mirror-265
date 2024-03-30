"""
Session Cache Implementation

Author: Ran (01-ERFA)
Date created: 29/03/2024
Last modified: 29/03/2024

This module contains the implementation of a session cache (SC) and cached data (CD).
"""

from datetime import datetime, timedelta
from time import sleep
from threading import Thread, Lock

class CachedData:
    """
    Represents cached data with an optional time-to-live (TTL).

    Attributes:
        value (Any): The value being cached.
        expire_time (datetime | None): The expiration time for the cached data.
            If None, the data does not expire.
    """
    def __init__(self, value, ttl : int | None) -> None:
        """
        Initialize CachedData with the provided value and TTL.

        Args:
            value (Any): The value to be cached.
            ttl (int | None): The time-to-live (TTL) for the cached data in seconds.
                If None or <= 0, the data does not expire.
        """
        self.value = value
        self.expire_time = datetime.now() + timedelta(seconds=ttl) if isinstance(ttl, int) and ttl > 0 else None

    def __repr__(self) -> str:
        """
        Return a string representation of the CachedData instance.

        Returns:
            str: A string representation containing information about the CachedData instance,
                including the expiration time and the cached value.
        """
        return f"CachedData(expire_time: {repr(self.expire_time)}, value: {repr(self.value)})"

class SessionCache:
    """
    Represents a session cache for storing and managing cached data.

    Attributes:
        __cache (dict): The internal dictionary to store cached data.
        __default_ttl (int): The default time-to-live (TTL) for cached data in seconds.
        __cleanup_enabled (bool): Flag indicating whether automatic cleanup is enabled.
        __cleanup_config (int): The interval in seconds for automatic cache cleanup.
        __thread_cleanup (Thread | None): The thread for running automatic cache cleanup.
        __safe_use (Lock): Thread lock for ensuring thread-safe access to cache data.

    Properties:
        length (int): Returns the number of items in the cache.
        cleaning_enabled (bool): Indicates whether automatic cleanup is enabled.
        cleanup_config (int | None): Returns the interval for automatic cache cleanup.
        default_ttl (int | None): Get the default time-to-live (TTL) for cached data in seconds, or None.

    Methods:
        start_cleanup(): Start automatic cache cleanup if not already running.
        stop_cleanup(): Stop automatic cache cleanup if running.
        clear_expired(): Clear expired items from the cache.
        get(key: Any) -> CachedData | None: Retrieve cached data associated with the given key.
        update(key: Any, value: Any, ttl: int | None = 0) -> None: Update the cache with the provided key-value pair.
        get_or_add(key: Any, value: Any = None, ttl: int | None = 0) -> CachedData: Retrieve cached data associated with the given key, or add it if not found.
        reset(): Reset the cache by removing all items.
        
        __repr__(): Return a string representation of the SessionCache instance.
        __len__(): Return the number of items in the cache.
        __start_cleanup(): Start the automatic cache cleanup thread.
    """

    def __init__(self, default_ttl : int = 3600, cleanup_config : int = 9000) -> None:
        """
        Initialize SessionCache with the provided default TTL and cleanup configuration.

        Args:
            default_ttl (int, optional): The default time-to-live (TTL) for cached data in seconds.
                Defaults to 3600 seconds (1 hour).
            cleanup_config (int, optional): The interval in seconds for automatic cache cleanup.
                If set to 0 or a negative value, automatic cleanup is disabled. Defaults to 9000 seconds (2.5 hours).
        """
        self.__cache           = {}
        self.__default_ttl     = default_ttl
        self.__cleanup_enabled = isinstance(cleanup_config, int) and cleanup_config > 0
        self.__cleanup_config  = cleanup_config if self.__cleanup_enabled else None
        self.__thread_cleanup  = None
        self.__safe_use        = Lock()

        if self.__cleanup_enabled: self.start_cleanup()

    def __repr__(self) -> str:
        """
        Return a string representation of the SessionCache instance.

        Returns:
            str: A string representation containing information about the SessionCache instance,
                including the number of items in the cache, the default TTL, whether automatic
                cleanup is enabled, the cleanup interval, and a list of cache keys.
        """
        return f"SessionCache(length: {len(self)}, default_ttl: {self.__default_ttl}, cleaning_enabled: {self.__cleanup_enabled}, cleanup_interval: {self.__cleanup_config}, cache_keys: {list(self.__cache.keys())})"

    def __len__(self):
        """Return the number of items in the cache."""
        return len(self.__cache)
    
    def __start_cleanup(self):
        """Start the automatic cache cleanup thread."""
        while self.__cleanup_enabled:
            self.clear_expired()
            sleep(self.__cleanup_config)

    @property
    def default_ttl(self):
        """
        Get the default time-to-live (TTL) for cached data in seconds.

        Returns:
            int | None: The default time-to-live (TTL) in seconds,
                or None if no default TTL is set.
        """
        return self.__default_ttl
    
    @default_ttl.setter
    def default_ttl(self, ttl : int | None):
        """
        Set the default time-to-live (TTL) for cached data in seconds.

        Args:
            ttl (int | None): The default time-to-live (TTL) in seconds to be set.
                If ttl < 0 or ttl is not an integer, the default TTL is None.
        """
        self.__default_ttl = ttl if isinstance(ttl, int) and ttl > 0 else None

    @property
    def length(self) -> int:
        """Return the number of items in the cache."""
        return len(self)

    @property
    def cleaning_enabled(self) -> bool:
        """
        Return whether automatic cache cleanup is enabled.

        Returns:
            bool: True if automatic cleanup is enabled, False otherwise.
        """
        return self.__cleanup_enabled
    
    @cleaning_enabled.setter
    def cleaning_enabled(self, enabled):
        """
        Set whether automatic cache cleanup is enabled.

        Args:
            enabled (bool): True to enable automatic cleanup, False to disable.
        """
        self.__cleanup_enabled = bool(enabled)
        if not self.__cleanup_enabled: self.stop_cleanup()
    
    @property
    def cleanup_config(self) -> int | None:
        """
        Return the interval for automatic cache cleanup.

        Returns:
            int | None: The interval for automatic cleanup in seconds,
                or None if automatic cleanup is disabled.
        """
        return self.__cleanup_config

    @cleanup_config.setter
    def cleanup_config(self, interval):
        """
        Set the interval for automatic cache cleanup.

        Args:
            interval (int): The interval for automatic cleanup in seconds.
                If set to 0 or a negative value, automatic cleanup is disabled.
        """
        self.__cleanup_config = interval if isinstance(interval, int) and interval > 0 else None
        if not isinstance(interval, int) and interval <= 0: self.stop_cleanup()

    def start_cleanup(self):
        """Start automatic cache cleanup if not already running."""
        if not self.__cleanup_enabled and isinstance(self.__cleanup_config, int) and self.__cleanup_config > 0: 
            self.__cleanup_enabled = True
            self.__thread_cleanup  = Thread(target=self.__start_cleanup, daemon=True)
            self.__thread_cleanup.start()
        
    def stop_cleanup(self):
        """Stop automatic cache cleanup if running."""
        self.__cleanup_enabled = False
        if self.__thread_cleanup is not None:
            self.__thread_cleanup.join()
            self.__thread_cleanup = None

    def clear_expired(self):
        """Clear expired items from the cache."""
        current_time = datetime.now()
        with self.__safe_use:
            self.__cache = {key: data for key, data in self.__cache.items() if data.expire_time is None or data.expire_time > current_time}
    
    def get(self, key):
        """
        Retrieve cached data associated with the given key.

        Args:
            key (Any): The key associated with the cached data.

        Returns:
            Any | None: The cached data value associated with the key,
                or None if the data is expired or not found.
        """
        with self.__safe_use:
            data : CachedData | None = self.__cache.get(key)
            if isinstance(data, CachedData) and (data.expire_time is None or data.expire_time > datetime.now()):
                return data.value
        return None
    
    def get_or_add(self, key, value = None, ttl : int | None = 0):
        """
        Retrieve cached data associated with the given key, or add it if not found.

        Args:
            key (Any): The key associated with the cached data.
            value (Any, optional): The value to be cached if the key is not found.
                Defaults to None.
            ttl (int | None, optional): The time-to-live (TTL) for the cached data in seconds.
                If None or <= 0, the default TTL is used. 

        Returns:
            Any: The cached data value associated with the key, either existing or newly added.
        """
        with self.__safe_use:
            if key not in self.__cache: self.__cache[key] = CachedData(value, ttl if ttl is None or (isinstance(ttl, int) and ttl > 0) else self.__default_ttl)
        return self.get(key)

    def update(self, key, value, ttl : int | None = 0):
        """
        Update the cache with the provided key-value pair.

        Args:
            key (Any): The key to associate with the cached value.
            value (Any): The value to be cached.
            ttl (int | None, optional): The time-to-live (TTL) for the cached data in seconds.
                If None or <= 0, the default TTL is used.
        """
        with self.__safe_use:
            self.__cache[key] = CachedData(value, ttl if ttl is None or (isinstance(ttl, int) and ttl > 0) else self.__default_ttl)

    def reset(self):
        """Reset the cache by removing all items."""
        with self.__safe_use: self.__cache = {}
