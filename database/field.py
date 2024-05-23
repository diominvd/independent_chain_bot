class Field:
    def __init__(self, name: str, field_type: str, parameters: str = None):
        self.name = name
        self.type = field_type

        if parameters:
            self.type += f" {parameters}"
