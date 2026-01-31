import asyncio
from background_mouse import BackgroundMouse
from template_locator import locate
from window_capture import WindowCapture

# Interval (in seconds) between template searches to avoid CPU overuse
TEMPLATE_SEARCH_INTERVAL = 0.05


class Strategy:
    def __init__(self, wc: WindowCapture, bg_mouse: BackgroundMouse):
        self.capture: WindowCapture = wc
        self.mouse: BackgroundMouse = bg_mouse
        self.running: bool = False
        self.task: asyncio.Task | None = None

    def run(self, march: bool = False, night_battle: bool = False):
        """Start the strategy by creating an async task"""
        self.running = True
        self.task = asyncio.create_task(self._run(march=march, night_battle=night_battle))

    def stop(self):
        """Stop the strategy and cancel the async task"""
        self.running = False
        if self.task and not self.task.done():
            self.task.cancel()
            self.task = None

    async def _run(self, march: bool = False, night_battle: bool = False) -> None:
        """Main strategy loop: continuously search for templates and perform actions"""
        try:
            # Base templates
            templates = [
                'combat/compass.png',
                "combat/line_ahead.png",
                'common/next.png',
                'common/return.png',
            ]

            # Optional templates
            if march:
                templates.append("combat/advance.png")

            if night_battle:
                templates.append("combat/engage_night_battle.png")
            else:
                templates.append("combat/skip_night_battle.png")

            # Main loop: keep searching and clicking templates
            while self.running:
                self._click_first_template_path(templates)
                await asyncio.sleep(TEMPLATE_SEARCH_INTERVAL)
        except asyncio.CancelledError:
            # Graceful exit when the task is cancelled
            return

    def _click_first_template_path(self, template_paths: list[str]):
        """Try to locate the first matching template and perform a mouse click"""
        image = self.capture.snapshot()
        pos = locate(image, template_paths)
        if pos is not None:
            self.mouse.click(pos)
