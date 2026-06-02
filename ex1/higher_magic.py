"""high order functions take other functions as arguments"""

from collections.abc import Callable, Sequence


def spell_combiner(
        spell1: Callable[[str, int], str], spell2: Callable[[str, int], str])\
                -> Callable[[str, int], tuple[str, str]]:
    """
    combining 2 functions into 1
    inner function that accepts target and power
    combined_spell runs both original functions
    joins both output strings into a tuple
    """
    def combined_spell(target: str, power: int) -> tuple[str, str]:
        """
        executes both functions with the same parameters
        """
        result1 = spell1(target, power)
        result2 = spell2(target, power)
        return (result1, result2)
    return combined_spell


def power_amplifier(
    base_spell: Callable[[str, int], str], multiplier: int)\
            -> Callable[[str, int], str]:
    """
    modifying arguments
    - captures multiplier and base spell inside a closure
    - returned function maintains the same signature as base
    """
    def amplified_spell(target: str, power: int) -> str:
        new_power = power * multiplier
        return base_spell(target, new_power)
    return amplified_spell


def conditional_caster(condition: Callable[[str, int], bool],
                       spell: Callable[[str, int], str])\
                               -> Callable[[str, int], str]:
    """
    returns a new spell only if a condition is true
    - takes a test and a execution function
    """
    def guarded_spell(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return guarded_spell


def spell_sequence(spells: Sequence[Callable[[str, int], str]])\
        -> Callable[[str, int], list[str]]:
    """
    returns one function that executes a list of spells
    - accepts list of functions
    - returned function loops thru each
    - each is executed with the original target and power
    """
    def executed_sequence(target: str, power: int) -> list[str]:
        results = []
        for individual_spell in spells:
            results.append(individual_spell(target, power))
        return results
    return executed_sequence


def fireball(target: str, power: int) -> str:
    """baseline spell"""
    return f"Fireball hits {target}"


def heal(target: str, power: int) -> str:
    return f"Heals {target}"


def main() -> None:
    print("\nTesting spell combiner...")
    combined = spell_combiner(fireball, heal)
    res1, res2 = combined("Dragon", 10)
    print(f"Combined spell result: {res1}, {res2}")
    
    print("\nTesting power amplifier...")
    base_power = 10
    multiplier = 3
    mega_fireball = power_amplifier(fireball, multiplier)
    mega_fireball("Dragon", base_power)
    print(f"Original: {base_power}, Amplified: {base_power * multiplier}")
    
    print("\nTesting conditional caster...")

    def high_power_only(target: str, power: int) -> bool:
        return power >= 20

    guarded_fireball = conditional_caster(high_power_only, fireball)
    print(f"Power needed is 20:")
    print(f"Power 25: {guarded_fireball('Dragon', 25)}")
    print(f"Power 15: {guarded_fireball('Dragon', 15)}")
    
    print("\nTesting spell sequence...")
    spell_chain: list[Callable[[str, int], str]] = [fireball, heal, fireball]
    sequence_executor = spell_sequence(spell_chain)
    sequence_results = sequence_executor("Dragon", 10)
    print(f"Sequence results: {sequence_results}")


if __name__ == "__main__":
    main()
