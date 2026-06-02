"""
functools.wraps makes it so that even if when a decorator wraps a
function and overrides its name and dosctring, .wraps copies the original
onto the wrapper so it can be read
decorator factories for when a decorator needs its own arguments
@staticmethod defines a method that doesnt access any class instance state
(no self nor cls params)
"""

import functools
import time
from collections.abc import Callable
from typing import Any


def spell_timer(func: Callable) -> Callable:
    """
    intercepts calls to log steps before and after
    .wrap ensures name remains the same instead of being 'wrapper'
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"Spell completed in {duration:.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> Callable:
    """
    decorator factory with power requirement validation
    3 layers
    outer layer: power validator, gets config arg (min power)
    mid layer: decorator, gets targeted func
    inner layer: wrapper. gets runtime func call *args
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """args[0] is self, so power integer is grabbed thru length"""
            if len(args) > 1 and hasattr(args[0], 'cast_spell'):
                power = args[2]
            else:
                power = args[0]
            if power >= min_power:
                return func(*args, **kwargs)
            return "Insuficcient power for this spell"
        return wrapper
    return decorator


def retr_spell(max_attempts: int) -> Callable:
    """
    decorator factory tries execution multiple times if errors occur
    loops thru try/except until max_attempts
    every exception augments attempt counter
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print(f"Spell failed, retrying..."
                              f"(attempt {attempt}/{max_attempts})")
                    else:
                        return (f"Spell casting failed after "
                                f"{max_attempts} attempts")
            return "Spell casting failed"
        return wrapper
    return decorator


class MageGuild:
    """namespace with validation policies and deplloyment"""
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        """it lacks an instance. validates name"""
        if len(name) < 3:
            return False
        return all(char.isalpha() or char.isspace() for char in name)

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        """
        if validation succeeds inner block runs and prints success
        if it fails the decorator intercepts and returns failure
        """
        return f"Successfully cast {spell_name} with {power} power"


@spell_timer
def fireball_spell() -> str:
    """base spell for timer validation"""
    time.sleep(0.1)
    return "Fireball cast!"


def main() -> None:
    print("Testing spell timer...")
    timer_result = fireball_spell()
    print(f"Result: {timer_result}")
    print("\nTesting retrying spell...")

    @retr_spell(max_attempts=3)
    def unstable_spell() -> str:
        raise ValueError("Magical volatily anomaly detected!")
    retry_result = unstable_spell()
    print(retry_result)
    print("Waaaaaaagh spelled !")

    print("\nTesting MageGuild...")
    guild = MageGuild()
    print(MageGuild.validate_mage_name("Gandalf The Grey"))
    print(MageGuild.validate_mage_name("JI"))

    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Lightning", 5))


if __name__ == "__main__":
    main()
