class AppError(Exception):
    def __init__(self, message: str = 'AppError message', code: str = 'app_error_000') -> None:
        self.message = message
        self.code = code
        super().__init__(message)

    def get_message(self) -> str:
        return self.message

    def get_code(self) -> str:
        return self.code
