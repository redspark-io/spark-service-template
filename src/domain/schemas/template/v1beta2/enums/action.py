from enum import Enum


class ActionEnum(str, Enum):
    fetch_template = "fetch:template"
    fetch_plain = "fetch:plain"
