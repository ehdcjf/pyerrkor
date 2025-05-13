from sibd_pyerr.registry import register


@register("ZeroDivisionError", source="numpy")
def numpy_zero_division_error(exc_type, exc_value):
    return "0 나누기 오류", "NumPy 연산 중 0으로 나누기를 시도했습니다."
