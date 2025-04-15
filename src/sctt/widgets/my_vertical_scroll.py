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
        Binding("pageup,ctrl+b", "page_up", "Page Up", show=False),
        Binding("pagedown,ctrl+f", "page_down", "Page Down", show=False),
        Binding("ctrl+pageup", "page_left", "Page Left", show=False),
        Binding("ctrl+pagedown", "page_right", "Page Right", show=False),
    ]
    """Keyboard bindings for scrollable containers.

    | Key(s) | Description |
    | :- | :- |
    | up,k | Scroll up, if vertical scrolling is available. |
    | down,j | Scroll down, if vertical scrolling is available. |
    | left,h | Scroll left, if horizontal scrolling is available. |
    | right,l | Scroll right, if horizontal scrolling is available. |
    | home,g | Scroll to the home position, if scrolling is available. |
    | end,G | Scroll to the end position, if scrolling is available. |
    | pageup,ctrl+b | Scroll up one page, if vertical scrolling is available. |
    | pagedown,ctrl+f | Scroll down one page, if vertical scrolling is available. |
    | ctrl+pageup | Scroll left one page, if horizontal scrolling is available. |
    | ctrl+pagedown | Scroll right one page, if horizontal scrolling is available. |
    """

    @property
    def can_focus(self) -> bool:
        return self.show_vertical_scrollbar

    @can_focus.setter
    def can_focus(self, flag: bool) -> None:
        self.can_focus = flag
