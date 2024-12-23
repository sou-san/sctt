from textual.binding import Binding
from textual.widgets import DataTable


class MyDataTable[T](DataTable[T]):
    """vim keybindings が使える DataTable"""

    BINDINGS = [
        Binding("enter", "select_cursor", "Select", show=False),
        Binding("up,k", "cursor_up", "Cursor up", show=False),
        Binding("down,j", "cursor_down", "Cursor down", show=False),
        Binding("right,l", "cursor_right", "Cursor right", show=False),
        Binding("left,h", "cursor_left", "Cursor left", show=False),
        Binding("pageup,ctrl+b", "page_up", "Page up", show=False),
        Binding("pagedown,ctrl+f", "page_down", "Page down", show=False),
        Binding("ctrl+home,g", "scroll_top", "Top", show=False),
        Binding("ctrl+end,G", "scroll_bottom", "Bottom", show=False),
        Binding("home,0", "scroll_home", "Home", show=False),
        Binding("end,$", "scroll_end", "End", show=False),
    ]
    """
    | Key(s) | Description |
    | :- | :- |
    | enter | Select cells under the cursor. |
    | up,k | Move the cursor up. |
    | down,j | Move the cursor down. |
    | right,l | Move the cursor right. |
    | left,h | Move the cursor left. |
    | pageup,ctrl+b | Move one page up. |
    | pagedown,ctrl+f | Move one page down. |
    | ctrl+home,g | Move to the top. |
    | ctrl+end,G | Move to the bottom. |
    | home,0 | Move to the home position (leftmost column). |
    | end,$ | Move to the end position (rightmost column). |
    """
