from pyerrkor.registry import register


# 타입에러는 좀 심화해서 구현할 필요 있음
@register("TypeError")
def _handle_type_error(exc_type, exc_value):
    kor_err_name = "타입 오류"
    kor_err_message = "자료형이 맞지 않아 연산할 수 없습니다."
    return (kor_err_name, kor_err_message)
