from sibd_pyerr.registry import register
import re


@register("IndexError", source="numpy")
def numpy_index_error(exc_type, exc_value):
    msg = str(exc_value)
    m = re.search(r"index (\d+) is out of bounds for axis (\d+) with size (\d+)", msg)
    if m:
        index, axis, size = m.groups()
        return (
            "인덱스 오류",
            f"{axis}번 축의 크기가 {size}인데, 인덱스 {index}에 접근했습니다. 유효 범위를 초과했습니다.",
        )
    return "인덱스 오류", "NumPy 배열에서 잘못된 인덱스에 접근했습니다."
