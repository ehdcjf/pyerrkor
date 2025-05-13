from sibd_pyerr.registry import register


@register("IndentationError")
def _handle_indentation_error(exc_type, exc_value):
    kor_err_name = "들여쓰기 오류"
    kor_err_message = "들여쓰기가 잘못되었습니다"
    return (kor_err_name, kor_err_message)
