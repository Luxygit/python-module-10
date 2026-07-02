"""
functools.wraps makes it so that even if when a decorator wraps a
function and overrides its name and dosctring, .wraps copies the original
onto the wrapper so it can be read
decorator factories are use when a decorator needs its own arguments
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
            if "power" in kwargs:
                power = kwargs["power"]
            elif len(args) > 2:
                power = args[2]
            elif len(args) > 0:
                power = args[0]
            else:
                return "Insufficient power for this spell"
            if power >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable:
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
    """namespace with validation policies and deployment"""
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
    try:
        print("Testing spell timer...")
        timer_result = fireball_spell()
        print(f"Result: {timer_result}")

        print("\nTesting retrying spell...")
        attempt_counter = 0

        @retry_spell(max_attempts=3)
        def unstable_spell() -> str:
            raise ValueError("Unstable spell")

        @retry_spell(max_attempts=3)
        def flux_spell() -> str:
            nonlocal attempt_counter
            attempt_counter += 1
            if attempt_counter < 2:
                raise ValueError("Error")
            return "Cast succesfull!"
        print("Failure case:")
        print(f"{unstable_spell()}")
        print("Sucessful case:")
        print(f"{flux_spell()}")

        print("\nTesting MageGuild...")
        print("Valid name 'Gandalf'?: "
              f"{MageGuild.validate_mage_name('Gandalf')}")
        print("Valid name 'J1'?: "
              f"{MageGuild.validate_mage_name('JI')}")

        print("\nTesting power validator...")
        guild = MageGuild()
        print(guild.cast_spell("Lightning", 15))
        print(guild.cast_spell("Lightning", 5))
        print(f"Keyword Call: {guild.cast_spell(spell_name='Fire', power=20)}")
        print(f"Keyword Call: {guild.cast_spell(spell_name='Water', power=9)}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
