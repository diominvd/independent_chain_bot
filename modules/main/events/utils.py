import random


def spin() -> tuple:
    values: list = ["🍋", "🍒", "💎"]
    result: list = [random.choice(values) for i in range(3)]

    match result:
        case ["🍋", "🍋", "🍋"]:
            reward: float = 150.0
        case ["🍒", "🍒", "🍒"]:
            reward: float = 150.0
        case ["💎", "💎", "💎"]:
            reward: float = 200.0
        case _:
            reward: float = 0.0

    result: str = f"|{result[0]}|{result[1]}|{result[2]}|"
    return result, reward