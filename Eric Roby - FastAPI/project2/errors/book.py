
class BookException(Exception):
    def __init__(self, detail: str = "BookException"):
        self.detail = detail

    def __str__(self):
        return f"BookException: {self.detail}"


