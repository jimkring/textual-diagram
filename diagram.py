from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static, TextLog


class Diagram(Container):
    pass

class Node(Static):
    
    drag_active: bool = False
    drag_offset: tuple[int, int] = (0, 0)
    
    def on_mouse_down(self, event: events.MouseDown) -> None:
        """Start dragging on mouse down"""
        self.drag_offset = event.offset
        self.set_styles("border: tall white;")
        self.drag_active = True
        self.capture_mouse()
        
    def on_mouse_up(self, event: events.MouseUp) -> None:
        """Stop dragging on mouse up"""
        self.set_styles("border: tall black;")
        self.drag_active = False
        self.release_mouse()
        
    def on_mouse_move(self, event: events.MouseMove) -> None:
        """Move node on mouse move"""
        if self.drag_active:
            self.offset = self.offset + event.offset - self.drag_offset


class Connector(Static):
    
    source: tuple[int, int] = (0, 0)
    sink: tuple[int, int] = (0, 0)
    auto_width: bool = False
    auto_height: bool = False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DiagramApp(App):
    CSS_PATH = "diagram.css"

    def compose(self) -> ComposeResult:
        yield TextLog()
        yield Diagram(
            Node("A"),
            Node("B"),
            Node("C"),
            Connector("testing"),
        )


if __name__ == "__main__":
    app = DiagramApp()
    app.run()
