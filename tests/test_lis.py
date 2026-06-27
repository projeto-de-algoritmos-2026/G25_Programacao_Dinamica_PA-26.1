from src.analyzer import analyze_exercise
from src.lis import longest_increasing_subsequence, percentage_growth
from src.models import WorkoutEntry


def test_lis_returns_longest_increasing_sequence():
    result = longest_increasing_subsequence([2, 4, 3, 5, 1, 6])

    assert result.values == [2, 4, 5, 6]
    assert result.indices == [0, 1, 3, 5]


def test_percentage_growth():
    assert percentage_growth(2, 10) == 400
    assert percentage_growth(0, 10) is None


def test_analyze_exercise_applies_lis_to_selected_exercise():
    entries = [
        WorkoutEntry("Supino", "Janeiro", 2),
        WorkoutEntry("Supino", "Fevereiro", 4),
        WorkoutEntry("Supino", "Marco", 3),
        WorkoutEntry("Supino", "Abril", 8),
        WorkoutEntry("Supino", "Maio", 10),
        WorkoutEntry("Remada", "Janeiro", 30),
    ]

    evolution = analyze_exercise(entries, "Supino")

    assert evolution.values == [2, 4, 8, 10]
    assert evolution.growth_percent == 400
    assert evolution.best_period == "Abril"
