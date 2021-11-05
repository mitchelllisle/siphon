from siphon import AioQueue, queuecollect, CollectedError
from functools import partial
import pytest

ahundredints = partial(range, 100)


def test_queue_plus():
    q = AioQueue()
    [q.put_nowait(i) for i in ahundredints()]
    assert q.collect() == [i for i in ahundredints()]


def test_iter():
    q = AioQueue()
    [q.put_nowait(i) for i in ahundredints()]

    o = []
    for i in q:
        o.append(i)
    assert o == [i for i in ahundredints()]


@pytest.mark.asyncio
async def test_aiter():
    q = AioQueue()
    [q.put_nowait(i) for i in ahundredints()]

    o = []
    async for i in q:
        o.append(i)
    assert o == [i for i in ahundredints()]


@pytest.mark.asyncio
async def test_queuecollect_errs():
    eq = AioQueue()

    @queuecollect(errors=eq)
    def raiseerr(i: int, err=Exception):
        raise err(f"error with {i}")

    [await raiseerr(i) for i in ahundredints()]
    assert eq.qsize() == 100
    assert all([isinstance(x, CollectedError) for x in eq.collect()])


@pytest.mark.asyncio
async def test_queuecollect_collectederror():
    eq = AioQueue()

    @queuecollect(errors=eq)
    def raiseerr(i: int, **kwargs):
        raise Exception(f"error with {i}")

    await raiseerr(1, test=2)
    err = eq.get_nowait()
    assert err.error_name == "Exception"
    assert err.func_name == "raiseerr"
    assert err.args == (1, )
    assert err.kwargs == {"test": 2}
    assert err.func.__name__ == "raiseerr"


@pytest.mark.asyncio
async def test_queuecollect_collectederror_reraise():
    eq = AioQueue()

    @queuecollect(errors=eq)
    def raiseerr(i: int, **kwargs):
        raise Exception(f"error with {i}")

    await raiseerr(1, test=2)
    with pytest.raises(Exception):
        err = await eq.get()
        err.reraise


@pytest.mark.asyncio
async def test_queuecollect_success():
    eq = AioQueue()

    @queuecollect(errors=eq)
    def raiseerr(i: int):
        return i

    o = [await raiseerr(i) for i in ahundredints()]
    assert len(o) == 100
    assert all([isinstance(x, int) for x in o])


@pytest.mark.asyncio
async def test_queuecollect_successqueue():
    eq = AioQueue()
    sq = AioQueue()

    @queuecollect(errors=eq, success=sq)
    def raiseerr(i: int):
        return i

    [await raiseerr(i) for i in ahundredints()]
    assert sq.qsize() == 100
    assert all([isinstance(x, int) for x in sq])
