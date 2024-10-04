import json
import logging
from datetime import date, datetime

class SensitiveDict:
    def __init__(self, data):
        self._data = data

    def __repr__(self):
        return "<SensitiveDict>"

    def __str__(self):
        return self.__repr__()

    def get_data(self):
        return self._data
    

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SensitiveDict):
            return str(obj)
        if isinstance(obj, logging.Logger):
            return "<Logger>"
        if isinstance(obj, (date, datetime)):
            return obj.strftime("%Y-%m-%d")
        return super().default(obj)
