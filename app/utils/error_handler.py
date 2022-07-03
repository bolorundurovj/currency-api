class OpsException(Exception):
    def __init__(self, code: int = 500, message: str = "An error occurred"):
        super(OpsException, self).__init__(message, code)
        self.status = False
        self.code = code
        self.message = message
