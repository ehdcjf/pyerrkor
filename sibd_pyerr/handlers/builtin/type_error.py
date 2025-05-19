from sibd_pyerr.registry import register
import traceback
import re


# 타입에러는 좀 심화해서 구현할 필요 있음
@register("TypeError")
def _handle_type_error(exc_type, exc_value):
    kor_err_name = "타입 오류"
    msg = str(exc_value)
    kor_err_message = "자료형이 맞지 않아 연산할 수 없습니다."

    m_concat = re.search(r'can only concatenate (\w+) \(not "(\w+)"\) to \1', msg)

    # 1. concatenate
    if m_concat:
        expected, actual = m_concat.groups()
        return (
            "타입 오류",
            f"{expected} 자료형끼리만 + 연산이 가능합니다. (지금은 {actual} 자료형이 섞여 있습니다.)",
        )

    # 2. unsupported operand type
    m_unsupported = re.search(
        r"unsupported operand type\(s\) for ([+\-*/%]): '(\w+)' and '(\w+)'", msg
    )

    if m_unsupported:
        operator, left, right = m_unsupported.groups()
        return (
            "타입 오류",
            f"{left} 자료형은 {right} 자료형과 '{operator}' 연산이 지원되지 않습니다.",
        )

    # 3. missing required argument
    m_missing = re.search(r"missing (\d+) required positional argument[s]?: (.+)", msg)
    if m_missing:
        count, args = m_missing.groups()
        return kor_err_name, f"{count}개의 인자가 부족합니다: {args}"

    # 4. too many arguments
    m_too_many = re.search(
        r"takes (\d+) positional argument[s]? but (\d+) were given", msg
    )
    if m_too_many:
        expected, given = m_too_many.groups()
        return kor_err_name, (
            f"함수는 {expected}개의 인자만 받을 수 있지만, {given}개가 전달되었습니다."
        )

    # 5. not callable
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

    # 6. not subscriptable
    m_subscript = re.search(r"'(\w+)' object is not subscriptable", msg)
    if m_subscript:
        t = m_subscript.group(1)
        return kor_err_name, f"{t} 자료형은 인덱싱이 지원되지 않습니다."

    # 7. not iterable
    m_iter = re.search(r"'(\w+)' object is not iterable", msg)
    if m_iter:
        t = m_iter.group(1)
        return kor_err_name, f"{t} 자료형은 반복문(for문 등)에서 사용할 수 없습니다."

    # 8. has no len()
    m_len = re.search(r"object of type '(\w+)' has no len\(\)", msg)
    if m_len:
        t = m_len.group(1)
        return kor_err_name, f"{t} 자료형은 len() 함수를 사용할 수 없습니다."

    # 9. 비교 불가
    m_compare = (
        re.search(r"'(\w+)' and '(\w+)'", msg)
        if "not supported between instances of" in msg
        else None
    )
    if m_compare:
        left, right = m_compare.groups()
        return kor_err_name, (
            f"{left} 자료형과 {right} 자료형은 비교 연산(<, > 등)이 지원되지 않습니다."
        )
    # 'X' object is not iterable
    m_iter = re.search(r"'(\w+)' object is not iterable", msg)
    if m_iter:
        t = m_iter.group(1)
        return kor_err_name, f"{t} 자료형은 반복문(for문 등)에서 사용할 수 없습니다."

    # 'X' object is not reversible
    m_reverse = re.search(r"'(\w+)' object is not reversible", msg)
    if m_reverse:
        t = m_reverse.group(1)
        return kor_err_name, f"{t} 자료형은 reversed() 함수에 사용할 수 없습니다."

    # abs
    m_abs = re.search(r"bad operand type for abs\(\): '(\w+)'", msg)
    if m_abs:
        t = m_abs.group(1)
        return kor_err_name, f"{t} 자료형은 abs() 함수에 사용할 수 없습니다."

    # 단항 + - ~
    m_unary = re.search(r"bad operand type for unary ([+\-~]): '(\w+)'", msg)
    if m_unary:
        op, t = m_unary.groups()
        op_map = {"-": "음수(-)", "+": "단항 +", "~": "비트 NOT(~)"}
        return kor_err_name, f"{t} 자료형은 {op_map[op]} 연산이 지원되지 않습니다."

    # isinstance arg type 오류
    m_instance = re.search(r"isinstance\(\) arg 2 must be a type", msg)
    if m_instance:
        return (
            kor_err_name,
            "isinstance()의 두 번째 인자는 타입 또는 타입의 튜플이어야 합니다. (예: int 또는 (int, str))",
        )

    # format 함수에 부적절한 타입 사용
    m_format = re.search(r"unsupported format string passed to (\w+)\.__format__", msg)
    if m_format:
        t = m_format.group(1)
        return kor_err_name, f"{t} 자료형은 format() 함수에 사용할 수 없습니다."

    # fallback
    return kor_err_name, kor_err_message
