#!/usr/bin/env python3
"""Roll two six-sided dice; doubles are a win."""
import random

def main() -> None:
    first, second = random.randint(1, 6), random.randint(1, 6)
    result = f"Rolled {first} + {second} = {first + second}"
    if first == second:
        result += " - Doubles! You win!"
    print(result)

if __name__ == "__main__":
    main()
