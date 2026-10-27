from .mazegen import generate
from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Input, Label
from textual.containers import Container, Horizontal, Vertical, Grid
from textual import work, events
from typing import Any
from time import sleep
import asyncio


THEMES = [
    "monokai",
    "textual-dark",
    "gruvbox",
]


class UserInterface(App[None]):

    CSS_PATH = "tui_css"

    def __init__(self, maze: generate, size: tuple[int, int],
                 seed: int, perfect: bool, start_exit: list[tuple[int, int]],
                 output_file: str, style: generate.Style | None) -> None:
        super().__init__()
        self.maze = maze
        self.maze_seed = seed
        self.width = size[0]
        self.height = size[1]
        self.seed = seed
        self.perfect = perfect
        self.current_style = style
        self.start_exit = start_exit
        self.output_file = output_file
        self.theme = THEMES[0]
        self.play = 0

    def update_maze(self) -> None:
        if self.check_maze_fits(self.maze):
            self.query_one("#maze", Static).update(
                self.maze.draw_maze())

    def update_settings(self) -> None:
        settings = self.read_maze_settings()
        if settings is None:
            return
        self.width, self.height, self.seed = settings
        start_exit = self.read_start_exit()
        if start_exit is None:
            return
        self.start_exit = start_exit

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
                yield Button("Play", id="play")
                yield Button("Solve maze", id="solve")
                yield Button("Cycle theme", id="theme")
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

                    yield Label("File:")
                    yield Input(str(self.output_file), id="output",
                                placeholder="maze.txt", classes="span-2")
                    yield Button("Export", id="export", classes="span-3")

                yield Label("Wall style", id="style-label")
                yield Button(str(self.maze.selected.name), id="style")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "generate":
            self.update_settings()
            self.maze = generate(
                (self.width, self.height), self.seed,
                self.perfect, self.current_style, self.start_exit)

            self.maze.kruskal()
            self.update_maze()
            self.maze_seed = self.seed

        elif event.button.id == "reset":
            self.maze = generate((self.width, self.height), self.maze_seed,
                                 self.perfect, self.current_style,
                                 self.start_exit)
            self.update_maze()
            self.play = 0
            self.query_one("#play", Button).label = "Play"

        elif event.button.id == "play":
            self.update_settings()
            if self.play == 0:
                self.play = 1
                asyncio.create_task(self.animate_gen())
                self.query_one("#play", Button).label = "Pause"
            else:
                self.play = 0
                self.query_one("#play", Button).label = "Play"

        elif event.button.id == "solve":
            start_exit = self.read_start_exit()
            if start_exit is None:
                return
            self.start_exit = start_exit
            self.maze.solve(self.start_exit)
            self.update_maze()

        elif event.button.id == "theme":
            """
            Switch to the next theme in themes
            """
            themes = [t for t in THEMES if t in self.available_themes]
            try:
                index = themes.index(self.theme)
            except ValueError:
                index = -1
            self.theme = themes[(index + 1) % len(themes)]
            self.notify(f"Theme: {self.theme}")

        elif event.button.id == "quit":
            self.exit()

        elif event.button.id == "export":
            filename = self.query_one("#output", Input).value.strip()
            if not filename:
                self.notify("Enter a file name first", severity="error")
                return
            try:
                self.maze.export_maze(filename, self.start_exit)
            except OSError as e:
                self.notify(f"Could not write {filename}: {e.strerror}",
                            severity="error")
                return
            self.output_file = filename
            self.notify(f"Exported to {filename}")

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

    async def animate_gen(self) -> None:
        max_connections = self.width * self.height - 1
        if self.width >= 9 and self.height >= 9:
            max_connections -= len(self.maze.ignore)

        if not self.maze.connections or self.maze.connections == max_connections:
            self.maze = generate(
                (self.width, self.height), self.seed,
                self.perfect, self.current_style, self.start_exit)
            self.update_maze()

        while self.play:
            tmp2 = self.maze.grid
            if self.maze.kruskal_play():
                self.play = 0
                self.query_one("#play", Button).label = "Play"
                return
            self.query_one("#maze", Static).update(self.maze.draw_maze())
            await asyncio.sleep(0.05)

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

        if start[0] >= self.height or start[1] > self.width - 1:
            if start[0] >= self.height:
                start = (self.height - 1, start[1])
            if start[1] >= self.width:
                start = (start[0], self.width - 1)

        if exit_[0] >= self.height or exit_[1] > self.width - 1:
            if exit_[0] >= self.height:
                exit_ = (self.height - 1, exit_[1])
            if exit_[1] >= self.width:
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
