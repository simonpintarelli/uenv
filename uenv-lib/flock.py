import fcntl
import time

import terminal

class Lock():
    READ = 1
    WRITE = 2
    def __init__(self, path: str, type: int):
        self._lockfile = f"{path}.lock"

        # open the file
        self._lock = open(self._lockfile, "a")

        self._time = time.time()

        # acquire lock
        self._type = type
        if self._type==Lock.READ:
            # acquire shared lock
            fcntl.flock(self._lock, fcntl.LOCK_SH)
        else:
            # acquire exclusive lock
            fcntl.flock(self._lock, fcntl.LOCK_EX)

        terminal.info(f"aquired lock {self._lockfile} at {self._time}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        fcntl.flock(self._lock, fcntl.LOCK_UN)  # Release the lock
        self._lock.close()
        endtime = time.time()
        terminal.info(f"released lock {self._lockfile} at {endtime}, held for {(endtime - self._time)*1000:.2f} ms")

