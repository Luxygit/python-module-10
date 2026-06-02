"""anonymous functions and lambda expressions"""

from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """sorts artifacts by power level"""
    return sorted(artifacts, key=lambda x: x['power'], reverse=True)


def power_filter(mages: list[dict[str, Any]], min_power: int)\
        -> list[dict[str, Any]]:
    """filters mages by power"""
    return list(filter(lambda x: x['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    """transforms spell names"""
    return list(map(lambda x: f"* {x} *", spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    """calculate max min and average power"""
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}
    powers = list(map(lambda x: x['power'], mages))
    return {
            "max_power": int(max(powers)),
            "min_power": int(min(powers)),
            "avg_power": float(round(sum(powers) / len(powers), 2))
            }


def main() -> None:
    """validating test"""
    print("\nTesting artifact sorter...")
    sample_artifacts = [
            {"name": "Crystal Orb", "power": 85, "type": "focus"},
            {"name": "Fire Staff", "power": 92, "type": "weapon"}
            ]
    sorted_arts = artifact_sorter(sample_artifacts)
    print(f"{sorted_arts[0]['name']} ({sorted_arts[0]['power']} power) "
          f"comes before {sorted_arts[1]['name']} "
          f"({sorted_arts[1]['power']} power)")
    print("\nTesting spell transformer...")
    sample_spells = ["fireball", "heal", "shield"]
    transformed = spell_transformer(sample_spells)
    print(" ".join(transformed))


if __name__ == "__main__":
    main()
