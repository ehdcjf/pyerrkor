from sibd_pyerr.registry import register
import re
import difflib


@register("ModuleNotFoundError")
def handle_module_not_found_error(exc_type, exc_value):
    kor_err_name = "모듈 찾기 오류"
    msg = str(exc_value)

    m = re.search(r"No module named '(.*?)'", msg)
    if not m:
        return kor_err_name, "존재하지 않는 모듈을 임포트하려 했습니다."

    modname = m.group(1)

    # 오타 감지용 표준 모듈 일부 리스트
    std_modules = [
        "math",
        "datetime",
        "sys",
        "os",
        "json",
        "re",
        "time",
        "random",
        "collections",
        "itertools",
        "functools",
        "subprocess",
        "threading",
        "multiprocessing",
        "typing",
        "asyncio",
        "statistics",
        "heapq",
        "pathlib",
        "copy",
        "traceback",
        "unittest",
        "csv",
        "argparse",
        "logging",
        "decimal",
        "fractions",
        "email",
        "http",
        "tkinter",
    ]

    suggestion = difflib.get_close_matches(modname, std_modules, n=1, cutoff=0.75)
    if suggestion:
        return kor_err_name, (
            f"'{modname}' 모듈은 존재하지 않습니다.\n"
            f"혹시 '{suggestion[0]}' 모듈을 잘못 입력하신 건 아닌가요?"
        )

    return kor_err_name, (
        f"'{modname}' 모듈은 존재하지 않습니다.\n"
        f"모듈 이름의 철자가 맞는지 확인하세요."
    )
