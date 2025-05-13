from sibd_pyerr.registry import register
import re


@register("ValueError")
def _handle_value_error(exc_type, exc_value):
    kor_err_name = "값 오류"
    msg = str(exc_value)
    kor_err_message = "잘못된 값이 사용되었습니다."

    # 예외 패턴 리스트 (정규식, 한줄 요약, 상세 설명)
    patterns = [
        (
            r"invalid literal for int\(\) with base (\d+): '(.+)'",
            "정수 변환 오류",
            lambda m: f"문자열 '{m.group(2)}'은(는) {m.group(1)}진수 정수로 변환할 수 없습니다.\n입력값이 숫자로만 이루어졌는지 확인하세요.",
        ),
        (
            r"could not convert string to float: '(.+)'",
            "실수 변환 오류",
            lambda m: f"문자열 '{m.group(1)}'은(는) 실수(float)로 변환할 수 없습니다.\n숫자가 맞는지 확인해 보세요.",
        ),
        (
            r"not enough values to unpack \(expected (\d+), got (\d+)\)",
            "언패킹 값 부족",
            lambda m: f"{m.group(1)}개의 변수에 값을 넣으려 했지만, 실제 값은 {m.group(2)}개였습니다.\n언패킹 대상의 길이를 확인하세요.",
        ),
        (
            r"too many values to unpack \(expected (\d+)\)",
            "언패킹 값 초과",
            lambda m: f"{m.group(1)}개의 변수만 필요한데, 더 많은 값을 받았습니다.\n언패킹할 객체의 길이를 확인하세요.",
        ),
        (
            r"not in list",
            "리스트에 값 없음",
            lambda m: "값이 리스트에 존재하지 않습니다.",
        ),
        (
            r"range\(\) arg 3 must not be zero",
            "range step 값 오류",
            lambda m: "`range()` 함수의 세 번째 인자(step)가 0으로 설정되었습니다.\n0은 유효한 간격(step)이 될 수 없습니다.",
        ),
    ]

    # 패턴 매칭
    for pattern, summary, explain_fn in patterns:
        m = re.search(pattern, msg)
        if m:
            return kor_err_name + f" - {summary}", explain_fn(m)

    return kor_err_name, kor_err_message
