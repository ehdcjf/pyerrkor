import re
from sibd_pyerr.registry import register


@register("NameError")
def handle_name_error(exc_type, exc_value):
    kor_err_name = "이름 오류"
    m = re.search(r"name '(.+?)' is not defined", str(exc_value))
    var = m.group(1) if m else ""
    message = f"정의되지 않은 변수 '{var}'를 사용했습니다."
    return kor_err_name, message
