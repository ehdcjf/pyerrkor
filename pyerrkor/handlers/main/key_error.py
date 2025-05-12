from pyerrkor.registry import register


@register("KeyError")
def _handle_key_error(exc_type, exc_value):
    kor_err_name = "키 오류"
    kor_err_message = "딕셔너리에 존재하지 않는 키를 사용했습니다."
    return (kor_err_name, kor_err_message)
