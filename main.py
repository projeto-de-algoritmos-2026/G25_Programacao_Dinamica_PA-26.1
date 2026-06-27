"""Sistema sem interface grafica para registrar e analisar evolucao de treinos."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.analyzer import analyze_all, analyze_exercise
from src.models import ExerciseEvolution, WorkoutEntry
from src.storage import append_entry, load_entries

DEFAULT_DATA_PATH = Path("data/workouts.json")


def parse_measurements(raw_measurements: list[str] | None) -> dict[str, float]:
    measurements: dict[str, float] = {}

    for raw_measurement in raw_measurements or []:
        if "=" not in raw_measurement:
            raise argparse.ArgumentTypeError(
                "Medidas customizadas devem usar o formato nome=valor."
            )

        name, value = raw_measurement.split("=", maxsplit=1)
        measurements[name] = float(value)

    return measurements


def format_percent(value: float | None) -> str:
    if value is None:
        return "indisponivel"

    return f"{value:+.2f}%"


def print_evolution(evolution: ExerciseEvolution) -> None:
    print(f"\nExercicio: {evolution.exercise}")
    print(f"Metrica analisada: {evolution.metric}")

    if not evolution.sequence:
        print("Nenhuma sequencia crescente encontrada.")
        return

    first = evolution.sequence[0]
    last = evolution.sequence[-1]
    sequence = " -> ".join(f"{value:g}" for value in evolution.values)

    print(f"Valor inicial: {evolution.initial_value:g} ({first.period})")
    print(f"Valor atual da sequencia: {evolution.final_value:g} ({last.period})")
    print(f"Maior sequencia de evolucao: {sequence}")
    print(f"Evolucao total: {format_percent(evolution.growth_percent)}")

    if evolution.best_period is not None:
        print(f"Melhor periodo: {evolution.best_period} ({evolution.best_delta:+g})")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analise inteligente de evolucao na academia usando LIS."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Caminho do arquivo JSON de registros.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Registra um treino.")
    add_parser.add_argument("--exercise", required=True, help="Nome do exercicio.")
    add_parser.add_argument("--period", required=True, help="Periodo do registro, ex: 2026-01.")
    add_parser.add_argument("--load", required=True, type=float, help="Carga em kg.")
    add_parser.add_argument("--reps", type=int, help="Numero de repeticoes.")
    add_parser.add_argument("--body-weight", type=float, help="Peso corporal em kg.")
    add_parser.add_argument(
        "--measurement",
        action="append",
        help="Medida customizada no formato nome=valor. Pode ser usada varias vezes.",
    )

    analyze_parser = subparsers.add_parser("analyze", help="Analisa um exercicio.")
    analyze_parser.add_argument("--exercise", required=True, help="Nome do exercicio.")
    analyze_parser.add_argument(
        "--metric",
        default="load_kg",
        help="Metrica: load_kg, reps, body_weight_kg ou uma medida customizada.",
    )

    all_parser = subparsers.add_parser("analyze-all", help="Analisa todos os exercicios.")
    all_parser.add_argument("--metric", default="load_kg", help="Metrica analisada.")

    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "add":
        entry = WorkoutEntry(
            exercise=args.exercise,
            period=args.period,
            load_kg=args.load,
            reps=args.reps,
            body_weight_kg=args.body_weight,
            measurements=parse_measurements(args.measurement),
        )
        append_entry(args.data, entry)
        print("Treino registrado com sucesso.")
        return

    entries = load_entries(args.data)

    if args.command == "analyze":
        print_evolution(analyze_exercise(entries, args.exercise, args.metric))
        return

    if args.command == "analyze-all":
        for evolution in analyze_all(entries, args.metric):
            print_evolution(evolution)


if __name__ == "__main__":
    main()
