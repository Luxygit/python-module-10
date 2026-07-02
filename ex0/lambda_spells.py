"""anonymous functions and lambda expressions"""

from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """sorts artifacts by power level"""
    try:
        return sorted(artifacts, key=lambda x: x['power'], reverse=True)
    except Exception as e:
        print(f"Warning corrupted data {e}")
        return []


def power_filter(
        mages: list[dict[str, Any]], min_power: int
        ) -> list[dict[str, Any]]:
    """filters mages by power"""
    try:
        return list(filter(lambda x: x['power'] >= min_power, mages))
    except Exception as e:
        print(f"Warning corrupted data {e}")
        return []


def spell_transformer(spells: list[str]) -> list[str]:
    """transforms spell names"""
    try:
        return (list(map(lambda x: f"* {x} *", spells)))
    except Exception as e:
        print(f"Warning corrupted data {e}")
        return []


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    """calculate max min and average power"""
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}
    try:
        powers = list(map(lambda x: x['power'], mages))
        return {
                "max_power": int(max(powers)),
                "min_power": int(min(powers)),
                "avg_power": float(round(sum(powers) / len(powers), 2))
                }
    except Exception as e:
        print(f"Warning corrupted data {e}")
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}


def main() -> None:
    """validating test"""
    try:
        print("\nTesting artifact sorter from strongest to weakest")
        sample_artifacts = [
                {"name": "Crystal Orb", "power": 85, "type": "energy"},
                {"name": "Fire Staff", "power": 92, "type": "magical"},
                {"name": "Machinge Gun", "power": 2, "type": "projectiles"}
                ]
        sample_mages = [
                {"name": "Merlin", "power": 10},
                {"name": "Gandalf", "power": 40},
                {"name": "Diego", "power": 9000},
                ]
        sorted_ar = artifact_sorter(sample_artifacts)
        for order, art in enumerate(sorted_ar, 1):
            print(f"{order}: {art['name']} ({art['power']}) power")

        print("\nTesting power filter")
        strong_mages = power_filter(sample_mages, 50)
        print(f"Mages with power >= 50: {[m['name'] for m in strong_mages]}")

        print("\nTesting spell transformer...")
        sample_spells = ["fireball", "heal", "shield"]
        transformed = spell_transformer(sample_spells)
        print(" ".join(transformed))

        print("\nTesting mage stats")
        stats = mage_stats(sample_mages)
        print(f"Stats: {stats}")
    except Exception as e:
        print(f"Warning corrupted data {e}")


if __name__ == "__main__":
    main()
