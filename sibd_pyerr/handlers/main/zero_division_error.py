from sibd_pyerr.registry import register


@register("ZeroDivisionError")
def _handle_zero_division_error(exc_type, exc_value):
    return ("0나누기 오류", "0으로 나누기를 시도했습니다.")
