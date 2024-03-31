import json


class Helpers:

    @classmethod
    def is_json_string(cls, str) -> bool:
        try:
            json.loads(str)
            return True
        except json.JSONDecodeError as err:
            return False
