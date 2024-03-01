import flet as ft


class AudioPlayer(ft.UserControl):
    def __init__(self, app, page: ft.Page):
        super().__init__()
        self.app = app
        self.page = page
        self.current_position_text = ft.Text()
        self.duration_text = ft.Text()
        self.state = None

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
            value=1,
            min=0,
            max=1,
            width=100,
            on_change_end=self.set_track_volume,
            rotate=-1.57,
            )
        self.audio = ft.Audio(
            src=audio_src,
            autoplay=True,
            volume=1,
            balance=0,
            on_position_changed=lambda e: self.change_slider_value(e),
            on_state_changed=lambda e: self.set_audio_state(e.data),
        )
        self.page.overlay.append(self.audio)
        self.slider = ft.Slider(value=0, min=0,
                                on_change_end=self.set_track_position)
        self.app.layout.bottombar.bottombar_items.controls[0] = self.build()
        self.page.update()
        self.page.bottom_appbar.update()

    def set_track_position(self, e: ft.ControlEvent):
        if self.state == 'playing':
            self.audio.pause()
            self.slider.value = e.control.value
            self.audio.seek(int(self.slider.value))
            self.audio.resume()
        elif self.state == 'paused':
            self.play_pause_bttn.icon = ft.icons.PLAY_CIRCLE
            self.slider.value = e.control.value
        self.page.update()

    def change_slider_value(self, e: ft.Control):
        track_duration = self.audio.get_duration()
        track_dur_converted = self.convert_to_min_and_sec(track_duration)
        current_position = int(e.data)
        if track_duration - current_position <= 100:
            self.play_pause_bttn.icon = ft.icons.PLAY_CIRCLE
        current_pos_converted = self.convert_to_min_and_sec(current_position)

        self.current_position_text.value = f'{current_pos_converted[0]}:'
        self.current_position_text.value += f'{current_pos_converted[1]}'

        self.duration_text.value = f'{track_dur_converted[0]}:'
        self.duration_text.value += f'{track_dur_converted[1]}'

        self.slider.max = track_duration
        self.slider.value = e.data
        self.page.bottom_appbar.update()
        self.page.update()

    def convert_to_min_and_sec(self, value):
        total_seconds = value / 1000  # Переводим значение в секунды
        minutes = int(total_seconds // 60)  # Получаем количество минут
        seconds = int(total_seconds % 60)  # Получаем оставшиеся секунды
        seconds_formatted = str(seconds).zfill(2)
        return minutes, seconds_formatted

    def on_off_volume_slider(self):
        print('on/off')

    def set_track_volume(self, e: ft.ControlEvent):
        print(e.control.value)

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

    def build(self):
        middle_part = ft.Column(
            [
                self.name_text,
                ft.Row(
                    [
                        self.slider,
                        self.play_pause_bttn,
                        # ft.Column(
                        #     [
                        #         self.volume_slider,
                        #         self.volume_bttn,
                        #     ]
                        # )
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
        )
        # view_2 = ft.Container(
        #     content=self.volume_slider,
        #     alignment=ft.alignment.bottom_right,
        #     bgcolor=ft.colors.TRANSPARENT
        # )
        # view = ft.Column(
        #     [view_2, view_1]
        # )
        return view
