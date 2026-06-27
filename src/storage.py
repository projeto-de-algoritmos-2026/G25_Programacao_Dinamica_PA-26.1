"""Persistencia simples em JSON para registros de treino."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from src.models import WorkoutEntry


def load_entries(path: Path) -> list[WorkoutEntry]:
    """Carrega registros de treino de um arquivo JSON."""

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        WorkoutEntry(
            exercise=item["exercise"],
            period=item["period"],
            load_kg=float(item["load_kg"]),
            reps=item.get("reps"),
            body_weight_kg=item.get("body_weight_kg"),
            measurements=item.get("measurements", {}),
        )
        for item in data
    ]


def save_entries(path: Path, entries: list[WorkoutEntry]) -> None:
    """Salva registros de treino em JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump([asdict(entry) for entry in entries], file, ensure_ascii=False, indent=2)


def append_entry(path: Path, entry: WorkoutEntry) -> None:
    """Adiciona um registro ao arquivo de dados."""

    entries = load_entries(path)
    entries.append(entry)
    save_entries(path, entries)
