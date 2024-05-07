class Markdown:
    @staticmethod
    def bold(text: str) -> str:
        return f"<b>{text}</b>"

    @staticmethod
    def monospaced(text: str) -> str:
        return f"<code>{text}</code>"