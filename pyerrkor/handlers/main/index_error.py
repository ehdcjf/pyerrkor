from pyerrkor.registry import register


@register("IndexError")
def _handle_index_error(exc_type, exc_value):
    kor_err_name = "인덱스 오류"
    kor_err_message = "인덱스를 잘못 사용했습니다."
    return (kor_err_name, kor_err_message)
