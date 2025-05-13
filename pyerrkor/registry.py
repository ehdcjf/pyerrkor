_handlers: dict[str, callable] = {}


def register(error_name: str):
    def decorator(fn):
        _handlers[error_name] = fn
        return fn

    return decorator


def get_kor_error_info(exc_type, exc_value):
    err_name = exc_type.__name__
    if err_name in _handlers:
        return _handlers[err_name](exc_type, exc_value)
    return ("정의되지 않은 에러", str(exc_value))
