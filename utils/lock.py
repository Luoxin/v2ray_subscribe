# 写锁
import threading
from contextlib import contextmanager
import threading
from contextlib import contextmanager

# Thread-local state to stored information on locks already acquired
_local = threading.local()


def Wlock():
    return threading.Lock()


@contextmanager
def acquire(*locks):
    # Sort locks by object identifier
    locks = sorted(locks, key=lambda x: id(x))

    # Make sure lock order of previously acquired locks is not violated
    acquired = getattr(_local, "acquired", [])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError("Lock Order Violation")

    # Acquire all of the locks
    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        # Release locks in reverse order of acquisition
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks) :]


class Rwlock(object):
    def __init__(self):
        self._lock = threading.Lock()
        self._extra = threading.Lock()
        self.read_num = 0

    def read_acquire(self):
        with self._extra:
            self.read_num += 1
            if self.read_num == 1:
                self._lock.acquire()

    def read_release(self):
        with self._extra:
            self.read_num -= 1
            if self.read_num == 0:
                self._lock.release()

    def write_acquire(self):
        self._lock.acquire()

    def write_release(self):
        self._lock.release()


@contextmanager
def acquire_read(lock: Rwlock):
    try:
        lock.read_acquire()
        yield
    finally:
        lock.read_release()


@contextmanager
def acquire_write(lock: Rwlock):
    try:
        lock.write_acquire()
        yield
    finally:
        lock.write_release()


if __name__ == "__main__":
    lock = Wlock()

    with acquire(lock):
        print("write")

    with acquire(lock):
        print("write")

    # lock = Rwlock()
    #
    # with acquire_read(lock):
    #     print("read")
    #
    # with acquire_write(lock):
    #     print("write")
