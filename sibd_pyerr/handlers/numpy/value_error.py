from sibd_pyerr.registry import register
import re


@register("ValueError", source="numpy")
def numpy_value_error(exc_type, exc_value):
    msg = str(exc_value)

    # reshape 관련 에러
    m = re.search(r"cannot reshape array of size (\d+) into shape (.+)", msg)
    if m:
        size, shape = m.groups()
        return ("값 오류", f"크기가 {size}인 배열을 {shape} 형태로 변경할 수 없습니다.")

    # broadcasting 관련
    if "could not broadcast input array" in msg:
        return "값 오류", "NumPy 배열을 해당 크기로 브로드캐스팅할 수 없습니다."

    return "값 오류", "NumPy 연산 중 값의 형태가 올바르지 않습니다."
