import flet as ft

def create_ui(start_button_handler, settings_button_handler, zoom_in_handler, zoom_out_handler, reset_zoom_handler, adjust_threshold_handler):
    # 上部メニューバー
    start_button = ft.ElevatedButton(text="開始", on_click=start_button_handler)
    settings_button = ft.ElevatedButton(text="設定", on_click=settings_button_handler)
    menu_bar = ft.Row([start_button, settings_button], alignment=ft.MainAxisAlignment.START)

    # 左側の画像認識結果部分
    recognition_result = ft.Text("画像認識結果: OK")

    zoom_in_button = ft.IconButton(icon=ft.icons.ZOOM_IN, on_click=zoom_in_handler)
    zoom_out_button = ft.IconButton(icon=ft.icons.ZOOM_OUT, on_click=zoom_out_handler)
    reset_zoom_button = ft.ElevatedButton(text="リセット", on_click=reset_zoom_handler)
    zoom_controls = ft.Row([zoom_in_button, zoom_out_button, reset_zoom_button], alignment=ft.MainAxisAlignment.START)

    image = ft.Image(src="path_to_image.png", width=300, height=300)  # 画像のパスを指定

    left_column = ft.Column([
        recognition_result,
        zoom_controls,
        image
    ], spacing=10)

    # 右側のしきい値調整と異常度表示部分
    threshold_button = ft.ElevatedButton(text="しきい値調整", on_click=adjust_threshold_handler)

    threshold_bar = ft.ProgressBar(value=0.5, semantics_label=['0','100'], color='red', bgcolor='#00000000')  # 異常度の初期値を設定
    abnormality_bar = ft.ProgressBar(value=0.7, semantics_label=['0','100'])  # 異常度の初期値を設定

    threshold_text = ft.Text("しきい値: 50")  # しきい値の表示
    abnormality_text = ft.Text("異常度: 70")  # 判定結果と異常度の表示
    result_text = ft.Text(
        "判定結果: OK",
        size=20,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE_600,
        weight=ft.FontWeight.W_100,
        )
    
    result_button = ft.ElevatedButton(
        content=ft.Text("OK", size=20, style=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        # opacity_on_click=1.0,
        disabled=True,
        style = ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    bgcolor=ft.colors.BLUE
                ),
    )
    axis_row = ft.Row([
        ft.Container(
            content=ft.Text(value="0"), alignment=ft.alignment.center
            ),
        ft.Container(
            content=ft.Text(value="100"), alignment=ft.alignment.center
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    # 判定結果と異常度の表示
    text_colume = ft.Row([
        threshold_text,
        abnormality_text,
    ], spacing=10)

    bar_colume = ft.Column([
        threshold_bar,
        abnormality_bar,
        axis_row
    ], spacing=0)

    # threshold_colume = ft.Column([
    #     threshold_text,
    #     threshold_bar,
    # ], spacing=0)

    # abnormality_colume = ft.Column([
    #     abnormality_text,
    #     abnormality_bar,
    # ], spacing=0)

    result_card = ft.Card(content=ft.Container(ft.Column([text_colume, bar_colume, result_button]), padding=10))


    right_column = ft.Column([
        threshold_button,
        result_card,
        # threshold_colume,
        # abnormality_colume,
        # result_text
    ], spacing=10)

    return menu_bar, left_column, right_column
