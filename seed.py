"""Script para popular o banco de dados com dados de teste realistas."""

import random
from pathlib import Path
from src.models import WorkoutEntry
from src.storage import save_entries

DATA_PATH = Path("data/workouts.json")

def generate_seed_data() -> list[WorkoutEntry]:
    entries = []
    
    # 1. Supino Reto (Evolução constante com pequenos altos e baixos para testar a LIS)
    base_supino = 40.0
    for month in range(1, 13):
        period = f"2025-{month:02d}"
        
        # Cresce na maioria das vezes, mas tem umas quedas
        if month == 5:
            # Pegou um resfriado, carga caiu
            load = base_supino - 5.0
        elif month == 10:
            # Semana ruim
            load = base_supino - 2.0
        else:
            load = base_supino
            base_supino += random.choice([0.0, 2.0, 2.0, 4.0]) # Progressão
            
        entries.append(
            WorkoutEntry(
                exercise="Supino Reto",
                period=period,
                load_kg=round(load, 1),
                reps=random.choice([8, 10, 12]),
                body_weight_kg=75.0 + (month * 0.2), # Ganhando peso aos poucos
            )
        )

    # 2. Agachamento Livre (Evolução excelente)
    base_agachamento = 60.0
    for month in range(1, 13):
        period = f"2025-{month:02d}"
        load = base_agachamento
        base_agachamento += random.choice([2.0, 4.0, 5.0])
        
        entries.append(
            WorkoutEntry(
                exercise="Agachamento Livre",
                period=period,
                load_kg=round(load, 1),
                reps=random.choice([6, 8, 10]),
                body_weight_kg=75.0 + (month * 0.2),
            )
        )

    # 3. Desenvolvimento (Evolução estagnada/difícil)
    base_desenvolvimento = 20.0
    for month in range(1, 13):
        period = f"2025-{month:02d}"
        
        # Sobe devagar e as vezes cai
        load = base_desenvolvimento + random.choice([-2.0, 0.0, 0.0, 2.0])
        if load > base_desenvolvimento + 2:
            base_desenvolvimento = load
            
        entries.append(
            WorkoutEntry(
                exercise="Desenvolvimento",
                period=period,
                load_kg=round(load, 1),
                reps=random.choice([8, 10, 12]),
                body_weight_kg=75.0 + (month * 0.2),
            )
        )

    return entries

def main():
    print(f"Gerando dados aleatórios em {DATA_PATH}...")
    entries = generate_seed_data()
    save_entries(DATA_PATH, entries)
    print(f"✅ {len(entries)} registros criados com sucesso!")
    print("Agora você pode rodar a interface web para ver os gráficos!")

if __name__ == "__main__":
    main()
