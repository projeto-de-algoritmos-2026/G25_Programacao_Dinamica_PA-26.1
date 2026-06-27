"""Algoritmo da Maior Subsequencia Crescente usando programacao dinamica."""

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class LISResult:
    """Resultado da maior subsequencia crescente."""

    indices: list[int]
    values: list[float]


def longest_increasing_subsequence(values: Sequence[float]) -> LISResult:
    """Retorna a LIS dos valores informados.

    A implementacao usa programacao dinamica O(n^2):
    dp[i] guarda o tamanho da maior subsequencia crescente que termina em i.
    previous[i] guarda o indice anterior escolhido para reconstruir a resposta.
    """

    if not values:
        return LISResult(indices=[], values=[])

    n = len(values)
    dp = [1] * n
    previous = [-1] * n

    for i in range(n):
        for j in range(i):
            if values[j] < values[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                previous[i] = j

    best_end = max(range(n), key=lambda index: dp[index])
    indices: list[int] = []

    current = best_end
    while current != -1:
        indices.append(current)
        current = previous[current]

    indices.reverse()
    return LISResult(indices=indices, values=[values[index] for index in indices])


def percentage_growth(initial: float, final: float) -> float | None:
    """Calcula crescimento percentual, ou None quando a base e zero."""

    if initial == 0:
        return None

    return ((final - initial) / initial) * 100


def best_progress_interval(values: Iterable[float]) -> tuple[int | None, float]:
    """Retorna o indice do maior salto entre registros consecutivos e seu valor."""

    values_list = list(values)
    if len(values_list) < 2:
        return None, 0

    best_index = 1
    best_delta = values_list[1] - values_list[0]

    for index in range(2, len(values_list)):
        delta = values_list[index] - values_list[index - 1]
        if delta > best_delta:
            best_index = index
            best_delta = delta

    return best_index, best_delta
