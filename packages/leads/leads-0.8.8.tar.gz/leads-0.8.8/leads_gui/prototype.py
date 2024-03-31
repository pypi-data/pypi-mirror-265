from math import lcm as _lcm
from typing import Callable as _Callable, Self as _Self, TypeVar as _TypeVar, Generic as _Generic

from PIL import ImageTk as _ImageTk
from customtkinter import CTk as _CTk, get_appearance_mode as _get_appearance_mode

from leads_gui.runtime import RuntimeData
from leads_gui.system import _ASSETS_PATH, get_system_platform
from leads_gui.types import Widget as _Widget, Color as _Color

T = _TypeVar("T", bound=RuntimeData)


class Window(_Generic[T]):
    def __init__(self,
                 width: int,
                 height: int,
                 refresh_rate: int,
                 runtime_data: T,
                 on_refresh: _Callable[[_Self], None] = lambda _: None,
                 title: str = "LEADS",
                 fullscreen: bool = True,
                 no_title_bar: bool = True) -> None:
        self._root: _CTk = _CTk()
        self._root.title(title)
        self._root.wm_iconbitmap()
        self._root.iconphoto(True, _ImageTk.PhotoImage(file=_ASSETS_PATH + "/logo.png"))
        self._root.overrideredirect(no_title_bar)
        self._width: int = self._root.winfo_screenwidth() if fullscreen else width
        self._height: int = self._root.winfo_screenheight() if fullscreen else height
        self._root.geometry(str(self._width) + "x" + str(self._height))
        self._refresh_rate: int = refresh_rate
        self._refresh_interval: int = int(1000 / refresh_rate)
        self._runtime_data: T = runtime_data
        self._on_refresh: _Callable[[Window], None] = on_refresh

        self._active: bool = False

    def root(self) -> _CTk:
        return self._root

    def width(self) -> int:
        return self._width

    def height(self) -> int:
        return self._height

    def refresh_rate(self) -> int:
        return self._refresh_rate

    def runtime_data(self) -> T:
        return self._runtime_data

    def set_on_refresh(self, on_refresh: _Callable[[_Self], None]) -> None:
        self._on_refresh = on_refresh

    def active(self) -> bool:
        return self._active

    def show(self) -> None:
        self._active = True

        def wrapper() -> None:
            self._on_refresh(self)
            if self._active:
                self._root.after(self._refresh_interval, wrapper)

        self._root.after(0, wrapper)
        self._root.mainloop()

    def kill(self) -> None:
        self._active = False
        self._root.destroy()


class ContextManager(object):
    def __init__(self, window: Window) -> None:
        self._window: Window = window
        self._widgets: dict[str, _Widget] = {}
        self._system_platform: str = get_system_platform()

    def __setitem__(self, key: str, widget: _Widget) -> None:
        self._widgets[key] = widget

    def __getitem__(self, key: str) -> _Widget:
        return self._widgets[key]

    def system_platform(self) -> str:
        return self._system_platform

    def set(self, key: str, widget: _Widget) -> None:
        self[key] = widget

    def get(self, key: str) -> _Widget:
        return self[key]

    def parse_layout(self, layout: list[list[str | _Widget]]) -> list[list[_Widget]]:
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                e = layout[i][j]
                if isinstance(e, str):
                    layout[i][j] = self[e]
        return layout

    def layout(self, layout: list[list[str | _Widget]]) -> None:
        layout = self.parse_layout(layout)
        self.root().grid_columnconfigure(tuple(range(t := _lcm(*map(len, layout)))), weight=1)
        for i in range(len(layout)):
            row = layout[i]
            length = len(row)
            for j in range(length):
                s = int(t / length)
                row[j].grid(row=i, column=j * s, sticky="NSEW", columnspan=s, ipadx=4, ipady=4, padx=4, pady=4)

    def window(self) -> Window:
        return self._window

    def rd(self) -> T:
        return self._window.runtime_data()

    def active(self) -> bool:
        return self._window.active()

    def root(self) -> _CTk:
        return self._window.root()

    def show(self) -> None:
        self._window.show()

    def kill(self) -> None:
        self._window.kill()


def parse_color(color: _Color) -> str:
    return color if isinstance(color, str) else color[0] if _get_appearance_mode() == "Light" else color[1]
