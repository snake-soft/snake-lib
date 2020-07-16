import datetime
import time
from _thread import RLock
from functools import update_wrapper, _make_key, _CacheInfo

# Check the example at the end of this script.


class Node:
    """node of the circular doubly linked list"""

    def __init__(self, prev=None, next_=None, key=None, result=None, cache_time=None):
        self.prev = prev
        self.next = next_
        self.key = key
        self.result = result
        self.cache_time = cache_time


def lru_cache(maxsize=128, typed=False, **timedelta_kwargs):
    if maxsize is not None and not isinstance(maxsize, int):
        raise TypeError('Expected maxsize to be an integer or None')
    timedelta = datetime.timedelta(**timedelta_kwargs) if timedelta_kwargs else None

    def decorating_function(user_function):
        wrapper = _lru_cache_wrapper(user_function, maxsize, typed, timedelta, _CacheInfo)
        return update_wrapper(wrapper, user_function)

    return decorating_function


def _lru_cache_wrapper(user_function, maxsize, typed, timedelta, _CacheInfo):
    sentinel = object()  # unique object used to signal cache misses
    make_key = _make_key  # build a key from the function arguments

    cache = {}
    hits = misses = 0
    full = False
    cache_get = cache.get  # bound method to lookup a key or return None
    cache_len = cache.__len__  # get cache size without calling len()
    lock = RLock()  # because linked list updates aren't thread-safe
    root = Node()  # root of the circular doubly linked list
    root.prev = root.next = root  # initialize the linked list

    if maxsize == 0:
        def wrapper(*args, **kwargs):
            nonlocal misses
            result = user_function(*args, **kwargs)
            misses += 1
            return result

    elif maxsize is None:
        def wrapper(*args, **kwargs):
            nonlocal hits, misses
            key = make_key(args, kwargs, typed)
            value = cache_get(key, sentinel)
            if value is not sentinel:
                if timedelta is not None:
                    result, cache_time = value
                    if datetime.datetime.now() - cache_time < timedelta:
                        hits += 1
                        return result
                    else:
                        del cache[key]
                else:
                    hits += 1
                    return value
            result = user_function(*args, **kwargs)
            if timedelta is not None:
                cache[key] = result, datetime.datetime.now()
            else:
                cache[key] = result
            misses += 1
            return result

    else:
        def wrapper(*args, **kwargs):
            nonlocal root, hits, misses, full
            key = make_key(args, kwargs, typed)
            with lock:
                node = cache_get(key)
                if node is not None:
                    if timedelta is not None and datetime.datetime.now() - node.cache_time >= timedelta:
                        # cache expired, remove the node from linked list and cache
                        node_prev, node_next = node.prev, node.next
                        node_prev.next = node_next
                        node_next.prev = node_prev
                        del cache[node.key]
                        full = cache_len() >= maxsize
                    else:
                        # The expiration feature is not enabled or the cache is not expired
                        node_prev, node_next = node.prev, node.next
                        node_prev.next = node_next
                        node_next.prev = node_prev

                        last_node = root.prev
                        node.prev = last_node
                        node.next = root
                        last_node.next = root.prev = node
                        hits += 1
                        return node.result

            result = user_function(*args, **kwargs)
            with lock:
                if key in cache:
                    # TODO not sure if expiration should be handled here
                    # Getting here means that this same key was added to the
                    # cache while the lock was released.  Since the link
                    # update is already done, we need only return the
                    # computed result and update the count of misses.
                    pass
                elif full:
                    old_root: Node = root
                    old_root.result = result
                    old_root.key = key
                    old_root.cache_time = datetime.datetime.now()
                    cache[key] = old_root

                    root = old_root.next
                    del cache[root.key]
                    root.key = root.result = root.cache_time = None
                else:
                    last_node: Node = root.prev
                    new_node = Node(last_node, root, key, result, datetime.datetime.now())
                    last_node.next = root.prev = cache[key] = new_node
                    full = cache_len() >= maxsize
                misses += 1
            return result

    def cache_info():
        """Report cache statistics"""
        with lock:
            return _CacheInfo(hits, misses, maxsize, cache_len())

    def cache_clear():
        """Clear the cache and cache statistics"""
        nonlocal hits, misses, full
        with lock:
            cache.clear()
            root.prev = root.next = root
            root.key = root.result = None
            hits = misses = 0
            full = False

    wrapper.cache_info = cache_info
    wrapper.cache_clear = cache_clear
    return wrapper


if __name__ == '__main__':
    @lru_cache(seconds=3)
    def foo(arg):
        print('function executed, got arg: {}'.format(arg))
        return arg

    foo('a')
    print('sleeping for 2 seconds...')
    time.sleep(2)

    foo('b')
    print('sleeping for another 2 seconds...')
    time.sleep(2)

    foo('a')                                                                    # "a" expired
    print('function returned value {} directly from cache'.format(foo('b')))    # "b" not expired yet