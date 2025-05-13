import sys
from .registry import get_kor_error_info
from .display.cli import print_cli_error
from .display.jupyter import display_jupyter_error
from .handlers import *  # 모든 핸들러 등록


def custom_handler(exc_type, exc_value, exc_traceback):
    name, msg = get_kor_error_info(exc_type, exc_value)
    print_cli_error(name, msg)
    import traceback

    traceback.print_exception(exc_type, exc_value, exc_traceback)


def ipython_handler(shell, exc_type, exc_value, exc_traceback, tb_offset=None):
    name, msg = get_kor_error_info(exc_type, exc_value)
    display_jupyter_error(name, msg)
    shell.showtraceback((exc_type, exc_value, exc_traceback), tb_offset=tb_offset)


def install():
    try:
        from IPython import get_ipython

        shell = get_ipython()
        if shell:
            shell.set_custom_exc((Exception,), ipython_handler)
            return
    except ImportError:
        pass
    sys.excepthook = custom_handler
