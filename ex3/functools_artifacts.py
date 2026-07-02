"""
functools reduce/operator iterate and accumulades elements into a single one
functools partial creates a new partial app callable object
functools lru_cache memoizes function returns using Least Recently
Usedcache  matching parameter combinations
functools singledispatch implements generic functions polymorphism by
calling separate sub routines mapped for the data type of the first argument
"""

import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    """
    combines powers with functional reduction
    - .reduce applies a 2arg function to elements to compress the collection
    - if input is empty it returns 0
    - operator functions provide pure functions
    """
    if not spells:
        return 0
    operations: dict[str, Callable[[int, int], int]] = {
            "add": operator.add,
            "multiply": operator.mul,
            "max": max,
            "min": min
            }
    if operation not in operations:
        print(f"Unknown magical operation: {operation}")
        return 0
    try:
        return functools.reduce(operations[operation], spells)
    except TypeError as e:
        print(f"Reducer error: {e}")
        return 0


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    """
    pre-fills base function with .partial
    - .partial freezes specific parameters returning a callable
    that only demands the remaining arguments
    - base signature is power:int, element: str, target: str
    - freeze power=50 and the element for fire ice lightning
    """
    fire_spell = functools.partial(base_enchantment, 50, "fire")
    ice_spell = functools.partial(base_enchantment, 50, "ice")
    lightning_spell = functools.partial(base_enchantment, 50, "lightning")
    return {
            "fire": fire_spell,
            "ice": ice_spell,
            "lightning": lightning_spell
            }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    """
    lru_cache intercepts recursive function entries
    if n is solved previously, execution is intercepted and
    returns the integer from an in-memory dictionary
    """
    if n < 0:
        return 0
    if n == 0:
        return 0
    if n == 1:
        return 1
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    """
    creates a single-dispatch polymorphism function router
    - .singledispatch sets up a base function block
    - .register registers type-specific variant blocks
    """
    @functools.singledispatch
    def dispatcher(spell: Any) -> str:
        # fallback message
        return "Unknown spell type"

    @dispatcher.register(int)
    def _(spell: int) -> str:
        # integer maps to damage calcs
        return f"Damage spell: {spell} damage"

    @dispatcher.register(str)
    def _(spell: str) -> str:
        # string maps to enchantment
        return f"Enchantment: {spell}"

    @dispatcher.register(list)
    def _(spell: list) -> str:
        # list items length to count elements
        return f"Multi-cast: {len(spell)} spells"
    return dispatcher


def base_enchantment_template(power: int, element: str, target: str) -> str:
    """3 parameter template placholder"""
    return f"{element.capitalize()} spell with {power} power cast on {target}"


def main() -> None:
    try:
        print("\nTesting spell reducer...")
        sample_powers = [10, 20, 30, 40]
        print(f"Sum: {spell_reducer(sample_powers, 'add')}")
        print(f"Product: {spell_reducer(sample_powers, 'multiply')}")
        print(f"Max: {spell_reducer(sample_powers, 'max')}")
        print(f"Min: {spell_reducer(sample_powers, 'min')}")

        print("\nTesting partial enchanter...")
        factories = partial_enchanter(base_enchantment_template)
        print(factories["fire"]("Goblin"))
        print(factories["ice"]("Dragon"))
        print(factories["lightning"]("Orc"))

        print("\nTesting memoized fibonacci...")
        print(f"Fib(0): {memoized_fibonacci(0)}")
        print(f"Fib(1): {memoized_fibonacci(1)}")
        print(f"Fib(10): {memoized_fibonacci(10)}")
        print(f"Fib(15): {memoized_fibonacci(15)}")

        print("\nTesting spell dispatcher...")
        dispatch = spell_dispatcher()
        print(dispatch(42))
        print(dispatch("fireball"))
        print(dispatch([1, 2, 3]))
        print(dispatch(3.14))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
