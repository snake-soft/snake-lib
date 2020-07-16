""" This library is a collection of tools to use for development """
from .timer import timer
from .cache import lru_cache
from .cache import lru_cache as cache


__all__ = [
    'timer',
    'lru_cache',
    'cache',
    ]

if __name__ == '__main__':
    unittest.main()
