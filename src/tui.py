from generator import generate
from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Input, Label
from textual.containers import Container, Horizontal, Vertical
from textual import events
from typing import Any


class UserInterface(App[None]):
    CSS = """
        Screen {
            min-width: 50;
            min-height: 50;
            align: center middle;
            border: round cyan;
        }

        #maze-container {
            width: 100%;
            height: 1fr;
            align: center middle;
            padding-top: 0;
            border: round cyan;
        }

        #maze {
            width: auto;
            height: auto;
            padding: 0;
            margin: 0;
            color: cyan;
        }

        Button:focus {
            text-style: none;
            color: cyan;
        }

        #controls {
            dock: bottom;
            width: 100%;
            height: auto;
        }

        #button-container,
        #button-container2 {
            width: 50%;
            height: auto;
            border: round cyan;
            padding: 1;
            margin-bottom: 1;
        }

        #button-container Button,
        #button-container2 Button {
            width: 100%;
            margin-bottom: 1;
        }
    """

    def __init__(self, maze: generate, width: int, height: int,
                 seed: int, perfect: bool, style: list[generate.Style] | None) -> None:
        super().__init__()
        self.maze = maze
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.current_style = style

    def update_maze(self) -> None:
        if self.check_maze_fits(self.maze):
            self.query_one("#maze", Static).update(
                self.maze.draw_maze())

    def check_maze_fits(self, maze: generate) -> bool:
        lines = str(maze.draw_maze()).splitlines()
        avail_w, avail_h = self.query_one("#maze-container").content_size
        if len(lines[0]) > avail_w or len(lines) > avail_h:
            self.notify(f"Maze ({len(lines[0])}×{len(lines)}) won't fit "
                        f"in the display ({avail_w}×{avail_h}).",
                        title="Maze too large",
                        severity="error")
            return False
        return True

    def compose(self) -> ComposeResult:
        with Container(id="maze-container"):
            yield Static(
                self.maze.draw_maze(),
                id="maze",
                markup=False,
            )

        with Horizontal(id="controls"):
            with Vertical(id="button-container"):
                yield Button("Generate maze", id="generate")
                yield Button("Reset", id="reset")
                yield Button("Step", id="step")
                yield Button("Solve maze", id="solve")
                yield Button("Quit", id="quit")

            with Vertical(id="button-container2"):
                yield Label("Maze width")
                yield self.ScrollInput(str(self.width),
                                       id="width", placeholder="Width")

                yield Label("Maze height")
                yield self.ScrollInput(str(self.height),
                                       id="height", placeholder="Height")

                yield Label("Seed")
                yield self.ScrollInput(str(self.seed),
                                       id="seed", placeholder="Seed")

                yield Label("Perfect")
                yield Button(str(self.perfect), id="perfect")

                yield Label("Wall style")
                yield Button(str(self.maze.selected.name), id="style")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "generate":
            self.width = int(self.query_one("#width", Input).value)
            self.height = int(self.query_one("#height", Input).value)
            self.seed = int(self.query_one("#seed", Input).value)

            self.maze = generate((self.width, self.height),
                                 self.seed, self.perfect, self.current_style)
            self.maze.kruskal()
            self.update_maze()

        elif event.button.id == "reset":
            self.maze = generate((self.width, self.height),
                                 self.seed, self.perfect, self.current_style)
            self.update_maze()

        if event.button.id == "step":
            self.maze.kruskal_play()
            self.query_one("#maze", Static).update(
                            self.maze.draw_maze())

        elif event.button.id == "solve":
            import sys
            sys.exit(1)

        elif event.button.id == "quit":
            self.exit()

        elif event.button.id == "perfect":
            if self.perfect:
                self.perfect = False
            else:
                self.perfect = True
            self.query_one("#perfect", Button).label = f"{str(self.perfect)}"

        elif event.button.id == "style":
            self.maze.next_style()
            self.current_style = self.maze.selected
            self.query_one("#style", Button).label = self.maze.selected.name
            self.update_maze()

    class ScrollInput(Input):
        def __init__(self, *args: Any, step: int = 1, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            self.step = step

        def on_mouse_scroll_up(self, event: events.MouseScrollUp) -> None:
            self.change_value(self.step)
            event.stop()

        def on_mouse_scroll_down(self, event: events.MouseScrollDown) -> None:
            self.change_value(-self.step)
            event.stop()

        def change_value(self, amount: int) -> None:
            try:
                value = int(self.value or "0")
            except ValueError:
                value = 0

            self.value = str(max(1, value + amount))


if __name__ == "__main__":
    maze = generate((22, 11), 42, True, None)
    app = UserInterface(maze, 22, 11, 42, True, None)
    app.run()
