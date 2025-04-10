from enum import Enum


class ActionEnum(str, Enum):
    fetch_template = "fetch:template"
    fetch_plain = "publish:github"
    application_register = "application:register"
