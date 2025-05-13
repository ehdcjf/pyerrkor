from sibd_pyerr.registry import register
import re


@register("AttributeError")
def handle_attribute_error(exc_type, exc_value):
    kor_err_name = "속성 오류"
    msg = str(exc_value)

    patterns = [
        (
            r"'(\w+)' object has no attribute '(\w+)'",
            "객체 속성 없음",
            lambda m: f"{m.group(1)} 자료형에는 '{m.group(2)}' 속성이 없습니다.\n"
            f"자료형에 맞는 메서드인지 확인하거나, 오타 여부를 검토하세요.",
        ),
        (
            r"module '(\w+)' has no attribute '(\w+)'",
            "모듈 속성 없음",
            lambda m: f"'{m.group(1)}' 모듈에는 '{m.group(2)}' 속성이 없습니다.\n"
            f"오타이거나, 해당 모듈에서 제공되지 않는 함수일 수 있습니다.",
        ),
        (
            r"'NoneType' object has no attribute '(\w+)'",
            "None 접근 오류",
            lambda m: f"변수가 None인 상태에서 '{m.group(1)}' 속성에 접근하려 했습니다.\n"
            f"변수에 값이 할당되었는지 확인하세요.",
        ),
        (
            r"'(\w+)' object has no attribute '__getitem__'",
            "인덱싱 불가",
            lambda m: f"{m.group(1)} 자료형은 인덱싱([])이 지원되지 않습니다.",
        ),
    ]

    for pattern, summary, explain in patterns:
        m = re.search(pattern, msg)
        if m:
            return kor_err_name + f" - {summary}", explain(m)

    return (
        kor_err_name,
        "존재하지 않는 속성에 접근했습니다.\n객체나 변수의 자료형과 사용 가능한 속성을 확인하세요.",
    )
