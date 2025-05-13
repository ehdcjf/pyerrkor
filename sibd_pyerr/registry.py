builtin_handlers: dict[str, callable] = {}
pandas_handlers: dict[str, callable] = {}
numpy_handlers: dict[str, callable] = {}


def register(error_name: str, source="builtin"):
    def decorator(fn: callable):
        if source == "pandas":
            pandas_handlers[error_name] = fn
        elif source == "numpy":
            numpy_handlers[error_name] = fn
        else:
            builtin_handlers[error_name] = fn
        return fn

    return decorator


def detect_source(exc_type, exc_value):
    msg = str(exc_value)

    # 메시지 기반 pandas 감지
    if "not in index" in msg or "None of" in msg or "DataFrame" in msg:
        return "pandas"

    # traceback 기반
    tb = exc_value.__traceback__
    while tb:
        filename = tb.tb_frame.f_globals.get("__file__", "").lower()
        if "pandas" in filename:
            return "pandas"
        if "numpy" in filename:
            return "numpy"
        tb = tb.tb_next
    return "builtin"


def get_kor_error_info(exc_type, exc_value):
    err_name = exc_type.__name__
    source = detect_source(exc_type, exc_value)

    handler_sets = {
        "builtin": builtin_handlers,
        "pandas": pandas_handlers,
        "numpy": numpy_handlers,
    }

    handler = handler_sets.get(source, {}).get(err_name)
    if handler:
        return handler(exc_type, exc_value)

    return ("아직 한글화되지 않은 에러", str(exc_value))
