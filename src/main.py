from background_mouse import BackgroundMouse
from strategy import Strategy
from ui import UI
from window_capture import WindowCapture


def main():
    strategy: Strategy | None = None

    def run_strategy(title: str, march: bool = False, night_battle: bool = False):
        nonlocal strategy
        wc = WindowCapture(title)
        bg_mouse = BackgroundMouse(title)
        strategy = Strategy(wc, bg_mouse)
        strategy.run(march, night_battle)

    def stop_strategy():
        if strategy:
            strategy.stop()

    UI().run(run_strategy, stop_strategy)


if __name__ == "__main__":
    main()
