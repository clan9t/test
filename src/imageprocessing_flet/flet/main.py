import flet as ft
from ui import create_ui
from handlers import start_button_handler, settings_button_handler, zoom_in_handler, zoom_out_handler, reset_zoom_handler, adjust_threshold_handler

def main(page: ft.Page):
    page.title = 'Application(Anomely Detection)'
    # UI作成
    menu_bar, left_column, right_column = create_ui(
        start_button_handler,
        settings_button_handler,
        zoom_in_handler,
        zoom_out_handler,
        reset_zoom_handler,
        adjust_threshold_handler
    )

    # 全体のレスポンシブレイアウト
    layout = ft.ResponsiveRow(
        controls=[
            ft.Column([left_column], col={"xs": 12, "sm": 12, "md": 6, "lg": 6}),
            ft.Column([right_column], col={"xs": 12, "sm": 12, "md": 6, "lg": 6}),
        ],
        spacing=20
    )

    page.add(menu_bar, layout)

ft.app(target=main)
