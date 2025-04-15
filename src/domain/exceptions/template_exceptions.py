class TemplateNotFoundException(Exception):
    def __init__(self, message="Template not found"):
        super().__init__(message)


class TemplateInvalidFileTypeException(Exception):
    def __init__(self, message="Invalid file type"):
        super().__init__(message)
