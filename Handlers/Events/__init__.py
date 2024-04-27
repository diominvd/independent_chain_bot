def ru_events(*args) -> str:
    return \
        f"В разработке."


def en_events(*args) -> str:
    return \
        f"In development."


strings: dict = {
    "events": {
        "ru": ru_events,
        "en": en_events
    }
}