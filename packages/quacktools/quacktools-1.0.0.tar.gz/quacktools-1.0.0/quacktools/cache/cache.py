"""This module defines the caching logic which allows for fast test sample data retrieval.
"""

from typing import List, Dict

import os
import json
import appdirs

from quacktools.constants.extension_constants import APPLICATION_NAME, CACHE_FILE_NAME


class Cache:
    """The Cache instance is a singleton instance, which allows for fast retrieval of test samples
    by using a caching mechanism.

    Attributes:
        cache (Dict): The cache and its data.
        cache_directory (str): The cache directory.
        cache_file_path (str): The cache file path.
    """

    def __init__(self) -> None:
        """Initializes the cache instance."""

        self.cache_directory = ""
        self.cache_file_path = ""

        self.create_cache_directory()

        self.cache = self.get_cache()

    def create_cache_directory(self) -> None:
        """Create a cache directory in the user's home directory. If the directory does not
        exist, then create one.
        """

        self.cache_directory = appdirs.user_cache_dir(APPLICATION_NAME)
        self.cache_file_path = self.cache_directory + CACHE_FILE_NAME

        os.makedirs(self.cache_directory, exist_ok=True)

        if not os.path.exists(self.cache_file_path):
            with open(self.cache_file_path, "w", encoding="utf-8") as cache_file:
                json.dump({}, cache_file, indent=4)

    def check_samples_cached(self, cache_key) -> bool:
        """Check if the samples have already been cached.

        Args:
            cache_key (str): The cache key is required to fetch cache data.

        Returns:
            bool: Boolean value based on whether samples already exist in cache.
        """

        return cache_key in self.cache

    def set_samples(self, cache_key: str, cache_data: Dict[str, List[str]]) -> None:
        """Cache the input cache data for the given cache key.

        Args:
            cache_key (str): The cache key is required to fetch cache data.
            cache_data (Dict[str, List[str]]): The cache data.
        """

        self.cache[cache_key] = cache_data

        with open(self.cache_file_path, "w", encoding="utf-8") as cache_file:
            json.dump(self.cache, cache_file, indent=4)

    def get_cache(self) -> Dict[str, List[str]]:
        """Return the cache and its data.

        Returns:
            Dict[str, List[str]]: The cache, and its data.
        """

        with open(self.cache_file_path, "r", encoding="utf-8") as cache_file:
            return json.load(cache_file)

    def get_samples(self, cache_key: str) -> Dict[str, List[str]]:
        """Returns a list of cached sample data. This is faster than getting samples from URL each time.

        Args:
            cache_key (str): The cache key is required to fetch cache data.

        Returns:
            Dict[str, List[str]]: The sample's I/O data.
        """

        return self.cache[cache_key]
