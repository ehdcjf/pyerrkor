import sys
from IPython.display import HTML, display
import re


# (주피터 노트북 탐지용)
def in_ipython():
    try:
        from IPython import get_ipython

        return get_ipython() is not None
    except ImportError:
        return False


KOR_ERROR_NAME = {
    "ArithmeticError": "",
    "AssertionError": "AssertionError",
    "AttributeError": "객체_에러",
    "BaseException": "",
    "BaseExceptionGroup": "",
    "BlockingIOError": "",
    "BrokenPipeError": "",
    "BufferError": "",
    "BytesWarning": "",
    "ChildProcessError": "",
    "ConnectionAbortedError": "",
    "ConnectionError": "",
    "ConnectionRefusedError": "",
    "ConnectionResetError": "",
    "DeprecationWarning": "",
    "EOFError": "",
    "EncodingWarning": "",
    "EnvironmentError": "",
    "Exception": "",
    "ExceptionGroup": "",
    "FileExistsError": "",
    "FileNotFoundError": "파일없음_에러",
    "FloatingPointError": "",
    "FutureWarning": "",
    "GeneratorExit": "",
    "IOError": "",
    "ImportError": "불러오기_에러",
    "ImportWarning": "",
    "IndentationError": "들여쓰기_에러",
    "IndexError": "인덱스_에러",
    "InterruptedError": "",
    "IsADirectoryError": "",
    "KeyError": "키_에러",
    "KeyboardInterrupt": "",
    "LookupError": "",
    "MemoryError": "메모리_에러",
    "ModuleNotFoundError": "모듈_불러오기_에러",
    "NameError": "변수명_에러",
    "NotADirectoryError": "",
    "NotImplementedError": "",
    "OSError": "운영체제_에러",
    "OverflowError": "",
    "PendingDeprecationWarning": "",
    "PermissionError": "",
    "ProcessLookupError": "",
    "PythonFinalizationError": "",
    "RecursionError": "재귀_에러",
    "ReferenceError": "",
    "ResourceWarning": "",
    "RuntimeError": "런타임_에러",
    "RuntimeWarning": "",
    "StopAsyncIteration": "",
    "StopIteration": "",
    "SyntaxError": "문법_에러",
    "SyntaxWarning": "",
    "SystemError": "",
    "SystemExit": "",
    "TabError": "탭_에러",
    "TimeoutError": "",
    "TypeError": "자료형_에러",
    "UnboundLocalError": "",
    "UnicodeDecodeError": "",
    "UnicodeEncodeError": "",
    "UnicodeError": "",
    "UnicodeTranslateError": "",
    "UnicodeWarning": "",
    "UserWarning": "",
    "ValueError": "값_에러",
    "Warning": "",
    "WindowsError": "",
    "ZeroDivisionError": "0으로_나누기_에러",
    "_IncompleteInputError": "",
}


# 한글 에러 메시지 매칭
error_messages = {
    "IndexError": "리스트나 문자열 인덱스를 잘못 사용했습니다.",
    "KeyError": "딕셔너리에 존재하지 않는 키를 사용했습니다.",
}

_handlers: dict[str, callable] = {}


def register(error_name: str):
    """에러이름을 키로 핸들러 함수 등록"""

    def decorator(fn: callable):
        _handlers[error_name] = fn
        return fn

    return decorator


def get_kor_error_info(exc_type, exc_value):
    err_name = exc_type.__name__
    if err_name in _handlers:
        return _handlers[err_name](exc_type, exc_value)
    return ("정의되지 않은 에러", str(exc_value))


@register("NameError")
def _handle_name_error(exc_type, exc_value):
    kor_err_name = "이름 오류"
    m = re.search(r"name '(.+?)' is not defined", str(exc_value))
    var = m.group(1) if m else ""
    kor_err_message = f"정의되지 않은 변수 '{var}'를 사용했습니다."
    return (kor_err_name, kor_err_message)


@register("ZeroDivisionError")
def _handle_zero_division_error(exc_type, exc_value):
    kor_err_name = "0나누기 오류"
    kor_err_message = "0으로 나누기를 시도했습니다."
    return (kor_err_name, kor_err_message)


@register("IndexError")
def _handle_index_error(exc_type, exc_value):
    kor_err_name = "인덱스 오류"
    kor_err_message = "인덱스를 잘못 사용했습니다."
    return (kor_err_name, kor_err_message)


@register("KeyError")
def _handle_key_error(exc_type, exc_value):
    kor_err_name = "키 오류"
    kor_err_message = "딕셔너리에 존재하지 않는 키를 사용했습니다."
    return (kor_err_name, kor_err_message)


# 타입에러는 좀 심화해서 구현할 필요 있음
@register("TypeError")
def _handle_type_error(exc_type, exc_value):
    kor_err_name = "타입 오류"
    kor_err_message = "자료형이 맞지 않아 연산할 수 없습니다."
    return (kor_err_name, kor_err_message)


# 기본 에러 핸들러
def custom_handler(exc_type, exc_value, exc_traceback):
    kor_error_name, kor_error_message = get_kor_error_info(exc_type, exc_value)
    print(f"\033[91m{kor_error_name}\033[0m: {kor_error_message}\n")
    # 원래 에러 출력
    import traceback

    traceback.print_exception(exc_type, exc_value, exc_traceback)


# 주피터 노트북용 핸들러
def ipython_handler(shell, exc_type, exc_value, exc_traceback, tb_offset=None):
    kor_error_name, kor_error_message = get_kor_error_info(exc_type, exc_value)
    display(
        HTML(
            f'<span style="color:magenta;">{kor_error_name}</span>: {kor_error_message}\n'
        )
    )

    # 원래 에러를 IPython 스타일로 출력
    shell.showtraceback((exc_type, exc_value, exc_traceback), tb_offset=tb_offset)
    return None


# 설치 함수
def install():
    if in_ipython():
        from IPython import get_ipython

        shell = get_ipython()
        shell.set_custom_exc((Exception,), ipython_handler)
    else:
        sys.excepthook = custom_handler
