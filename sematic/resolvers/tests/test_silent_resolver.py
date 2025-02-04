# Sematic
from sematic.abstract_future import FutureState
from sematic.calculator import func
from sematic.resolvers.silent_resolver import SilentResolver
from sematic.retry_settings import RetrySettings


@func
def add(a: float, b: float) -> float:
    return a + b


@func
def add3(a: float, b: float, c: float) -> float:
    return add(add(a, b), c)


@func
def pipeline(a: float, b: float) -> float:
    c = add(a, b)
    d = add3(a, b, c)
    return add(c, d)


def test_silent_resolver():
    assert SilentResolver().resolve(pipeline(3, 5)) == 24


_tried = 0


class SomeException(Exception):
    pass


@func(retry=RetrySettings(exceptions=(SomeException,), retries=3))
def retry_three_times():
    global _tried
    _tried += 1
    raise SomeException()


def test_retry():
    future = retry_three_times()
    try:
        SilentResolver().resolve(future)
    except SomeException:
        pass
    else:
        assert False

    assert future.props.retry_settings.retry_count == 3
    assert future.state == FutureState.FAILED
    assert _tried == 4
