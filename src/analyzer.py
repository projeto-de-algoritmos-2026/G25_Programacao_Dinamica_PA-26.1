"""Analise da evolucao de treino usando LIS."""

from collections import defaultdict
from collections.abc import Iterable

from src.lis import best_progress_interval, longest_increasing_subsequence, percentage_growth
from src.models import ExerciseEvolution, WorkoutEntry


def analyze_exercise(
    entries: Iterable[WorkoutEntry],
    exercise: str,
    metric: str = "load_kg",
) -> ExerciseEvolution:
    """Aplica LIS para uma metrica de um exercicio especifico."""

    exercise_entries = [
        entry
        for entry in entries
        if entry.exercise.lower() == exercise.lower() and entry.metric_value(metric) is not None
    ]

    values = [entry.metric_value(metric) for entry in exercise_entries]
    numeric_values = [value for value in values if value is not None]
    lis = longest_increasing_subsequence(numeric_values)
    sequence = [exercise_entries[index] for index in lis.indices]

    growth = None
    if lis.values:
        growth = percentage_growth(lis.values[0], lis.values[-1])

    best_index, best_delta = best_progress_interval(lis.values)
    best_period = sequence[best_index].period if best_index is not None and sequence else None

    return ExerciseEvolution(
        exercise=exercise,
        metric=metric,
        sequence=sequence,
        values=lis.values,
        growth_percent=growth,
        best_period=best_period,
        best_delta=best_delta,
    )


def analyze_all(entries: Iterable[WorkoutEntry], metric: str = "load_kg") -> list[ExerciseEvolution]:
    """Aplica LIS separadamente para cada exercicio encontrado."""

    by_exercise: dict[str, list[WorkoutEntry]] = defaultdict(list)
    for entry in entries:
        by_exercise[entry.exercise].append(entry)

    return [
        analyze_exercise(exercise_entries, exercise, metric)
        for exercise, exercise_entries in sorted(by_exercise.items())
    ]
