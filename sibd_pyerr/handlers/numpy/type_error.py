from sibd_pyerr.registry import register
import re


@register("TypeError", source="numpy")
def numpy_type_error(exc_type, exc_value):
    msg = str(exc_value)
    if "did not contain a loop with signature matching types" in msg:
        return "타입 오류", "NumPy 연산에 호환되지 않는 자료형이 사용되었습니다."

    return "타입 오류", "NumPy 연산에 적절하지 않은 자료형이 사용되었습니다."
