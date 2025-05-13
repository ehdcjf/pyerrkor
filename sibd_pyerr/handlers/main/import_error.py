from sibd_pyerr.registry import register
import re


@register("ImportError")
def handle_import_error(exc_type, exc_value):
    kor_err_name = "임포트 오류"
    msg = str(exc_value)

    patterns = [
        (
            r"cannot import name '(\w+)' from '([\w.]+)'",
            "이름 임포트 실패",
            lambda m: (
                f"'{m.group(2)}' 모듈에는 '{m.group(1)}'이라는 이름이 없습니다.\n"
                f"해당 함수/클래스가 존재하는지, 버전에 따라 달라지지 않았는지 확인하세요."
            ),
        ),
        (
            r"attempted relative import with no known parent package",
            "상대 임포트 실패",
            lambda m: (
                "상대 경로 import를 사용할 수 없습니다.\n"
                "스크립트를 직접 실행하면 상대 경로는 동작하지 않으니, 패키지로 실행하거나 절대 경로를 사용하세요."
            ),
        ),
        (
            r"cannot import '(\w+)'",
            "불완전한 임포트",
            lambda m: (
                f"'{m.group(1)}'를 임포트할 수 없습니다.\n"
                f"모듈 설치 문제이거나, 파이썬 버전에 따라 지원되지 않을 수 있습니다."
            ),
        ),
    ]

    for pattern, summary, explain in patterns:
        m = re.search(pattern, msg)
        if m:
            return kor_err_name + f" - {summary}", explain(m)

    return (
        kor_err_name,
        "모듈에서 항목을 임포트할 수 없습니다.\n이름이 존재하는지, 의존성이 충족되었는지 확인하세요.",
    )
