import os
import json
from ctypes_window_info import get_window_infos
from typing import Union
import re
from mousekey import MouseKey
import subprocess

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}

def create_dummy_macro(
    macroname="pythonclickautomation",
    bluestacks_programm_data=r"C:\ProgramData\BlueStacks_nxt",
    shortcut="F12",
):
    r"""
    Create a dummy macro for automation.

    Args:
        macroname (str, optional): The name of the macro. Defaults to "pythonclickautomation".
        bluestacks_programm_data (str, optional): The path to BlueStacks data directory. Defaults to r"C:\ProgramData\BlueStacks_nxt".
        shortcut (str, optional): The keyboard shortcut for the macro. Defaults to "F12".

    Returns:
        str: The path to the created macro script.
    """
    userscriptfolder = os.path.join(
        bluestacks_programm_data, r"Engine\UserData\InputMapper\UserScripts"
    )

    bstacksjson = os.path.join(userscriptfolder, r"MetaData.json")

    pythonautoscript = os.path.join(userscriptfolder, f"{macroname}.json")
    if os.path.exists(pythonautoscript):
        print(f"{pythonautoscript} already exists")
        return pythonautoscript

    automationfile = {
        "Events": [
            {
                "Delta": 0,
                "EventType": "MouseDown",
                "Timestamp": 100,
                "X": 11.11111111111111,
                "Y": 18.75,
            },
            {
                "Delta": 0,
                "EventType": "MouseUp",
                "Timestamp": 200,
                "X": 11.11111111111111,
                "Y": 18.75,
            },
        ]
    }
    with open(pythonautoscript, mode="w", encoding="utf-8") as f:
        json.dump(automationfile, f)

    if os.path.exists(bstacksjson):
        with open(bstacksjson) as f:
            data = json.load(f)
        data["Macros"].append(
            {
                "Acceleration": 1,
                "CreationTime": "20240319T144005",
                "DoNotShowWindowOnFinish": True,
                "LoopDuration": 0,
                "LoopInterval": 0,
                "LoopIterations": 1,
                "LoopType": "TillLoopNumber",
                "MergeConfigurations": [],
                "Name": macroname,
                "RestartPlayer": False,
                "RestartPlayerAfterMinutes": 60,
                "Shortcut": shortcut,
                "StopOnHomeScreen": False,
            }
        )

        newid = data["NextMacroId"]
        data["NextMacroId"] += 1

        data["Organization"].append(
            {
                "ID": newid,
                "IsFolder": False,
                "IsOpen": False,
                "IsVisible": False,
                "Name": macroname,
                "Order": 1,
                "ParentFolder": -1,
            }
        )
    else:
        data = {
            "MacroSchemaVersion": 3,
            "Macros": [
                {
                    "Acceleration": 1,
                    "CreationTime": "20240319T144005",
                    "DoNotShowWindowOnFinish": True,
                    "LoopDuration": 0,
                    "LoopInterval": 0,
                    "LoopIterations": 1,
                    "LoopType": "TillLoopNumber",
                    "MergeConfigurations": [],
                    "Name": macroname,
                    "RestartPlayer": False,
                    "RestartPlayerAfterMinutes": 60,
                    "Shortcut": shortcut,
                    "StopOnHomeScreen": False,
                }
            ],
            "NextMacroId": 2,
            "Organization": [
                {
                    "ID": 1,
                    "IsFolder": False,
                    "IsOpen": False,
                    "IsVisible": False,
                    "Name": macroname,
                    "Order": 1,
                    "ParentFolder": -1,
                }
            ],
            "TabIndex": 0,
        }

    with open(bstacksjson, mode="w", encoding="utf-8") as f:
        json.dump(data, f)
    print("Restart Bluestacks!")
    return pythonautoscript


def get_resolution(instance, bluestacks_programm_data=r"C:\ProgramData\BlueStacks_nxt"):
    r"""
    Get the screen resolution of a BlueStacks instance.

    Args:
        instance (str): The BlueStacks instance name.
        bluestacks_programm_data (str, optional): The path to BlueStacks data directory. Defaults to r"C:\ProgramData\BlueStacks_nxt".

    Returns:
        Tuple[int, int]: The screen width and height of the BlueStacks instance.
    """
    bststackcfg = os.path.join(bluestacks_programm_data, "bluestacks.conf")

    with open(bststackcfg, "r", encoding="utf-8") as f:
        data = f.read()

    datalines = data.splitlines()
    screen_height_emulator = None
    screen_width_emulator = None
    for line in datalines:
        if f"{instance}.fb_height" in line:
            screen_height_emulator = int(line.split("=")[-1].strip(" '\""))
        if f"{instance}.fb_width" in line:
            screen_width_emulator = int(line.split("=")[-1].strip(" '\""))

    return screen_width_emulator, screen_height_emulator


class NoAdbClick:
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
    def __init__(
        self,
        pid: int,
        macroname: str = "pythonclickautomation",
        click_duration_ms: int = 1000,
        start_ms: int = 100,
        macro_shortcut: str = "F12",
        screen_width_emulator: Union[int, None] = None,
        screen_height_emulator: Union[int, None] = None,
        failsafe: Union[str, None] = None,
        with_spaces: bool = True,
        with_tabs: bool = True,
        with_newlines: bool = True,
        activate_window_before: bool = False,
        bluestacks_programm_data: str = r"C:\ProgramData\BlueStacks_nxt",
    ):
        if not re.match(r"^F\d+$", macro_shortcut):
            raise ValueError("Shortcut must be a F-key (F10,F12...)")
        json_of_already_created_dummy_macro = create_dummy_macro(
            macroname=macroname,
            bluestacks_programm_data=bluestacks_programm_data,
            shortcut=macro_shortcut,
        )

        self.mkey = MouseKey()
        if failsafe:
            self.mkey.enable_failsafekill(failsafe)

        self.bstacksdata = search_bluestacks_instances(emulator_search=pid)
        self.hwnd = self.bstacksdata[pid]["keymap"]["hwnd"]
        self.with_spaces = with_spaces
        self.with_tabs = with_tabs
        self.with_newlines = with_newlines
        self.activate_window_before = activate_window_before

        self.screen_width_emulator = screen_width_emulator
        self.screen_height_emulator = screen_height_emulator
        self.instance_name = None
        if not self.screen_width_emulator or not self.screen_height_emulator:
            pro = subprocess.run(
                f"""wmic process where (ProcessId={pid}) get CommandLine""",
                capture_output=True,
                **invisibledict,
            )
            self.instance_name = (
                pro.stdout.strip().split()[-1].strip(b"'\"").decode("utf-8")
            )
            self.screen_width_emulator, self.screen_height_emulator = get_resolution(
                self.instance_name,
                bluestacks_programm_data=bluestacks_programm_data,
            )
        self.click_duration_ms = click_duration_ms
        self.start_ms = start_ms
        self.macro_shortcut = f"{{VK_{macro_shortcut}}}"
        self.pythonmacrojson = json_of_already_created_dummy_macro


    def input_tap(self, x:int, y:int, **kwargs):
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
        self.with_spaces = kwargs.get("with_spaces", self.with_spaces)
        self.with_tabs = kwargs.get("with_tabs", self.with_tabs)
        self.with_newlines = kwargs.get("with_newlines", self.with_newlines)
        self.activate_window_before = kwargs.get(
            "activate_window_before", self.activate_window_before
        )
        json_of_already_created_dummy_macro = kwargs.get(
            "json_of_already_created_dummy_macro", self.pythonmacrojson
        )
        screen_width_emulator = kwargs.get(
            "screen_width_emulator", self.screen_width_emulator
        )
        screen_height_emulator = kwargs.get(
            "screen_height_emulator", self.screen_height_emulator
        )
        click_duration_ms = kwargs.get("click_duration_ms", self.click_duration_ms)
        start_ms = kwargs.get("start_ms", self.start_ms)
        macro_shortcut = kwargs.get("macro_shortcut", self.macro_shortcut)
        ev = {
            "Events": [
                {
                    "Delta": 0,
                    "EventType": "MouseDown",
                    "Timestamp": start_ms,
                    "X": (x / screen_width_emulator) * 100,
                    "Y": (y / screen_height_emulator) * 100,
                },
                {
                    "Delta": 0,
                    "EventType": "MouseUp",
                    "Timestamp": click_duration_ms + start_ms,
                    "X": (x / screen_width_emulator) * 100,
                    "Y": (y / screen_height_emulator) * 100,
                },
            ]
        }
        with open(json_of_already_created_dummy_macro, "w", encoding="utf-8") as f:
            f.write(json.dumps(ev))

        if self.mkey.block_user_input():
            try:
                self.mkey.send_keystrokes_to_hwnd(
                    handle=self.hwnd,
                    keystrokes=macro_shortcut,
                    with_spaces=True,
                    with_tabs=True,
                    with_newlines=True,
                    activate_window_before=False,
                )
            finally:
                self.mkey.unblock_user_input()


def search_bluestacks_instances(
    emulator_search: Union[re.Pattern, int, type(None)] = None,
):
    wind = get_window_infos()
    allfoundemulators = []
    if isinstance(emulator_search, re.Pattern):
        for w in wind:
            if "hd-player.exe" in w.path.lower():
                if emulator_search.search(w.windowtext) and w.title.startswith(
                    "Qt5154QWindowOwn"
                ):
                    allfoundemulators.append(w)
    elif isinstance(emulator_search, int):
        for w in wind:
            if "hd-player.exe" in w.path.lower():
                if w.pid == emulator_search and w.title.startswith("Qt5154QWindowOwn"):
                    allfoundemulators.append(w)
    elif isinstance(emulator_search, type(None)):
        for w in wind:
            if "hd-player.exe" in w.path.lower() and w.title.startswith(
                "Qt5154QWindowOwn"
            ):
                allfoundemulators.append(w)

    keymaps = {}
    for w in allfoundemulators:
        for w_ in wind:
            if w_.pid == w.pid and "Keymap" in w_.windowtext:
                keymaps[w_.pid] = {"main_window": w._asdict(), "keymap": w_._asdict()}

    return keymaps


