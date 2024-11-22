from textual.binding import Binding
from textual.containers import VerticalScroll


class MyVerticalScroll(VerticalScroll):
    BINDINGS = [
        Binding("up,k", "scroll_up", "Scroll Up", show=False),
        Binding("down,j", "scroll_down", "Scroll Down", show=False),
        Binding("left,h", "scroll_left", "Scroll Up", show=False),
        Binding("right,l", "scroll_right", "Scroll Right", show=False),
        Binding("home,g", "scroll_home", "Scroll Home", show=False),
        Binding("end,G", "scroll_end", "Scroll End", show=False),
        Binding("pageup,b", "page_up", "Page Up", show=False),
        Binding("pagedown,f", "page_down", "Page Down", show=False),
        Binding("ctrl+pageup", "page_left", "Page Left", show=False),
        Binding("ctrl+pagedown", "page_right", "Page Right", show=False),
    ]
