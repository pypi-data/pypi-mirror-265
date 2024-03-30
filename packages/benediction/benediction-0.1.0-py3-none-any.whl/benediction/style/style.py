from __future__ import annotations

import curses
import typing
from dataclasses import dataclass, field, replace

from benediction.style.color import tailwind
from benediction.style.color._color import RGB, Color, Color_, ColorPair_

Attribute = typing.Literal[
    "alternate_character_set",
    "blink",
    "bold",
    "dim",
    "invisible",
    "italic",
    "normal",
    "protected_mode",
    "reverse_colors",
    "standout_mode",
    "underline_mode",
    "highlight_horizontal",
    "highlight_left",
    "highlight_low",
    "highlight_right",
    "highlight_top",
    "highlight_vertical",
]

_ATTRIBUTES: dict[Attribute, int] = {
    "alternate_character_set": curses.A_ALTCHARSET,
    "blink": curses.A_BLINK,
    "bold": curses.A_BOLD,
    "dim": curses.A_DIM,
    "invisible": curses.A_INVIS,
    "italic": curses.A_ITALIC,
    "normal": curses.A_NORMAL,
    "protected_mode": curses.A_PROTECT,
    "reverse_colors": curses.A_REVERSE,
    "standout_mode": curses.A_STANDOUT,
    "underline_mode": curses.A_UNDERLINE,
    "highlight_horizontal": curses.A_HORIZONTAL,
    "highlight_left": curses.A_LEFT,
    "highlight_low": curses.A_LOW,
    "highlight_right": curses.A_RIGHT,
    "highlight_top": curses.A_TOP,
    "highlight_vertical": curses.A_VERTICAL,
}


def _bitor(xs: typing.Iterable[int]):
    # bitwise or of all provided integers
    value = 0
    for x in xs:
        value |= x
    return value


def _default_to_parent(parent: Style, **kwargs):
    return {k: (getattr(parent, k) if v is None else v) for k, v in kwargs.items()}


class StyleKwargs(typing.TypedDict):
    # main style
    fg: typing.NotRequired[Color | RGB | tailwind.Color | None]
    bg: typing.NotRequired[Color | RGB | tailwind.Color | None]
    alternate_character_set: typing.NotRequired[bool | None]
    blink: typing.NotRequired[bool | None]
    bold: typing.NotRequired[bool | None]
    dim: typing.NotRequired[bool | None]
    invisible: typing.NotRequired[bool | None]
    italic: typing.NotRequired[bool | None]
    normal: typing.NotRequired[bool | None]
    protected_mode: typing.NotRequired[bool | None]
    reverse_colors: typing.NotRequired[bool | None]
    standout_mode: typing.NotRequired[bool | None]
    underline_mode: typing.NotRequired[bool | None]
    highlight_horizontal: typing.NotRequired[bool | None]
    highlight_left: typing.NotRequired[bool | None]
    highlight_low: typing.NotRequired[bool | None]
    highlight_right: typing.NotRequired[bool | None]
    highlight_top: typing.NotRequired[bool | None]
    highlight_vertical: typing.NotRequired[bool | None]


class WindowStyleKwargs(StyleKwargs, typing.TypedDict):
    # regular style kwargs + inner + window style kwargs
    inner_fg: typing.NotRequired[Color | RGB | tailwind.Color | None]
    inner_bg: typing.NotRequired[Color | RGB | tailwind.Color | None]
    win_fg: typing.NotRequired[Color | RGB | tailwind.Color | None]
    win_bg: typing.NotRequired[Color | RGB | tailwind.Color | None]
    win_alternate_character_set: typing.NotRequired[bool | None]
    win_blink: typing.NotRequired[bool | None]
    win_bold: typing.NotRequired[bool | None]
    win_dim: typing.NotRequired[bool | None]
    win_invisible: typing.NotRequired[bool | None]
    win_italic: typing.NotRequired[bool | None]
    win_normal: typing.NotRequired[bool | None]
    win_protected_mode: typing.NotRequired[bool | None]
    win_reverse_colors: typing.NotRequired[bool | None]
    win_standout_mode: typing.NotRequired[bool | None]
    win_underline_mode: typing.NotRequired[bool | None]
    win_highlight_horizontal: typing.NotRequired[bool | None]
    win_highlight_left: typing.NotRequired[bool | None]
    win_highlight_low: typing.NotRequired[bool | None]
    win_highlight_right: typing.NotRequired[bool | None]
    win_highlight_top: typing.NotRequired[bool | None]
    win_highlight_vertical: typing.NotRequired[bool | None]
    # window char
    win_ch: typing.NotRequired[str | None]


@dataclass(frozen=True, slots=True, repr=False)
class Style:
    default: typing.ClassVar[Style]
    # main style
    fg: Color | None = field(default=None)
    bg: Color | None = field(default=None)
    inner_fg: Color | None = field(default=None)
    inner_bg: Color | None = field(default=None)
    # attribute flags
    alternate_character_set: bool = field(default=False, kw_only=True)
    blink: bool = field(default=False, kw_only=True)
    bold: bool = field(default=False, kw_only=True)
    dim: bool = field(default=False, kw_only=True)
    invisible: bool = field(default=False, kw_only=True)
    italic: bool = field(default=False, kw_only=True)
    normal: bool = field(default=False, kw_only=True)
    protected_mode: bool = field(default=False, kw_only=True)
    reverse_colors: bool = field(default=False, kw_only=True)
    standout_mode: bool = field(default=False, kw_only=True)
    underline_mode: bool = field(default=False, kw_only=True)
    highlight_horizontal: bool = field(default=False, kw_only=True)
    highlight_left: bool = field(default=False, kw_only=True)
    highlight_low: bool = field(default=False, kw_only=True)
    highlight_right: bool = field(default=False, kw_only=True)
    highlight_top: bool = field(default=False, kw_only=True)
    highlight_vertical: bool = field(default=False, kw_only=True)
    # window style
    win_fg: Color | None = field(default=None)
    win_bg: Color | None = field(default=None)
    # window attribute flags
    win_alternate_character_set: bool = field(default=False, kw_only=True)
    win_blink: bool = field(default=False, kw_only=True)
    win_bold: bool = field(default=False, kw_only=True)
    win_dim: bool = field(default=False, kw_only=True)
    win_invisible: bool = field(default=False, kw_only=True)
    win_italic: bool = field(default=False, kw_only=True)
    win_normal: bool = field(default=False, kw_only=True)
    win_protected_mode: bool = field(default=False, kw_only=True)
    win_reverse_colors: bool = field(default=False, kw_only=True)
    win_standout_mode: bool = field(default=False, kw_only=True)
    win_underline_mode: bool = field(default=False, kw_only=True)
    win_highlight_horizontal: bool = field(default=False, kw_only=True)
    win_highlight_left: bool = field(default=False, kw_only=True)
    win_highlight_low: bool = field(default=False, kw_only=True)
    win_highlight_right: bool = field(default=False, kw_only=True)
    win_highlight_top: bool = field(default=False, kw_only=True)
    win_highlight_vertical: bool = field(default=False, kw_only=True)
    # window char
    win_ch: str = field(default=" ", kw_only=True)
    # integer representation of attribute flags
    _flag_attr: int = field(init=False, repr=False, compare=False)
    _win_flag_attr: int = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        # set integer representations of flag attributes
        _flag_attr = _bitor(v for k, v in _ATTRIBUTES.items() if getattr(self, k))
        _win_flag_attr = _bitor(v for k, v in _ATTRIBUTES.items() if getattr(self, f"win_{k}"))
        object.__setattr__(self, "_flag_attr", _flag_attr)
        object.__setattr__(self, "_win_flag_attr", _win_flag_attr)

    def __int__(self):
        return self.attr

    def __repr__(self):
        # represent as colors (when defined) and flags (when True)
        colors = [
            f"{attr}={getattr(self, attr)}"
            for attr in ["fg", "bg", "win_fg", "win_bg"]
            if getattr(self, attr) is not None
        ]
        flags = [f"{k}=True" for k in dir(self) if getattr(self, k) == True]
        return f"{self.__class__.__name__}({', '.join([*colors, *flags])})"

    @property
    def default_inner_fg(self):
        return self.inner_fg if self.inner_fg is not None else self.fg

    @property
    def default_inner_bg(self):
        return self.inner_bg if self.inner_bg is not None else self.bg

    @property
    def attr(self) -> int:
        if self.fg is not None and self.bg is not None:
            return ColorPair_(self.fg, self.bg) | self._flag_attr
        elif self.fg is not None and self.bg is None:
            return self.fg.fg | self._flag_attr
        elif self.bg is not None and self.fg is None:
            return self.bg.bg | self._flag_attr
        else:
            return self._flag_attr

    @property
    def win_attr(self) -> int:
        if self.win_fg is not None and self.win_bg is not None:
            return ColorPair_(self.win_fg, self.win_bg) | self._win_flag_attr
        elif self.win_fg is not None and self.win_bg is None:
            return self.win_fg.fg | self._win_flag_attr
        elif self.win_bg is not None and self.win_fg is None:
            return self.win_bg.bg | self._win_flag_attr
        else:
            return self._win_flag_attr

    def derive(self, **kwargs: typing.Unpack[WindowStyleKwargs]):
        """Create new Style derived from existing fields that are not replaced."""
        if not kwargs:
            # skip derivation if no fields are being overwritten
            return self
        else:
            # replace strings with Tailwind colors
            for key in ("fg", "bg", "inner_fg", "inner_bg", "win_fg", "win_bg"):
                color = kwargs.get(key)
                if isinstance(color, str):
                    kwargs[key] = Color_.tw(color)  # type: ignore
                elif isinstance(color, tuple):
                    kwargs[key] = Color_(*color)
        return replace(self, **_default_to_parent(self, **kwargs))


Style.default = Style()
