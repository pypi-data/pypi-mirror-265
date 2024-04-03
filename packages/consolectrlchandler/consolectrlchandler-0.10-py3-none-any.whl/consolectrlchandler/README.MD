# handler for CTRL_C_EVENT, CTRL_BREAK_EVENT, CTRL_CLOSE_EVENT, CTRL_LOGOFF_EVENT, CTRL_SHUTDOWN_EVENT

## Tested against Windows 10 / Python 3.11 / Anaconda

### pip install consolectrlhandler



```py
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


    test
    test
    ctrl handler 0
    test
    ctrl handler 0
    ctrl handler 0
    ctrl handler 0
    ctrl handler 0
    test
    ctrl handler 0
    test
    test
```