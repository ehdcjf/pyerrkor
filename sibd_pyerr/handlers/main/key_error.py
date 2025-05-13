from sibd_pyerr.registry import register
import re


@register("KeyError")
def builtin_key_error(exc_type, exc_value):
    msg = str(exc_value)
    clean_key = msg.strip("'\"")

    # 1. dict에서 없는 키 접근
    return (
        "키 오류",
        f"딕셔너리에 존재하지 않는 키 '{clean_key}'를 사용했습니다.",
    )
