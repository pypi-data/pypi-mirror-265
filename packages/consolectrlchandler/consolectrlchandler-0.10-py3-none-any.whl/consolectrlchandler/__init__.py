from ctypes import WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, DWORD
import sys

ctrl_config = sys.modules[__name__]
ctrl_config.function = lambda *args, **kwargs: None

kernel32 = windll.LoadLibrary("kernel32")
PHANDLER_ROUTINE = WINFUNCTYPE(BOOL, DWORD)
SetConsoleCtrlHandler = kernel32.SetConsoleCtrlHandler
SetConsoleCtrlHandler.argtypes = (PHANDLER_ROUTINE, BOOL)
SetConsoleCtrlHandler.restype = BOOL

(
    CTRL_C_EVENT,
    CTRL_BREAK_EVENT,
    CTRL_CLOSE_EVENT,
    CTRL_LOGOFF_EVENT,
    CTRL_SHUTDOWN_EVENT,
) = 0, 1, 2, 3, 4
continue_proc = True


def disable_con_proc():
    print("kill: {}".format(continue_proc))


@PHANDLER_ROUTINE
def console_handler(ctrl_type):
    r"""
    Console Control Handler for Windows

    This module provides functionality for handling console control events in Windows,
    namely CTRL_C_EVENT, CTRL_BREAK_EVENT, CTRL_CLOSE_EVENT, CTRL_LOGOFF_EVENT, CTRL_SHUTDOWN_EVENT

        Args:
            ctrl_type (int): The type of control event.

        Returns:
            bool: True if the event is handled; False otherwise.

        Example:
            To use this module, import it and set your desired function as the console handler:

            >>> from consolectrlhandler import ctrl_config

            Define your custom function to handle console control events:

            >>> def ctrl_handler(ctrl_type):
            ...     print(f"Received control event: {ctrl_type}")

            Assign your custom function as the console handler:

            >>> ctrl_config.function = ctrl_handler

            Then run your main program loop.

            # Complete code
            from consolectrlchandler import ctrl_config
            import time

            def ctrlhandler(ctrl_type):
                print(f"ctrl handler {ctrl_type}")

            ctrl_config.function = ctrlhandler
            while True:
                print("test")
                time.sleep(1)
    """
    if ctrl_type in (
        CTRL_C_EVENT,
        CTRL_BREAK_EVENT,
        CTRL_CLOSE_EVENT,
        CTRL_LOGOFF_EVENT,
        CTRL_SHUTDOWN_EVENT,
    ):
        ctrl_config.function(ctrl_type=ctrl_type)
        return True
    return False


if not SetConsoleCtrlHandler(console_handler, True):
    raise RuntimeError("SetConsoleCtrlHandler failed.")
