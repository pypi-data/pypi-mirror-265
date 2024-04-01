from typing import Protocol, Awaitable, AsyncIterable
import haskellian as hk
from haskellian import asynch as hka
from ..logprobs import logprob
from ...beam.succs import Logprob

class PredictFn(Protocol):
  """Batched predictions of plies `[from_ply, to_ply)` for all (1 or 2) players
  - Must return an array of shape `BATCH x PLAYERS x TOP_PREDS` of `(pred, logprob)` tuples
  """
  def __call__(self, from_ply: int, to_ply: int) -> Awaitable[list[list[list[tuple[str, int]]]]]:
    ...

async def batched_logprobs(predict: PredictFn, *, max_moves: int, start_ply: int = 0, batch_size: int = 8) -> AsyncIterable[list[Logprob]]:
  for i in range(start_ply, max_moves, batch_size):
    preds = await hka.wait(predict(i, i+batch_size))
    yield [logprob(ps) for ps in preds]

def prefetched_logprobs(predict: PredictFn, *, max_moves: int, start_ply: int = 0, batch_size: int = 8, prefetch: int = 2) -> AsyncIterable[Logprob]:
  """Async iterable of `Logprob`s by calling `predict`. Prefetches and batches requests"""
  return hk.vpipe(
    batched_logprobs(predict, max_moves=max_moves, start_ply=start_ply, batch_size=batch_size),
    hka.prefetched(prefetch),
    hka.flatten
  )
  