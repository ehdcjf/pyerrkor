from sibd_pyerr.registry import register
import re


@register("KeyError", source="pandas")
def pandas_key_error(exc_type, exc_value):
    key = str(exc_value).strip("'\"")
    msg = str(exc_value)

    if "not in index" in msg or "None of" in msg:
        return "키 오류", f"DataFrame 또는 Series에 '{key}'가 존재하지 않습니다."

    return "키 오류", f"pandas 객체에서 '{key}' 키를 찾을 수 없습니다."
