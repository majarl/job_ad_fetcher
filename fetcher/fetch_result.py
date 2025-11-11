from typing import Any


class FetchResult:
    success: bool
    msg: str
    payload: Any
    exception: Exception | None

    def __init__(self,
                 success: bool = False,
                 msg: str = "Empty",
                 payload: Any = None,
                 exception: Exception | None  = None):
        self.success = success
        self.msg = msg
        self.payload = payload
        self.exception = exception

    def __repr__(self):
        return f"""FetchResult:
        {self.success=}
        {self.msg=}
        {self.payload=}
        {self.exception=}
        """

    def ok(self):
        return self.success

    def failed(self):
        return not self.success

    @staticmethod
    def success(payload: Any):
        return FetchResult(
            success=True,
            msg="Ok",
            payload=payload,
            exception=None
        )

    @staticmethod
    def error(msg: str, exception: Exception | None = None):
        return FetchResult(
            success=False,
            msg=msg,
            payload=None,
            exception=exception
        )


