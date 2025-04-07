from textual.binding import Binding
from textual.containers import ScrollableContainer


class MyScrollableContainer(ScrollableContainer):
    """Vim キーバインドが使える ScrollableContainer"""

    BINDINGS = [
        Binding("k,up", "scroll_up", "Scroll Up", show=False),
        Binding("j,down", "scroll_down", "Scroll Down", show=False),
        Binding("h,left", "scroll_left", "Scroll Left", show=False),
        Binding("l,right", "scroll_right", "Scroll Right", show=False),
        Binding("home", "scroll_home", "Scroll Home", show=False),
        Binding("end", "scroll_end", "Scroll End", show=False),
        Binding("g,pageup", "page_up", "Page Up", show=False),
        Binding("G,pagedown", "page_down", "Page Down", show=False),
        Binding("0,ctrl+pageup", "page_left", "Page Left", show=False),
        Binding("$,ctrl+pagedown", "page_right", "Page Right", show=False),
    ]
    """Keyboard bindings for scrollable containers.

    | Key(s) | Description |
    | :- | :- |
    | k,up | Scroll up, if vertical scrolling is available. |
    | j,down | Scroll down, if vertical scrolling is available. |
    | h,left | Scroll left, if horizontal scrolling is available. |
    | l,right | Scroll right, if horizontal scrolling is available. |
    | home | Scroll to the home position, if scrolling is available. |
    | end | Scroll to the end position, if scrolling is available. |
    | g,pageup | Scroll up one page, if vertical scrolling is available. |
    | G,pagedown | Scroll down one page, if vertical scrolling is available. |
    | 0,ctrl+pageup | Scroll left one page, if horizontal scrolling is available. |
    | $,ctrl+pagedown | Scroll right one page, if horizontal scrolling is available. |
    """
