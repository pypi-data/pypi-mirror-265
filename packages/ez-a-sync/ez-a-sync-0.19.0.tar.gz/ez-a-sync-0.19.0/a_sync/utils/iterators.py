
import asyncio
import asyncio.futures
import logging

from a_sync._typing import *
from a_sync.primitives.queue import Queue

logger = logging.getLogger(__name__)

async def exhaust_iterator(iterator: AsyncIterator[T], *, queue: Optional[asyncio.Queue] = None) -> None:
    async for thing in iterator:
        if queue:
            logger.debug('putting %s from %s to queue %s', thing, iterator, queue)
            queue.put_nowait(thing)
        
async def exhaust_iterators(iterators, *, queue: Optional[asyncio.Queue] = None) -> None:
    await asyncio.gather(*[exhaust_iterator(iterator, queue=queue) for iterator in iterators]) 
    if queue:
        queue.put_nowait(_Done())
    
T0 = TypeVar('T0')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')
T6 = TypeVar('T6')
T7 = TypeVar('T7')
T8 = TypeVar('T8')
T9 = TypeVar('T9')

@overload
def as_yielded(*iterators: AsyncIterator[T]) -> AsyncIterator[T]:...
@overload
def as_yielded(iterator0: AsyncIterator[T0], iterator1: AsyncIterator[T1], iterator2: AsyncIterator[T2], iterator3: AsyncIterator[T3], iterator4: AsyncIterator[T4], iterator5: AsyncIterator[T5], iterator6: AsyncIterator[T6], iterator7: AsyncIterator[T7], iterator8: AsyncIterator[T8], iterator9: AsyncIterator[T9]) -> AsyncIterator[Union[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9]]:...
@overload
def as_yielded(iterator0: AsyncIterator[T0], iterator1: AsyncIterator[T1], iterator2: AsyncIterator[T2], iterator3: AsyncIterator[T3], iterator4: AsyncIterator[T4], iterator5: AsyncIterator[T5], iterator6: AsyncIterator[T6], iterator7: AsyncIterator[T7], iterator8: AsyncIterator[T8]) -> AsyncIterator[Union[T0, T1, T2, T3, T4, T5, T6, T7, T8]]:...
@overload
def as_yielded(iterator0: AsyncIterator[T0], iterator1: AsyncIterator[T1], iterator2: AsyncIterator[T2], iterator3: AsyncIterator[T3], iterator4: AsyncIterator[T4], iterator5: AsyncIterator[T5], iterator6: AsyncIterator[T6], iterator7: AsyncIterator[T7]) -> AsyncIterator[Union[T0, T1, T2, T3, T4, T5, T6, T7]]:...
@overload
def as_yielded(iterator0: AsyncIterator[T0], iterator1: AsyncIterator[T1], iterator2: AsyncIterator[T2], iterator3: AsyncIterator[T3], iterator4: AsyncIterator[T4], iterator5: AsyncIterator[T5], iterator6: AsyncIterator[T6]) -> AsyncIterator[Union[T0, T1, T2, T3, T4, T5, T6]]:...
@overload
def as_yielded(iterator0: AsyncIterator[T0], iterator1: AsyncIterator[T1], iterator2: AsyncIterator[T2], iterator3: AsyncIterator[T3], iterator4: AsyncIterator[T4], iterator5: AsyncIterator[T5]) -> AsyncIterator[Union[T0, T1, T2, T3, T4, T5]]:...
@overload
def as_yielded(iterator0: AsyncIterator[T0], iterator1: AsyncIterator[T1], iterator2: AsyncIterator[T2], iterator3: AsyncIterator[T3], iterator4: AsyncIterator[T4]) -> AsyncIterator[Union[T0, T1, T2, T3, T4]]:...
@overload
def as_yielded(iterator0: AsyncIterator[T0], iterator1: AsyncIterator[T1], iterator2: AsyncIterator[T2], iterator3: AsyncIterator[T3]) -> AsyncIterator[Union[T0, T1, T2, T3]]:...
@overload
def as_yielded(iterator0: AsyncIterator[T0], iterator1: AsyncIterator[T1], iterator2: AsyncIterator[T2]) -> AsyncIterator[Union[T0, T1, T2]]:...
@overload
def as_yielded(iterator0: AsyncIterator[T0], iterator1: AsyncIterator[T1]) -> AsyncIterator[Union[T0, T1]]:...
@overload
def as_yielded(iterator0: AsyncIterator[T0], iterator1: AsyncIterator[T1], iterator2: AsyncIterator[T2], *iterators: AsyncIterator[T]) -> AsyncIterator[Union[T0, T1, T2, T]]:...
async def as_yielded(*iterators: AsyncIterator[T]) -> AsyncIterator[T]:  # type: ignore [misc]
    queue: Queue[T] = Queue()
    def get_ready() -> List[T]:
        try:
            return queue.get_all_nowait()
        except asyncio.QueueEmpty:
            return []
    task = asyncio.create_task(exhaust_iterators(iterators, queue=queue))
    def done_callback(t: asyncio.Task) -> None:
        if (e := t.exception()) and not next_fut.done(): 
            next_fut.set_exception(e)
    task.add_done_callback(done_callback)
    while not task.done():
        next_fut = asyncio.get_event_loop().create_future()
        get_task = asyncio.create_task(coro=queue.get(), name=str(queue))
        asyncio.futures._chain_future(get_task, next_fut)  # type: ignore [attr-defined]
        for item in (await next_fut, *get_ready()):
            if isinstance(item, _Done):
                task.cancel()
                return
            yield item
            
    if e := task.exception():
        get_task.cancel()
        raise e

class _Done:
    pass