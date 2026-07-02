"""high order functions take other functions as arguments"""

from collections.abc import Callable


def spell_combiner(
        spell1: Callable[[str, int], str],
        spell2: Callable[[str, int], str]
        ) -> Callable[[str, int], tuple[str, str]]:
    """
    combining 2 functions into 1
    inner function that accepts target and power
    combined_spell runs both original functions
    joins both output strings into a tuple
    """
    def combined_spell(target: str, power: int) -> tuple[str, str]:
        """executes both functions with the same parameters"""
        try:
            return (spell1(target, power), spell2(target, power))
        except Exception as e:
            print(f"Combiner Stream Error: {e}")
            return ("Spell 1 failed", "Spell 2 failed")
    return combined_spell


def power_amplifier(
    base_spell: Callable[[str, int], str], multiplier: int
        ) -> Callable[[str, int], str]:
    """
    modifying arguments
    - captures multiplier and base spell inside a closure
    - returned function maintains the same signature as base
    """
    def amplified_spell(target: str, power: int) -> str:
        try:
            return base_spell(target, power * multiplier)
        except Exception as e:
            return f"Amplified error: {e}"
    return amplified_spell


def conditional_caster(condition: Callable[[str, int], bool],
                       spell: Callable[[str, int], str]
                       ) -> Callable[[str, int], str]:
    """
    returns a new spell only if a condition is true
    - takes a test and a execution function
    """
    def cond_spell(target: str, power: int) -> str:
        try:
            if condition(target, power):
                return spell(target, power)
            return "Spell fizzled"
        except Exception as e:
            return f"Condition error: {e}"
    return cond_spell


def spell_sequence(
        spells: list[Callable[[str, int], str]]
        ) -> Callable[[str, int], list[str]]:
    """
    returns one function that executes a list of spells
    - accepts list of functions
    - returned function loops thru each
    - each is executed with the original target and power
    """
    def executed_sequence(target: str, power: int) -> list[str]:
        results = []
        for spell in spells:
            try:
                results.append(spell(target, power))
            except Exception as e:
                results.append(f"Sequence error: {e}")
        return results
    return executed_sequence


def fireball(target: str, power: int) -> str:
    """baseline spell"""
    return f"Fireball hits {target} for {power}"


def heal(target: str, power: int) -> str:
    return f"Heals {target} for {power}"


def main() -> None:
    try:
        print("\nTesting spell combiner...")
        combined = spell_combiner(fireball, heal)
        res1, res2 = combined("Dragon", 10)
        print(f"Combined spell result: {res1}, {res2}")

        print("\nTesting power amplifier...")
        base_power = 10
        multiplier = 3
        mega_fireball = power_amplifier(fireball, multiplier)
        mega_out = mega_fireball("Dragon", base_power)
        print(f"Original: {base_power}, Amplified: {base_power * multiplier}")
        print(f"Amplified {mega_out}")

        print("\nTesting conditional caster...")

        def high_power_only(target: str, power: int) -> bool:
            return power >= 20
        cond_fireball = conditional_caster(high_power_only, fireball)
        print("Power needed is 20:")
        print(f"Power 25: {cond_fireball('Dragon', 25)}")
        print(f"Power 15: {cond_fireball('Dragon', 15)}")

        print("\nTesting spell sequence...")
        spell_chain: list[Callable] = [fireball, heal, fireball]
        sequence_executor = spell_sequence(spell_chain)
        sequence_results = sequence_executor("Dragon", 10)
        print(f"Sequence results: {sequence_results}")
    except Exception as e:
        print(f"Global error: {e}")


if __name__ == "__main__":
    main()
