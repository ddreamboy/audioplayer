import flet as ft

def main(page):

    def slider_changed(e):
        t.value = f"Slider changed to {e.control.value}"
        slider.label = f"{e.control.value}%"
        page.update()

    t = ft.Text()
    slider = ft.Slider(min=0, max=100, on_change=slider_changed)
    page.add(
        ft.Text("Slider with 'on_change' event:"),
        slider
    )
        

ft.app(target=main)