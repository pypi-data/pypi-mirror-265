from typing import Protocol, Iterable, AsyncIterable, Unpack
import ramda as R
import haskellian as hk
from haskellian import asynch as hka
import chess
import lcz
from ..util import logprobs as logps
from .succs import AggregateLogps, Params as SuccParams, Logprob, successors, Node, Child

class UCIPrior(Protocol):
  """Evaluates a batch of `fens` into `UCI -> Probability` mappings"""
  def __call__(self, fens: Iterable[str]) -> list[dict[str, float]]:
    ...
    
class BeamWidth(Protocol):
  def __call__(self, ply: int) -> int:
    ...

class Params(SuccParams):
  uci_prior: UCIPrior
  agg_logp: AggregateLogps
  beam_width: BeamWidth
  fen: str
  
default_params = Params(
  uci_prior=lcz.eval,
  agg_logp=lambda lp, lq: logps.weighted_geo_mean(lp, lq, a=10, b=1),
  beam_width=lambda _: 4,
  fen=chess.STARTING_FEN
)

Beam = list[Node]

async def search(logprobs: AsyncIterable[Logprob], **params: Unpack[Params]) -> AsyncIterable[Beam]:
  """Beam search across the forest of moves stemming from `start_fens`
  - `logprobs[ply](san, piece)`: (OCR) log-probability of `san` (which captures `piece`) at `ply`
  - `uci_prior(fens)`: batched prior distribution of legal moves (defaults to using `MaiaChess` with `Leela Chess Zero`)
  - `agg_logp(logp, logq)`: aggregation function of the OCR and prior log-probabilities. Defaults to a weighted geometric average giving the OCR probabilities 10x the importance. I.e. `(p^10 * q)^(1/11)` (but in log-space, ofc)
  """
  p = default_params | params
  beam: Beam = [Node(p['fen'])]
  priors = p['uci_prior']([p['fen']])
  async for i, lp in hka.enumerate(logprobs):
    succs: list[Child] = hk.vpipe(
      zip(beam, priors),
      hk.map(lambda node_prior: successors(*node_prior, lp, p['agg_logp'], **R.pick(['logp_min', 'ocr_logp_,in'], p))),
      hk.flatten, list
    )
    if succs == []:
        return
    else:
        beam = sorted(succs, key=R.prop("sum_logp"), reverse=True)[:p['beam_width'](i)]
        priors = p['uci_prior'](n.fen for n in beam)
        yield beam