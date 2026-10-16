from .generator import generate
from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Input, Label
from textual.containers import Container, Horizontal, Vertical, Grid
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
    }

    #maze {
        width: auto;
        height: auto;
        color: cyan;
    }

    #controls {
        dock: bottom;
        width: 100%;
        height: auto;
    }

    .panel {
        width: 1fr;
        height: auto;
        border: round cyan;
        padding: 1;
        margin-bottom: 1;
    }

    Button:focus {
        text-style: none;
        color: cyan;
    }

    #actions Button {
        width: 100%;
        margin-bottom: 1;
    }

    #actions Button:last-of-type {
        margin-bottom: 0;
    }

    #settings-grid {
        layout: grid;
        grid-size: 6;
        grid-columns: 9 1fr 1fr 9 1fr 1fr;
        grid-rows: auto;
        grid-gutter: 0 1;
        width: 100%;
        height: auto;
    }

    #settings-grid Label {
        width: 100%;
        height: 3;
        content-align: left middle;
    }

    #settings-grid ScrollInput,
    #settings-grid Button {
        width: 100%;
        min-width: 0;
    }

    .span-2 { column-span: 2; }
    .span-5 { column-span: 5; }

    #style-label {
        margin-top: 1;
    }

    #style {
        width: 100%;
        height: 3;
    }
    """

    def __init__(self, maze: generate, size: tuple[int, int],
                 seed: int, perfect: bool, start_exit: list[tuple[int, int]],
                 style: generate.Style | None) -> None:
        super().__init__()
        self.maze = maze
        self.width = size[0]
        self.height = size[1]
        self.seed = seed
        self.perfect = perfect
        self.current_style = style
        self.start_exit = start_exit

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
            yield Static(self.maze.draw_maze(), id="maze", markup=False)

        with Horizontal(id="controls"):
            with Vertical(id="actions", classes="panel"):
                yield Button("Generate maze", id="generate")
                yield Button("Reset", id="reset")
                yield Button("Step", id="step")
                yield Button("Solve maze", id="solve")
                yield Button("Quit", id="quit")

            with Vertical(id="settings", classes="panel"):
                (start_y, start_x), (exit_y, exit_x) = self.start_exit

                with Grid(id="settings-grid"):
                    yield Label("Maze:")
                    yield self.ScrollInput(
                        str(self.height), id="height", placeholder="H")
                    yield self.ScrollInput(
                        str(self.width), id="width", placeholder="W")

                    yield Label("Perfect:")
                    yield Button(str(self.perfect), id="perfect",
                                 classes="span-2")

                    yield Label("Start:")
                    yield self.ScrollInput(
                        str(start_y), id="start-y", placeholder="Y")
                    yield self.ScrollInput(
                        str(start_x), id="start-x", placeholder="X")

                    yield Label("Exit:")
                    yield self.ScrollInput(
                        str(exit_y), id="exit-y", placeholder="Y")
                    yield self.ScrollInput(
                        str(exit_x), id="exit-x", placeholder="X")

                    yield Label("Seed:")
                    yield self.ScrollInput(
                        str(self.seed), id="seed", placeholder="Seed",
                        classes="span-5")

                yield Label("Wall style", id="style-label")
                yield Button(str(self.maze.selected.name), id="style")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "generate":
            settings = self.read_maze_settings()
            if settings is None:
                return
            self.width, self.height, self.seed = settings
            start_exit = self.read_start_exit()
            if start_exit is None:
                return
            self.start_exit = start_exit
            self.maze = generate(
                (self.width, self.height), self.seed,
                self.perfect, self.current_style, self.start_exit)

            self.maze.kruskal()
            self.update_maze()

        elif event.button.id == "reset":
            self.maze = generate((self.width, self.height), self.seed,
                                 self.perfect, self.current_style,
                                 self.start_exit)
            self.update_maze()

        if event.button.id == "step":
            self.maze.kruskal_play()
            self.query_one("#maze", Static).update(
                            self.maze.draw_maze())

        elif event.button.id == "solve":
            start_exit = self.read_start_exit()
            if start_exit is None:
                return
            self.start_exit = start_exit
            self.maze.solve(self.start_exit)
            self.update_maze()

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

    def read_maze_settings(self) -> tuple[int, int, int] | None:
        """
            check weither the input fields are numbers
            Return (width, height, seed) from the inputs, or None if invalid.
        """
        try:
            width = int(self.query_one("#width", Input).value)
            height = int(self.query_one("#height", Input).value)
            seed = int(self.query_one("#seed", Input).value)
        except ValueError:
            self.notify("Width, height and seed must be whole numbers",
                        severity="error")
            return None

        if width < 1 or height < 1:
            self.notify("Width and height must be at least 1",
                        severity="error")
            return None

        return width, height, seed

    def read_start_exit(self) -> list[tuple[int, int]] | None:
        """
            check weither the input fields are numbers and clamps
            to maze size if too large Return ((start_y, start_x),
            (exit_y, exit_x)) from the inputs, or None if invalid.
        """
        try:
            start = (
                int(self.query_one("#start-y", Input).value),
                int(self.query_one("#start-x", Input).value),
            )
            exit_ = (
                int(self.query_one("#exit-y", Input).value),
                int(self.query_one("#exit-x", Input).value),
            )
        except ValueError:
            self.notify("Start/exit must be whole numbers", severity="error")
            return None

        if start[0] > self.height or start[1] > self.width - 1:
            if start[0] > self.height:
                start = (self.height - 1, start[1])
            if start[1] > self.width - 1:
                start = (start[0], self.width - 1)

        if exit_[0] > self.height or exit_[1] > self.width - 1:
            if exit_[0] > self.height:
                exit_ = (self.height - 1, exit_[1])
            if exit_[1] > self.width - 1:
                exit_ = (exit_[0], self.width - 1)
        return [start, exit_]

    class ScrollInput(Input):
        """
            uses events to detect the scrolling of the mouse wheel
        """
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

            self.value = str(max(0, value + amount))
