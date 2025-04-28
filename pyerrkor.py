import sys
from IPython.display import HTML, display


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
    "ZeroDivisionError": "0으로 나누기를 시도했습니다.",
    "NameError": "정의되지 않은 변수를 사용했습니다.",
    "TypeError": "자료형이 맞지 않아 연산할 수 없습니다.",
    "IndexError": "리스트나 문자열 인덱스를 잘못 사용했습니다.",
    "KeyError": "딕셔너리에 존재하지 않는 키를 사용했습니다.",
}


# 기본 에러 핸들러
def custom_handler(exc_type, exc_value, exc_traceback):
    error_name = exc_type.__name__
    kor_error_name = KOR_ERROR_NAME.get(error_name, "정의되지 않은 에러")
    msg = error_messages.get(error_name, f"{error_name}")
    print(f"\033[91m{kor_error_name}\033[0m: {msg}\n")
    # 원래 에러 출력
    import traceback

    traceback.print_exception(exc_type, exc_value, exc_traceback)


# 주피터 노트북용 핸들러
def ipython_handler(shell, exc_type, exc_value, exc_traceback, tb_offset=None):
    error_name = exc_type.__name__
    kor_error_name = KOR_ERROR_NAME.get(error_name, "정의되지 않은 에러")
    msg = error_messages.get(error_name, f"{error_name}")
    display(HTML(f'<span style="color:magenta;">{kor_error_name}</span>: {msg}\n'))
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
