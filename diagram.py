from __future__ import annotations

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static, TextLog
from textual.widget import Widget
from textual.dom import DOMNode
from textual.widgets._static import _check_renderable
from rich.console import RenderableType
from rich.protocol import is_renderable
from rich.text import Text
from rich.bar import Bar


class Diagram(Widget):
    pass

class Node(Static):
    
    drag_active: bool = False
    drag_offset: tuple[int, int] = (0, 0)
    connectors: list[Connector] = []
    
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
            for c in self.connectors:
                c.update_segments()
            
    def add_connector(self, connector: Connector):
        self.connectors.append(connector)
       
       
class Connector():
    source: Node
    sink: Node
    segments: tuple[HorizontalLine, VerticalLine, HorizontalLine]
    
    @classmethod
    def from_nodes(cls, source: Node, sink: Node):
        """Constructor from two nodes"""
        self = cls()
        self.source = source
        self.sink = sink
        source.add_connector(self)
        sink.add_connector(self)
        
        self.segments = (HorizontalLine(), VerticalLine(), HorizontalLine())
        
        return self
    
    def update_segments(self):
        h1 = self.segments[0]
        v = self.segments[1]
        h2 = self.segments[2]
        source_offset = self.source.offset + (self.source.size[0] + 1, 0) - (0, 8)
        sink_offset = self.sink.offset
        width = self.sink.offset[0] - self.source.offset[0] - self.source.size[0]
        height = sink_offset[1] - source_offset[1] - 4
        h1.offset = source_offset
        v.offset = source_offset + (width // 2, 0) - (0, 1)
        h2.offset = source_offset + (width // 2, 0) - (0, 2)
        h1.set_styles(f"width: {width/2};")
        v.set_styles(f"height: {height};")
        h2.set_styles(f"width: {width/2};")
        


class VerticalLine(Static): pass

class HorizontalLine(Static): pass


class DiagramApp(App):
    CSS_PATH = "diagram.css"

    def compose(self) -> ComposeResult:
        a = Node("A")
        b = Node("B")
        c = Node("C")
        
        connector_1 = Connector.from_nodes(a, b)
        connector_2 = Connector.from_nodes(b, c)
        
        yield TextLog()
        yield Diagram(
            a,
            b,
            c,
            *connector_1.segments,
            *connector_2.segments,
        )


if __name__ == "__main__":
    app = DiagramApp()
    app.run()
