
# like input tap for BlueStacks instances, but without using ADB

## pip install bstacksnoadbclick

### Tested against Windows 10 / Python 3.11 / Anaconda / BlueStacks5


```PY
from bstacksnoadbclick import NoAdbClick

r"""
Class for performing clicks on BlueStacks instances without using ADB.
It creates a dummy macro and runs it (method: input_tap) using direct keystrokes (admin rights!!) to the BlueStacks window (hwnd) to activate it.

Args:
    pid (int): Process ID of the BlueStacks instance.
    macroname (str, optional): The name of the macro. Defaults to "pythonclickautomation".
    click_duration_ms (int, optional): Duration of the click in milliseconds. Defaults to 1000.
    start_ms (int, optional): Start time of the click in milliseconds. Defaults to 100.
    macro_shortcut (str, optional): Keyboard shortcut for the macro. Defaults to "F12".
    screen_width_emulator (Union[int, None], optional): Screen width of the emulator. Defaults to None.
    screen_height_emulator (Union[int, None], optional): Screen height of the emulator. Defaults to None.
    failsafe (Union[str, None], optional): Fail-safe key combination to prevent infinite loops. Defaults to None.
    with_spaces (bool, optional): Include spaces in keystrokes. Defaults to True.
    with_tabs (bool, optional): Include tabs in keystrokes. Defaults to True.
    with_newlines (bool, optional): Include newlines in keystrokes. Defaults to True.
    activate_window_before (bool, optional): Activate window before sending keystrokes. Defaults to False.
    bluestacks_programm_data (str, optional): Path to BlueStacks data directory. Defaults to r"C:\ProgramData\BlueStacks_nxt".

Raises:
    ValueError: If the shortcut is not in F-key format (e.g., F10, F12).
"""


self = NoAdbClick(
    pid=22240,
    macroname="pythonclickautomation",
    click_duration_ms=1000,
    start_ms=100,
    macro_shortcut="F12",
    screen_width_emulator=None,
    screen_height_emulator=None,
    failsafe=None,
    with_spaces=True,
    with_tabs=True,
    with_newlines=True,
    activate_window_before=False,
    bluestacks_programm_data=r"C:\ProgramData\BlueStacks_nxt",
)

r"""
Perform a tap input at the specified coordinates.

Args:
    x (int): X-coordinate of the tap.
    y (int): Y-coordinate of the tap.
    **kwargs: Additional keyword arguments for customization.

Keyword Args:
    with_spaces (bool): Include spaces in keystrokes.
    with_tabs (bool): Include tabs in keystrokes.
    with_newlines (bool): Include newlines in keystrokes.
    activate_window_before (bool): Activate window before sending keystrokes.
    json_of_already_created_dummy_macro (str): Path to the already created macro JSON file.
    screen_width_emulator (int): Screen width of the emulator.
    screen_height_emulator (int): Screen height of the emulator.
    click_duration_ms (int): Duration of the click in milliseconds.
    start_ms (int): Start time of the click in milliseconds.
    macro_shortcut (str): Keyboard shortcut for the macro.
"""
self.input_tap(300, 1000, click_duration_ms=10, start_ms=1)
```
