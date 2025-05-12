from pyerrkor.registry import register


@register("ZeroDivisionError")
def _handle_zero_division_error(exc_type, exc_value):
    kor_err_name = "0나누기 오류"
    kor_err_message = "0으로 나누기를 시도했습니다."
    return (kor_err_name, kor_err_message)
