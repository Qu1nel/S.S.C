import itertools
import signal
import time


def handler(time, signum) -> None:  # type: ignore
    """Some func."""
    print(f"\nHa-hAaa \\_@-@-\\| {time = } {signum = }")


signal.signal(signal.SIGINT, handler)

for i in itertools.count(1):
    print(f"{i}", end="\r")
    time.sleep(0.1)
