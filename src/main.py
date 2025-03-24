import flet
import base64
import os
from io import BytesIO
from flet import (
    Page,
    FilePicker,
    Text,
    ElevatedButton,
    Row,
    Column,
    FilePickerResultEvent,
)

import readpdfutils as rpu
from PIL import Image


def main(page: Page):
    image1 = flet.Image(src="images/icon.png", fit=flet.ImageFit.SCALE_DOWN)
    props = {"page_no": 0, "path": ""}

    def select_file(e: FilePickerResultEvent):
        page.add(filepicker)
        filepicker.pick_files("Select file...")

    # 3) CREATE THE FUNCTION OF EVENT
    def return_file(e: FilePickerResultEvent):
        path = e.files[0].path
        props["path"] = path
        page_no = props["page_no"]
        s = ""
        if path.endswith(".pdf"):
            width = page.width
            b = rpu.get_page_for_display(page_no, path, width)
            w, h = rpu.get_page_size_for_display(page_no, path, width)
            img = Image.frombytes("RGBA", (w, h), b)
            buff = BytesIO()
            img.save(buff, format="PNG")
            newstring = base64.b64encode(buff.getvalue()).decode("utf-8")
            image1.src_base64 = newstring
            image1.update()
            s = f"image size ({img.width}, {img.height})"
        file_path.value = s
        file_path.update()
        page.update()

    def next_page(e):
        width = page.width
        props["page_no"] += 1
        page_no = props["page_no"]
        path = props["path"]
        update_image()

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



    row_filepicker = Row(vertical_alignment="center")
    file_path = Text(value="Selected file path", expand=1)
    # 1) CREATE A FILEPICKER:
    filepicker = FilePicker(on_result=return_file)

    row_filepicker.controls.append(
        ElevatedButton(text="Select file...", on_click=select_file)
    )
    # ADD THE PATH (if you will select it)
    row_filepicker.controls.append(file_path)

    page.add(row_filepicker)
    page.add(image1)
    page.add(flet.OutlinedButton(text="Next Page", on_click=next_page))


if __name__ == "__main__":
    flet.app(target=main)
