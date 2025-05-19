from sibd_pyerr.registry import register
import traceback
import re


@register("TypeError")
def _handle_type_error(exc_type, exc_value):
    kor_err_name = "타입 오류"
    msg = str(exc_value)

    patterns = [
        {
            "pattern": r'can only concatenate (\w+) \(not "(\w+)"\) to \1',
            "message": lambda m: f"{m.group(1)} 자료형끼리만 + 연산이 가능합니다. (지금은 {m.group(2)} 자료형이 섞여 있습니다.)",
        },
        {
            "pattern": r"unsupported operand type\(s\) for ([+\-*/%]): '(\w+)' and '(\w+)'",
            "message": lambda m: f"{m.group(2)} 자료형은 {m.group(3)} 자료형과 '{m.group(1)}' 연산이 지원되지 않습니다.",
        },
        {
            "pattern": r"missing (\d+) required positional argument[s]?: (.+)",
            "message": lambda m: f"{m.group(1)}개의 인자가 부족합니다: {m.group(2)}",
        },
        {
            "pattern": r"takes (\d+) positional argument[s]? but (\d+) were given",
            "message": lambda m: f"함수는 {m.group(1)}개의 인자만 받을 수 있지만, {m.group(2)}개가 전달되었습니다.",
        },
        {
            "pattern": r"'(\w+)' object is not subscriptable",
            "message": lambda m: f"{m.group(1)} 자료형은 인덱싱이 지원되지 않습니다. ",
        },
        {
            "pattern": r"'(\w+)' object is not iterable",
            "message": lambda m: f"{m.group(1)} 자료형은 반복문(for문 등)에서 사용할 수 없습니다.",
        },
        {
            "pattern": r"'(\w+)' object is not reversible",
            "message": lambda m: f"{m.group(1)} 자료형은 reversed() 함수에 사용할 수 없습니다.",
        },
        {
            "pattern": r"bad operand type for abs\(\): '(\w+)'",
            "message": lambda m: f"{m.group(1)} 자료형은 abs() 함수에 사용할 수 없습니다.",
        },
        {
            "pattern": r"bad operand type for unary ([+\-~]): '(\w+)'",
            "message": lambda m: {"-": "음수(-)", "+": "단항 +", "~": "비트 NOT(~)"}[
                m.group(1)
            ]
            + f" 연산은 {m.group(2)} 자료형에 대해 지원되지 않습니다.",
        },
        {
            "pattern": r"isinstance\(\) arg 2 must be a type",
            "message": lambda m: "isinstance()의 두 번째 인자는 타입 또는 타입의 튜플이어야 합니다. (예: int 또는 (int, str))",
        },
        {
            "pattern": r"unsupported format string passed to (\w+)\.__format__",
            "message": lambda m: f"{m.group(1)} 자료형은 format() 함수에 사용할 수 없습니다.",
        },
        {
            "pattern": r"'(\w+)' and '(\w+)'",
            "condition": lambda msg: "not supported between instances of" in msg,
            "message": lambda m: f"{m.group(1)} 자료형과 {m.group(2)} 자료형은 비교 연산(<, > 등)이 지원되지 않습니다.",
        },
    ]

    for p in patterns:
        if "condition" in p and not p["condition"](msg):
            continue
        m = re.search(p["pattern"], msg)
        if m:
            return kor_err_name, p["message"](m)

    # 특수 case: not callable → traceback 사용
    if "object is not callable" in msg:
        tb = traceback.extract_tb(exc_value.__traceback__)
        code_lines = [frame.line for frame in tb if frame.line]
        if any("print" in line for line in code_lines):
            return kor_err_name, (
                "print 함수를 덮어썼습니다. 커널을 재시작하거나 del print 후 다시 시도하세요."
            )
        return (
            kor_err_name,
            "함수가 아닌 값을 호출하려 했습니다.",
        )

    return kor_err_name, "자료형이 맞지 않아 연산할 수 없습니다."
