"""Interface web Flask para o sistema de análise de evolução de treinos.

Reutiliza integralmente a lógica implementada em src/ (LIS, analyzer, models, storage).
Nenhuma lógica de negócio é duplicada aqui — apenas a camada de apresentação.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

from src.analyzer import analyze_all, analyze_exercise
from src.lis import longest_increasing_subsequence
from src.models import WorkoutEntry
from src.storage import append_entry, load_entries

app = Flask(__name__)
app.secret_key = "gymtracker-lis-2026"

DATA_PATH = Path("data/workouts.json")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_exercise_names(entries: list[WorkoutEntry]) -> list[str]:
    """Retorna nomes únicos de exercícios, ordenados."""
    return sorted({e.exercise for e in entries})


def _build_chart_data(
    entries: list[WorkoutEntry],
    exercise: str,
    metric: str,
) -> tuple[list[str], list[float], list[int]]:
    """Monta labels, valores e índices da LIS para os gráficos.

    Usa exatamente as mesmas funções do colega para garantir consistência.
    """
    filtered = [
        e for e in entries
        if e.exercise.lower() == exercise.lower()
        and e.metric_value(metric) is not None
    ]
    values = [e.metric_value(metric) for e in filtered]
    numeric = [v for v in values if v is not None]
    labels = [e.period for e in filtered]

    lis = longest_increasing_subsequence(numeric)

    return labels, numeric, lis.indices


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def dashboard():
    """Dashboard principal — mostra todos os exercícios com mini gráficos."""
    entries = load_entries(DATA_PATH)
    evolutions = analyze_all(entries)

    # Dados para mini gráficos
    all_labels: dict[str, list[str]] = {}
    all_values: dict[str, list[float]] = {}
    lis_indices: dict[str, list[int]] = {}

    for evo in evolutions:
        labels, values, indices = _build_chart_data(entries, evo.exercise, evo.metric)
        all_labels[evo.exercise] = labels
        all_values[evo.exercise] = values
        lis_indices[evo.exercise] = indices

    # Estatísticas do header
    total_exercises = len(evolutions)
    total_entries = len(entries)

    growths = [
        evo.growth_percent for evo in evolutions
        if evo.growth_percent is not None
    ]
    best_growth = f"+{max(growths):.0f}%" if growths else "—"

    lis_lengths = [len(evo.values) for evo in evolutions]
    longest_lis = max(lis_lengths) if lis_lengths else 0

    return render_template(
        "index.html",
        evolutions=evolutions,
        all_labels=all_labels,
        all_values=all_values,
        lis_indices=lis_indices,
        total_exercises=total_exercises,
        total_entries=total_entries,
        best_growth=best_growth,
        longest_lis=longest_lis,
    )


@app.route("/exercise/<name>")
def exercise_detail(name: str):
    """Página de análise detalhada de um exercício."""
    metric = request.args.get("metric", "load_kg")
    entries = load_entries(DATA_PATH)

    evolution = analyze_exercise(entries, name, metric)
    labels, values, indices = _build_chart_data(entries, name, metric)

    return render_template(
        "exercise.html",
        evolution=evolution,
        all_labels=labels,
        all_values=values,
        lis_indices=indices,
    )


@app.route("/add", methods=["GET"])
def add_page():
    """Formulário para registrar um novo treino."""
    entries = load_entries(DATA_PATH)
    exercises = _get_exercise_names(entries)
    return render_template("add.html", exercises=exercises)


@app.route("/add", methods=["POST"], endpoint="add_entry")
def add_entry_route():
    """Processa o formulário de registro de treino."""
    try:
        exercise = request.form["exercise"].strip()
        period = request.form["period"].strip()
        load_kg = float(request.form["load"])

        reps_raw = request.form.get("reps", "").strip()
        reps = int(reps_raw) if reps_raw else None

        bw_raw = request.form.get("body_weight", "").strip()
        body_weight = float(bw_raw) if bw_raw else None

        # Medidas customizadas
        measurement_names = request.form.getlist("measurement_name[]")
        measurement_values = request.form.getlist("measurement_value[]")
        measurements: dict[str, float] = {}
        for m_name, m_value in zip(measurement_names, measurement_values):
            m_name = m_name.strip()
            if m_name and m_value.strip():
                measurements[m_name] = float(m_value)

        entry = WorkoutEntry(
            exercise=exercise,
            period=period,
            load_kg=load_kg,
            reps=reps,
            body_weight_kg=body_weight,
            measurements=measurements,
        )

        append_entry(DATA_PATH, entry)
        flash("Treino registrado com sucesso!", "success")

    except (ValueError, KeyError) as exc:
        flash(f"Erro ao registrar treino: {exc}", "error")

    return redirect(url_for("add_page"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
