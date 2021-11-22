class CreateDataLakeInput:
    schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            },
            "description": {
                "type": "string"
            },
            "config": {
                "type": "string"
            },
        },
        "additionalProperties": False,
        "required": ["name", "description", "config"]
    }

    @classmethod
    def from_json(cls, data):
        self = cls()
        self.name           = data["name"]
        self.description    = data["description"]
        self.config         = data["config"]
        return self

