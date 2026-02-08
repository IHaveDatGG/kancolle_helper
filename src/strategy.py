import asyncio
from background_mouse import BackgroundMouse
import config
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

    def run(self):
        """Start the strategy by creating an async task"""
        self.running = True
        self.capture.start()
        self.task = asyncio.create_task(self._run())

    def stop(self):
        """Stop the strategy and cancel the async task"""
        self.running = False
        self.capture.stop()
        if self.task and not self.task.done():
            self.task.cancel()
            self.task = None

    async def _run(self) -> None:
        """Main strategy loop: continuously search for templates and perform actions"""
        try:
            # Base templates
            base_templates = [
                'combat/compass.png',
                "combat/line_ahead.png",
                'common/next.png',
                'common/return.png',
            ]

            # Main loop: keep searching and clicking templates
            while self.running:
                templates = base_templates.copy()

                match config.settings.advance:
                    case config.TriState.ENABLED:
                        templates.append("combat/advance.png")
                    case config.TriState.DISABLED:
                        templates.append("combat/retreat.png")

                match config.settings.night_battle:
                    case config.TriState.ENABLED:
                        templates.append("combat/engage_night_battle.png")
                    case config.TriState.DISABLED:
                        templates.append("combat/skip_night_battle.png")

                self._click_first_template_path(templates)
                await asyncio.sleep(TEMPLATE_SEARCH_INTERVAL)
        except asyncio.CancelledError:
            # Graceful exit when the task is cancelled
            return

    def _click_first_template_path(self, template_paths: list[str]):
        """Try to locate the first matching template and perform a mouse click"""
        image = self.capture.get_frame()
        if image is not None:
            pos = locate(image, template_paths)
            if pos is not None:
                self.mouse.click(pos)
