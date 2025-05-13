from sibd_pyerr.registry import register


@register("IndexError")
def _handle_index_error(exc_type, exc_value):
    kor_err_name = "인덱스 오류"
    msg = str(exc_value)
    if "list" in msg:
        return (kor_err_name, "리스트의 인덱스 범위를 벗어났습니다.")
    elif "string" in msg:
        return (kor_err_name, "문자열의 인덱스 범위를 벗어났습니다.")
    elif "tuple" in msg:
        return (kor_err_name, "튜플의 인덱스 범위를 벗어났습니다.")
    else:
        return (kor_err_name, "자료형의 인덱스 범위를 벗어났습니다.")
