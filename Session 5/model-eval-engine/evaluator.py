# evaluator.py
"""Utility functions for evaluating text similarity.

Currently implements a simple ROUGE‑L calculation based on longest common
subsequence.  The score is normalised to a value between 0 and 1.
"""

from typing import List


def _tokenise(text: str) -> List[str]:
    """Split text into tokens by whitespace.

    This simple tokenizer is sufficient for demonstration purposes.
    """
    return text.strip().split()


def _lcs_length(a: List[str], b: List[str]) -> int:
    """Return the length of the longest common subsequence of two token lists.

    Uses a classic dynamic‑programming approach with O(len(a)*len(b)) time
    and O(min(len(a), len(b))) space.
    """
    if not a or not b:
        return 0
    # Ensure the shorter list is used for the inner loop to save memory
    if len(a) < len(b):
        a, b = b, a
    previous = [0] * (len(b) + 1)
    for token_a in a:
        current = [0]
        for j, token_b in enumerate(b, 1):
            if token_a == token_b:
                current.append(previous[j - 1] + 1)
            else:
                current.append(max(previous[j], current[-1]))
        previous = current
    return previous[-1]


def rouge_l_score(candidate: str, reference: str) -> float:
    """Compute the ROUGE‑L F1 score between *candidate* and *reference*.

    Parameters
    ----------
    candidate: str
        The model generated text.
    reference: str
        The ground‑truth text.

    Returns
    -------
    float
        Normalised ROUGE‑L F1 score in the range [0, 1].
    """
    cand_tokens = _tokenise(candidate)
    ref_tokens = _tokenise(reference)
    lcs = _lcs_length(cand_tokens, ref_tokens)
    if not cand_tokens or not ref_tokens:
        return 0.0
    precision = lcs / len(cand_tokens)
    recall = lcs / len(ref_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)
