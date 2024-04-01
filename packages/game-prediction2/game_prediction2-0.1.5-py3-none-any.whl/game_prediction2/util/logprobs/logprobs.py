from editdistance import distance as edit_dist
import numpy as np
from chess_notation.represent import representations
from chess_notation.language import Language
from chess_utils import CapturablePiece
from ...beam import Logprob

def pseudo_logp(word: str, top_preds: list[tuple[str, float]]) -> float:
  """Approximates the log probability of `word` given a subset of the best outputs `top_preds` of a model.
  - `top_preds :: [(Pred, Logprob)]`: the top-k predictions of a model with probability distribution `P`
    - So, each `(pred, logp) in top_preds` holds `logp = log P(pred)`
  - If `word` is in `top_preds`, the real log-probability is returned
  - Otherwise, an approximation factor `alpha(p)` is computed as `1 - NED(word, p)` for every `p in preds`
    - `NED` is the Normalized Edit Distance (normalized over `len(word)`)
    - If `NED(word, p) <= 1`, the assigned probability is `P(p)*alpha(p)`
    - Otherwise, the probability is 0
  - The maximum across all computed probabilities is returned
  
  **Note: both computations and the returned value are indeed log-probabilities. The explanation talks normal probabilities for clarity**
  """
  return max(
    (np.log(1 - dist/len(word)) + logp
    for pred, logp in top_preds if (dist := edit_dist(pred, word)) < min(len(word), len(pred))),
    default=-float('inf')
  )
  

def max_pseudo_logp(san: str, captured_piece: CapturablePiece | None, top_preds: list[tuple[str, float]], langs: list[Language]) -> float:
  """Max `pseudo_logp` across all possible representations of `san`"""
  reprs = set(representations(san, captured_piece=captured_piece, languages=langs))
  return max(pseudo_logp(r, top_preds) for r in reprs)

def players_max_pseudo_logp(san: str, captured_piece: CapturablePiece | None, players_preds: tuple[list[tuple[str, float]], ...], players_langs: tuple[list[Language], ...]) -> float:
  """Max `max_pseudo_logp` across players"""
  assert len(players_preds) == len(players_langs), f'ERROR: Inconsistent number of players: {len(players_preds)} preds, but {len(players_langs)} languages'
  return max(
    max_pseudo_logp(san, captured_piece, preds, langs)
    for preds, langs in zip(players_preds, players_langs)
  )
  
def logprob(players_preds: list[list[tuple[str, float]]]) -> Logprob:
  """Wrapper around `players_max_pseudo_logp`, with predefined languages (a future API will completely exclude them, as they'll be auto-detected)"""
  def _logprob(san: str, captured_piece: CapturablePiece | None):
    return players_max_pseudo_logp(san, captured_piece, players_preds, [['CA'] for _ in players_preds])
  return _logprob
  
def weighted_geo_mean(logp: float, logq: float, a: float, b: float):
  """Weighted geometrical mean (`[p^a * q^b]^(1/(a+b))`) but in log-space"""
  return (a*logp + b*logq) / (a+b)