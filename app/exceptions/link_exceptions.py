class LinkAlreadyExistsError(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Short code '{code}' already exists")


class LinkNotFoundError(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Link '{code}' was not found")
