import os

import flet as ft
import httpx

API_URL = os.getenv("API_URL", "http://localhost:8888")
ACCENT = "#7C5CFF"
BG = "#0F1020"
CARD = "#181A2E"
MUTED = "#8A8FB0"


async def shorten(real_link: str, custom_len: int | None) -> str:
    payload: dict = {"real_link": real_link}
    if custom_len:
        payload["custom_len"] = custom_len

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(f"{API_URL}/make_short", json=payload)

    if resp.status_code == 200:
        return resp.json()["short"]
    if resp.status_code == 422:
        raise ValueError("Некорректная ссылка. Пример: https://example.com")
    raise ValueError("Сервер не смог сократить ссылку. Попробуйте ещё раз.")


def main(page: ft.Page):
    page.title = "Taker Links"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG
    page.padding = 24
    page.window.width = 560
    page.window.height = 760
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO

    clipboard = ft.Clipboard()
    launcher = ft.UrlLauncher()
    page.services.extend([clipboard, launcher])

    history: list[tuple[str, str]] = []

    def toast(text: str, error: bool = False):
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(text),
                bgcolor="#B3261E" if error else "#2E7D32",
            )
        )

    url_field = ft.TextField(
        label="Длинная ссылка",
        hint_text="https://example.com/very/long/link",
        prefix_icon=ft.Icons.LINK,
        border_radius=14,
        border_color="#2A2D4A",
        focused_border_color=ACCENT,
        bgcolor="#12132A",
        autofocus=True,
    )

    len_label = ft.Text("Длина хеша: 6", color=MUTED, size=13)
    len_slider = ft.Slider(
        min=4,
        max=16,
        divisions=12,
        value=6,
        active_color=ACCENT,
        label="{value}",
    )

    def on_len_change(e):
        len_label.value = f"Длина хеша: {int(len_slider.value)}"
        page.update()

    len_slider.on_change = on_len_change

    result_box = ft.Container(visible=False)
    history_col = ft.Column(spacing=8)
    history_box = ft.Container(visible=False)

    submit_btn = ft.FilledButton(
        "Сократить",
        icon=ft.Icons.BOLT,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ACCENT,
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=14),
        ),
    )
    loader = ft.ProgressRing(width=20, height=20, stroke_width=2, visible=False)

    async def copy(short: str):
        await clipboard.set(short)
        toast("Ссылка скопирована")

    async def open_link(short: str):
        await launcher.launch_url(short)

    def short_row(short: str, original: str, big: bool = False) -> ft.Control:
        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            short,
                            size=18 if big else 14,
                            weight=ft.FontWeight.W_600,
                            color=ACCENT if big else "#E6E8FF",
                            selectable=True,
                        ),
                        ft.Text(
                            original,
                            size=12,
                            color=MUTED,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.IconButton(
                    ft.Icons.CONTENT_COPY,
                    tooltip="Копировать",
                    on_click=lambda e, s=short: page.run_task(copy, s),
                ),
                ft.IconButton(
                    ft.Icons.OPEN_IN_NEW,
                    tooltip="Открыть",
                    on_click=lambda e, s=short: page.run_task(open_link, s),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def render(short: str, original: str):
        result_box.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Готово!", size=12, color=MUTED),
                    short_row(short, original, big=True),
                ],
                spacing=6,
            ),
            padding=18,
            border_radius=16,
            bgcolor=CARD,
            border=ft.Border.all(1, ACCENT),
        )
        result_box.visible = True

        history.insert(0, (short, original))
        del history[8:]
        history_col.controls = [short_row(s, o) for s, o in history]
        history_box.visible = True

    async def on_submit(e):
        link = (url_field.value or "").strip()
        if not link:
            url_field.error = "Вставьте ссылку"
            page.update()
            return
        if not link.startswith(("http://", "https://")):
            link = "https://" + link

        url_field.error = None
        submit_btn.disabled = True
        loader.visible = True
        page.update()

        try:
            short = await shorten(link, int(len_slider.value))
            render(short, link)
        except httpx.ConnectError:
            toast("Нет связи с API. Запущен ли сервер на :8888?", error=True)
        except ValueError as err:
            toast(str(err), error=True)
        except Exception:
            toast("Что-то пошло не так", error=True)
        finally:
            submit_btn.disabled = False
            loader.visible = False
            page.update()

    submit_btn.on_click = on_submit
    url_field.on_submit = on_submit

    history_box.content = ft.Column(
        [
            ft.Text("Недавние", size=13, color=MUTED, weight=ft.FontWeight.W_600),
            ft.Container(
                content=history_col,
                padding=14,
                border_radius=16,
                bgcolor=CARD,
            ),
        ],
        spacing=8,
    )

    page.add(
        ft.Container(
            width=480,
            content=ft.Column(
                [
                    ft.Container(height=12),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.LINK, color=ACCENT, size=34),
                            ft.Text("Taker Links", size=30, weight=ft.FontWeight.W_800),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(
                        "Сокращатель ссылок в экосистеме Taker",
                        color=MUTED,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=8),
                    ft.Container(
                        content=ft.Column(
                            [
                                url_field,
                                ft.Column([len_label, len_slider], spacing=0),
                                ft.Row(
                                    [submit_btn, loader],
                                    spacing=14,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ],
                            spacing=14,
                        ),
                        padding=20,
                        border_radius=20,
                        bgcolor=CARD,
                    ),
                    result_box,
                    history_box,
                ],
                spacing=16,
            ),
        )
    )


if __name__ == "__main__":
    if os.getenv("UI_WEB"):
        ft.run(
            main,
            view=ft.AppView.WEB_BROWSER,
            host="0.0.0.0",
            port=int(os.getenv("UI_PORT", "8550")),
        )
    else:
        ft.run(main, view=ft.AppView.WEB_BROWSER)
