"""
lexical scoping and stateful closure using nonlocal keyword
Lexical scoping n closures remember access to variables from its
enclosing function env even after the outer function has finished executing.
Each time a factory functions is called their encapsulated state creates
a new environment.
"""

from collections.abc import Callable


def mage_counter() -> Callable[[], int]:
    """
    count is defined in the parent scope
    the inner function uses nonlocal count saying it wants to
    modify that parent variable instead of making a local one
    each call adds up on that remembered variable
    """
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    """
    each call augments total power using nonlocal access
    """
    total_power = initial_power

    def accumulator(power: int) -> int:
        nonlocal total_power
        try:
            total_power += power
            return total_power
        except Exception as e:
            print(f"Error {e}")
            return 0
    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    """
    captures enchantmenttype string param
    inner function gets this read-only value from parent to
    create the concatenated string
    """
    def enchanter(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return enchanter


def memory_vault() -> dict[str, Callable]:
    """
    emulates private storage using a hidden dictionary
    - vault is the local dict only touched by the inner functions
    - outer function returns both inner grouped in a dict allowing
    external code to modify and read internal states
    """
    vault: dict[str, int] = {}

    def store(key: str, value: int) -> None:
        """nonlocal not needed since dict is mutated"""
        try:
            vault[key] = value
        except Exception as e:
            print(f"Error: {e}")

    def recall(key: str) -> int | str:
        """safe lookup"""
        try:
            clean_key = str(key)
            if clean_key in vault:
                return vault[clean_key]
            return "Memory not found"
        except Exception as e:
            print(f"Error: {e}")
            return "Memory not found"
    return {
            "store": store,
            "recall": recall
            }


def main() -> None:
    try:
        print("Testing mage counter...")
        counter_a = mage_counter()
        counter_b = mage_counter()
        print(f"counter_a call 1: {counter_a()}")
        print(f"counter_a call 2: {counter_a()}")
        print(f"counter_b call 1: {counter_b()}")

        print("\nTesting spell accumulator...")
        accumulator = spell_accumulator(100)
        print(f"Base 100, add 20: {accumulator(20)}")
        print(f"Base 100, add 30: {accumulator(30)}")

        print("\nTesting enchantment factory...")
        fire_factory = enchantment_factory("Flaming")
        ice_factory = enchantment_factory("Frozen")
        print(fire_factory("Sword"))
        print(ice_factory("Shield"))

        print("\nTesting memory vault...")
        vault = memory_vault()
        print("Store 'secret' = 42")
        vault["store"]("secret", 42)
        print(f"Recall 'secret': {vault['recall']('secret')}")
        print(f"Recall 'unknown': {vault['recall']('unknown')}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
