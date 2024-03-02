import flet as ft


class AudioPlayer(ft.UserControl):
    def __init__(self, app, page: ft.Page):
        super().__init__()
        self.app = app
        self.page = page
        self.state = None
        self.track_time_changing = False

    def set_audio_elements(self, title, image_src, audio_src):
        self.page.overlay.clear()
        self.cover = ft.Image(
                    src=image_src,
                    width=96,
                    height=96,
                    fit=ft.ImageFit.COVER,
                    repeat=ft.ImageRepeat.NO_REPEAT
                )
        self.name_text = ft.Text(
                    title,
                    width=9 * 25
                    )
        self.play_pause_bttn = ft.IconButton(
                    icon=ft.icons.PAUSE_CIRCLE,
                    icon_color=ft.colors.WHITE,
                    on_click=lambda _: self.play_pause_audio()
                )
        self.volume_bttn = ft.IconButton(
                    icon=ft.icons.VOLUME_UP,
                    icon_color=ft.colors.WHITE,
                    on_click=lambda _: self.on_off_volume_slider()
                )
        self.volume_slider = self.slider = ft.Slider(
            value=20,
            min=0,
            divisions=100,
            max=100,
            width=200,
            on_change=self.set_track_volume,
            visible=False,
            label='{value}%'
            )
        self.audio = ft.Audio(
            src=audio_src,
            autoplay=True,
            volume=0.2,
            balance=0,
            on_position_changed=lambda e: self.change_slider_value(e),
            on_state_changed=lambda e: self.set_audio_state(e.data),
        )
        self.page.overlay.append(self.audio)
        self.slider = ft.Slider(value=0, min=0,
                                on_change_end=self.set_track_position,
                                on_change_start=self.set_slider_changing,
                                on_change=self.set_slider_label
                                )
        self.app.layout.bottombar.bottombar_height_update(200)
        self.app.layout.bottombar.bottombar_items.controls[0] = self.build()
        self.page.update()
        self.page.bottom_appbar.update()

    def set_track_position(self, e: ft.ControlEvent):
        self.track_time_changing = False
        if self.state == 'playing':
            self.audio.pause()
            self.slider.value = e.control.value
            self.audio.seek(int(self.slider.value))
            self.audio.resume()
        elif self.state == 'paused':
            self.play_pause_bttn.icon = ft.icons.PLAY_CIRCLE
            self.slider.value = e.control.value
        self.page.update()
            
    def set_slider_changing(self, e: ft.ControlEvent):
        self.track_time_changing = True
        
    def set_slider_label(self, e: ft.ControlEvent):
        track_duration = self.audio.get_duration()
        current_position = int(e.control.value)
        current_pos_converted = self.convert_to_ms(current_position)
        self.current_position_text = f'{current_pos_converted[0]}:'
        self.current_position_text += f'{current_pos_converted[1]}'
        self.slider.label = self.current_position_text
        self.page.update()

    def change_slider_value(self, e: ft.Control):
        if not self.track_time_changing:
            track_duration = self.audio.get_duration()
            current_position = int(e.data)
            if track_duration - current_position <= 100:
                self.play_pause_bttn.icon = ft.icons.PLAY_CIRCLE
            self.slider.max = track_duration
            self.slider.divisions = track_duration
            self.slider.value = e.data
            self.page.update()

    def convert_to_ms(self, value):
        total_seconds = value / 1000  # Переводим значение в секунды
        minutes = int(total_seconds // 60)  # Получаем количество минут
        seconds = int(total_seconds % 60)  # Получаем оставшиеся секунды
        seconds_formatted = str(seconds).zfill(2)
        return minutes, seconds_formatted

    def on_off_volume_slider(self):
        self.volume_slider.visible = not self.volume_slider.visible

        self.slider.disabled = not self.slider.disabled
        self.slider.visible = not self.slider.visible

        self.play_pause_bttn.disabled = not self.play_pause_bttn.disabled
        self.play_pause_bttn.visible = not self.play_pause_bttn.visible
        self.page.update()

    def set_track_volume(self, e: ft.ControlEvent):
        self.audio.volume = e.control.value / 100

    def set_audio_state(self, state):
        self.state = state

    def play_pause_audio(self):
        if self.state == 'playing':
            self.play_pause_bttn.icon = ft.icons.PLAY_CIRCLE
            self.audio.pause()
        elif self.state == 'paused':
            if self.slider.value != 0:
                self.audio.seek(int(self.slider.value))
            self.play_pause_bttn.icon = ft.icons.PAUSE_CIRCLE
            self.audio.resume()
        else:
            self.play_pause_bttn.icon = ft.icons.PAUSE_CIRCLE
            self.audio.play()
        self.page.update()
        
    def show_progress_starting_track(self):
        if self.state == 'playing':
            self.play_pause_bttn.icon = ft.icons.PLAY_CIRCLE
            self.audio.release()
        self.app.layout.bottombar.bottombar_height_update(135)
        self.app.layout.bottombar.bottombar_items.controls[0] = ft.Row(
            [
                ft.ProgressRing()
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.page.bottom_appbar.update()
        self.page.update()

    def build(self):
        middle_part = ft.Column(
            [
                self.name_text,
                ft.Row(
                    [
                        self.slider,
                        self.play_pause_bttn,
                        self.volume_bttn,
                        self.volume_slider,
                    ],
                    spacing=0
                ),
            ]
        )
        view = ft.Row(
            [
                self.cover,
                middle_part,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        return view
