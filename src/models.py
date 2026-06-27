"""Modelos do dominio de treinos."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class WorkoutEntry:
    """Registro de treino de um exercicio em um periodo."""

    exercise: str
    period: str
    load_kg: float
    reps: int | None = None
    body_weight_kg: float | None = None
    measurements: dict[str, float] = field(default_factory=dict)

    def metric_value(self, metric: str) -> float | None:
        """Busca o valor de uma metrica registrada."""

        if metric == "load_kg":
            return self.load_kg
        if metric == "reps":
            return float(self.reps) if self.reps is not None else None
        if metric == "body_weight_kg":
            return self.body_weight_kg

        return self.measurements.get(metric)


@dataclass(frozen=True)
class ExerciseEvolution:
    """Analise de evolucao para uma metrica de um exercicio."""

    exercise: str
    metric: str
    sequence: list[WorkoutEntry]
    values: list[float]
    growth_percent: float | None
    best_period: str | None
    best_delta: float

    @property
    def initial_value(self) -> float | None:
        return self.values[0] if self.values else None

    @property
    def final_value(self) -> float | None:
        return self.values[-1] if self.values else None
