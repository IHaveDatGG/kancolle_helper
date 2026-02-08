import asyncio
import flet as ft

import config

# Window configuration
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500

# Font sizes
TITLE_FONT_SIZE = 24
SUBTITLE_FONT_SIZE = 18

# UI element sizes
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40
TEXTFIELD_WIDTH = 200

# Animation settings
ANIMATION_DURATION = 3000
ANIMATION_CURVE = ft.AnimationCurve.EASE_IN_OUT
GRADIENT_COLORS = [
    ["#cc2222", "#966666"],
    ["#8888dd", "#bb1188"],
    ["#bbbb55", "#ff7fff"],
    ["#5bbbbb", "#3377dd"],
]


class UI:
    def __init__(self):
        # Page reference
        self.page: ft.Page | None = None

        # State flags and callbacks
        self.running: bool = False
        self.run_strategy = None
        self.stop_strategy = None

        # Toolbar
        self.capture_mode_button = ft.IconButton(
            icon=ft.icons.Icons.PHOTO_CAMERA_BACK,
            icon_color="yellow",
            tooltip=config.CaptureMode.SINGLE.value,
            on_click=self._toggle_capture_mode
        )
        self.toolbar = ft.Row(
            controls=[
                self.capture_mode_button
            ],
            alignment=ft.MainAxisAlignment.END
        )

        # Status display
        self.status = ft.Text("Current status: Waiting", size=TITLE_FONT_SIZE)

        # Input row (label + text field)
        self.window_title_input = ft.TextField(value="poi", width=TEXTFIELD_WIDTH)
        self.input_row = ft.Row(
            controls=[
                ft.Text("Window Title:", size=SUBTITLE_FONT_SIZE),
                self.window_title_input
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Main control button
        self.main_button = ft.ElevatedButton(
            "Run Strategy",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            style=ft.ButtonStyle(
                bgcolor={"": "blue"},
                color={"": "white"}
            ),
            on_click=self._toggle_strategy_execution
        )

        # Options
        self.march_option =  ft.Switch(label="March")
        self.night_battle_option = ft.Switch(label="Night battle")

        # Main container layout
        self.container = ft.Container(
            expand=True,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.status,
                    self.input_row,
                    self.main_button,
                    self.march_option,
                    self.night_battle_option,
                ],
            ),
            animate=ft.Animation(ANIMATION_DURATION, ANIMATION_CURVE),
        )

    def run(self, run_strategy, stop_strategy) -> None:
        """Initialize callbacks and start the Flet app."""
        self.run_strategy = run_strategy
        self.stop_strategy = stop_strategy
        ft.run(self._main)

    def _main(self, page: ft.Page) -> None:
        """Configure the main page and add UI components."""
        self.page = page
        page.title = "Kancolle Helper v0.1.3"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.window.width = WINDOW_WIDTH
        page.window.height = WINDOW_HEIGHT
        page.window.resizable = False
        page.on_close = self._stop_strategy
        page.add(
            ft.Stack([
                self.container,
                self.toolbar,
            ], expand=True)
        )

    def _toggle_capture_mode(self) -> None:
        """Toggle the current capture mode between SINGLE and CONTINUOUS."""
        if self.running:
            return

        config.settings.toggle_capture_mode()

        if config.settings.capture_mode == config.CaptureMode.SINGLE:
            self.capture_mode_button.icon = ft.icons.Icons.PHOTO_CAMERA_BACK
            self.capture_mode_button.icon_color = "yellow"
        else:
            self.capture_mode_button.icon = ft.icons.Icons.VIDEO_CAMERA_BACK
            self.capture_mode_button.icon_color = "red"

        self.capture_mode_button.tooltip = config.settings.capture_mode.value

    async def _toggle_strategy_execution(self) -> None:
        """Toggle between starting and stopping the strategy."""
        if not self.window_title_input.value:
            self.window_title_input.error = "Window cannot be empty"
            return

        self.window_title_input.error = None

        if not self.running:
            await self._run_strategy()
        else:
            self._stop_strategy()

    async def _run_strategy(self) -> None:
        """Start the strategy and update UI state."""
        self.running = True
        self.status.value = "Current status: Running"
        self.main_button.content = "Stop strategy"
        self.page.update()

        # Call external strategy function
        self.run_strategy(self.window_title_input.value)

        # Background gradient animation
        i = 0
        while self.running:
            self.container.gradient = ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=GRADIENT_COLORS[i],
            )
            self.page.update()
            i = (i + 1) % len(GRADIENT_COLORS)
            await asyncio.sleep(5)

    def _stop_strategy(self):
        """Stop the strategy and reset UI state."""
        self.running = False
        self.status.value = "Current status: Waiting"
        self.container.gradient = None
        self.main_button.content = "Run strategy"
        self.page.update()
        if self.stop_strategy:
            self.stop_strategy()
