import flet as ft
import base64
from io import BytesIO
from dataclasses import dataclass


import readpdfutils as rpu
from PIL import Image


@dataclass
class Props:
    page_no: int
    path: str




def main(page: ft.Page):
    page.window.frameless = False
    image1 = ft.Image(src="images/icon.png", fit=ft.ImageFit.NONE)
    props = Props(0, "")

    def select_file(e: ft.FilePickerResultEvent):
        page.add(filepicker)
        filepicker.pick_files("Select file...")

    # 3) CREATE THE FUNCTION OF EVENT
    def return_file(e: ft.FilePickerResultEvent):
        path = e.files[0].path
        props.path = path
        page_no = props.page_no
        s = ""
        if path.endswith(".pdf"):
            update_image(page_no, path)
            s = f"{path}"
        file_path.value = s
        file_path.update()
        page.update()

    def prev_page(e):
        if props.page_no > 0:
            props.page_no -= 1
            page_no = props.page_no
            path = props.path
            update_image(page_no, path)

    def next_page(e):
        props.page_no += 1
        page_no = props.page_no
        path = props.path
        update_image(page_no, path)

    def update_image(page_no, path):
        width = page.width
        b = rpu.get_page_for_display(page_no, path, width)
        w, h = rpu.get_page_size_for_display(page_no, path, width)
        img = Image.frombytes("RGBA", (w, h), b)
        buff = BytesIO()
        img.save(buff, format="PNG")
        newstring = base64.b64encode(buff.getvalue()).decode("utf-8")
        image1.src_base64 = newstring
        image1.update()

    row_filepicker = ft.Row(vertical_alignment="center")
    file_path = ft.Text(value="Selected file path", expand=1)
    filepicker = ft.FilePicker(on_result=return_file)

    row_filepicker.controls.append(
        ft.ElevatedButton(text="Select file...", on_click=select_file)
    )
    row_filepicker.controls.append(file_path)
    prev_button = ft.OutlinedButton(text="Prev Page", on_click=prev_page)
    next_button = ft.OutlinedButton(text="Next Page", on_click=next_page)
    images = ft.Row(expand=1, wrap=False, scroll="always")
    buttons = ft.Row(expand=1, wrap=False)
    buttons.controls.append(prev_button)
    buttons.controls.append(next_button)
    images.controls.append(image1)
    page.add(
        ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            expand=1,
            controls=[
                row_filepicker,
                images,
                buttons,
            ],
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
