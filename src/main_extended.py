import asyncio
import flet as ft
from background_mouse import BackgroundMouse
from strategy import Strategy
from template_locator import locate
from ui import UI
from window_capture import WindowCapture


# base modules
wc = WindowCapture("poi")
bg_mouse = BackgroundMouse("poi")
strategies = {
    "5-2": Strategy(wc, bg_mouse),
    "5-3": Strategy(wc, bg_mouse)
}

# ui
ui = UI()
ui_text = ft.Text("Extension Strategy", size=24)
start_button = ft.Button(
    "Start",
    width=300,
    height=70,
    style=ft.ButtonStyle(bgcolor={"": "blue"}, color={"": "white"})
)
strategy_options = ft.SegmentedButton(
    selected=["5-2"],
    show_selected_icon=False,
    segments=[
        ft.Segment(value="5-2", label="5-2"),
        ft.Segment(value="5-3", label="5-3")
    ]
)
formation_options = ft.SegmentedButton(
    selected=["x"],
    show_selected_icon=False,
    segments=[
        ft.Segment(value="x", label="X"),
        ft.Segment(value="line_ahead", label="單縱陣")
    ]
)


def override_strategy():
    async def _run_5_2():
        try:
            await wait_and_click("port/sortie.png", double_click=True)
            await wait_and_click("sortie/sortie.png", double_click=True)
            await wait_and_click("sortie/world_5.png")
            await wait_and_click("sortie/5-2.png")
            await wait_and_click("sortie/confirm_1.png")
            await wait_and_click("sortie/confirm_2.png")
            await wait_and_click("combat/compass.png")
            if formation_options.selected[0] != "x":
                await wait_and_click(f"combat/{formation_options.selected[0]}.png")
            await wait_and_click("common/next.png", wait=3.0)
            await wait_and_click("common/next.png")
            await wait_and_click("combat/retreat.png")
            start_button.on_click()
        except asyncio.CancelledError:
            return

    async def _run_5_3():
        try:
            await wait_and_click("port/sortie.png", double_click=True)
            await wait_and_click("sortie/sortie.png", double_click=True)
            await wait_and_click("sortie/world_5.png")
            await wait_and_click("sortie/5-3.png")
            await wait_and_click("sortie/confirm_1.png")
            await wait_and_click("sortie/confirm_2.png")

            await wait_and_click("combat/compass.png", wait=5.0)
            await wait_and_click("combat/compass.png")
            await wait_and_click("combat/line_ahead.png")
            await wait_and_click("common/next.png", wait=3.0)
            await wait_and_click("common/next.png")
            await wait_and_click("combat/advance.png")

            await wait_and_click("combat/compass.png", double_click=True)
            await wait_and_click("combat/5-3-P.png", double_click=True)
            await wait_and_click("combat/line_ahead.png", double_click=True)
            await wait_and_click("common/next.png", wait=3.0)
            await wait_and_click("common/next.png")
            await wait_and_click("combat/retreat.png")
            start_button.on_click()
        except asyncio.CancelledError:
            return

    async def wait_and_click(target, wait = 0.5, double_click = False):
        # update text
        ui_text.value = target
        ui.page.update()

        # find template
        pos = None
        while pos is None:
            await asyncio.sleep(0.1)
            image = wc.get_frame()
            if image is not None:
                pos = locate(image, [target])

        # click
        if double_click:
            bg_mouse.double_click(pos)
        else:
            bg_mouse.click(pos)

        # wait a minute
        await wait_and_update_text(wait)

    async def wait_and_update_text(seconds: float, interval: float = 0.05):
        remaining = seconds
        while remaining > 0:
            ui_text.value = f"wait: {remaining:.2f}s"
            ui.page.update()
            await asyncio.sleep(interval)
            remaining -= interval
        ui_text.value = f"wait: 0s"
        ui.page.update()

    strategies["5-2"]._run = _run_5_2
    strategies["5-3"]._run = _run_5_3


def override_ui():
    def toggle_strategy_execution():
        if not strategies[strategy_options.selected[0]].running:
            strategies[strategy_options.selected[0]].run()
            start_button.content = f"Stop Strategy {strategy_options.selected[0]}"
            start_button.style.bgcolor = {"": "red"}
        else:
            strategies[strategy_options.selected[0]].stop()
            ui_text.value = "Extension Strategy"
            start_button.content = f"Start Strategy {strategy_options.selected[0]}"
            start_button.style.bgcolor = {"": "blue"}
        ui.page.update()

    start_button.on_click = toggle_strategy_execution
    ui.container.content.controls = [ui_text, start_button, strategy_options, formation_options]

    original_main = ui._main

    def override_main(page: ft.Page):
        original_main(page)
        page.title = f"{page.title} (extended)"

    ui._main = override_main


def main():
    def close_all_strategies():
        for s in strategies.values():
            s.stop()

    override_strategy()
    override_ui()
    ui.run(None, close_all_strategies)


if __name__ == "__main__":
    main()
