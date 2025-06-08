import flet as ft
import base64
from io import BytesIO
from dataclasses import dataclass
import reflow
import djvulib
import cv2
import os
import shutil
import fastrlsa

import readpdfutils as rpu
from PIL import Image
from typing import Optional


@dataclass
class Props:
    page_no: int
    path: str
    image: str
    kind: str
    img: Optional[Image.Image]
    reflowed_image: Optional[Image.Image]
    reflowed : bool
    page_count: int

@dataclass
class MyObjects:
    bar: ft.ProgressRing


def main(page: ft.Page):
    pr = ft.ProgressRing(width = 50, height = 50, stroke_width=2)
    pr.visible = False
    myobjects = MyObjects(pr)
    page.window.frameless = False
    initial_page_count = page.client_storage.get("page_count") if page.client_storage.contains_key("page_count") else 0
    initial_path = page.client_storage.get("path") if page.client_storage.contains_key("path") else ""
    initial_page_no = (
        page.client_storage.get("page_no")
        if page.client_storage.contains_key("page_no")
        else 0
    )
    initial_kind = (
        page.client_storage.get("kind")
        if page.client_storage.contains_key("kind")
        else ""
    )
    initial_image = page.client_storage.get("image") if page.client_storage.contains_key("image") else "images/icon.png"
    image1 = ft.Image(src=initial_image, fit=ft.ImageFit.FIT_WIDTH)
    
    props = Props(initial_page_no, initial_path, initial_image, initial_kind, None, None, False, initial_page_count)

    def select_file(e: ft.FilePickerResultEvent):
        page.add(filepicker)
        filepicker.pick_files("Select file...")

    # 3) CREATE THE FUNCTION OF EVENT
    def return_file(e: ft.FilePickerResultEvent):
        path = e.files[0].path
        app_data_path = os.getenv("FLET_APP_STORAGE_DATA")
        basename = os.path.basename(path)
        my_file_path = os.path.join(app_data_path, basename)
        shutil.copy(path, my_file_path)
        page.client_storage.set("path", my_file_path)
        props.path = my_file_path
        props.page_no = 0
        page.client_storage.set("page_no", 0)
        page_no = props.page_no
        s = ""
        if path.endswith(".pdf"):
            props.kind = "pdf"
            page.client_storage.set("kind", "pdf")
            update_image(page_no, path)
        elif path.endswith(".djvu"):
            props.kind = "djvu"
            page.client_storage.set("kind", "djvu")
            update_image_djvu(page_no, path)
        s = f"{basename}"
        file_path.value = s
        file_path.update()
        page.update()

    def prev_page(e):
        if props.page_no > 0:
            props.page_no -= 1
            page_no = props.page_no
            page.client_storage.set("page_no", page_no)
            path = props.path
            if props.kind == "pdf":
                update_image(page_no, path)
            elif props.kind == "djvu":
                update_image_djvu(page_no, path)

    def next_page(e):
        column.scroll_to(0)
        if props.page_no + 1 < props.page_count:
            props.page_no += 1
            page_no = props.page_no
            page.client_storage.set("page_no", page_no)
            path = props.path
            if props.kind == "pdf":
                update_image(page_no, path)
            elif props.kind == "djvu":
                update_image_djvu(page_no, path)


    def update_image_djvu(page_no, path):
        if props.page_count == 0:
            props.page_count = djvulib.get_number_of_pages(path)
        arr = djvulib.get_image_as_arrray(page_no, path)
        _, bw = cv2.threshold(arr, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        img = Image.fromarray(bw, "L")
        buff = BytesIO()
        img.save(buff, format="PNG")
        props.img = img
        newstring = base64.b64encode(buff.getvalue()).decode("utf-8")
        app_data_path = os.getenv("FLET_APP_STORAGE_DATA")
        current_page_image_path = os.path.join(app_data_path, "page.png")
        page.client_storage.set("image", current_page_image_path)
        page.client_storage.set("page_count", props.page_count)
        img.save(current_page_image_path, format="PNG")
        image1.src_base64 = newstring
        image1.fit = ft.ImageFit.FIT_WIDTH
        image1.update()

    def update_image(page_no, path):
        width = page.width * 2
        if props.page_count == 0:
            props.page_count = rpu.get_page_count(path)
        b = rpu.get_page_for_display(page_no, path, width)
        w, h = rpu.get_page_size_for_display(page_no, path, width)
        img = Image.frombytes("RGBA", (w, h), b)
        buff = BytesIO()
        img.save(buff, format="PNG")
        props.img = img
        app_data_path = os.getenv("FLET_APP_STORAGE_DATA")
        current_page_image_path = os.path.join(app_data_path, "page.png")
        page.client_storage.set("image", current_page_image_path)
        page.client_storage.set("page_count", props.page_count)
        img.save(current_page_image_path, format="PNG")
        newstring = base64.b64encode(buff.getvalue()).decode("utf-8")
        image1.src_base64 = newstring
        image1.fit = ft.ImageFit.FIT_WIDTH
        image1.update()

    def reflow_image(e):
        try:
            myobjects.bar.visible = True
            myobjects.bar.update()
            if not props.reflowed:
                img = props.img
                new_image = reflow.reflow(img)
                buff = BytesIO()
                new_image.save(buff, format="PNG")
                props.reflowed_image = new_image
                newstring = base64.b64encode(buff.getvalue()).decode("utf-8")
                image1.src_base64 = newstring
                image1.fit = ft.ImageFit.FIT_WIDTH
                image1.update()
                props.reflowed = True
            else:
                buff = BytesIO()
                props.img.save(buff, format="PNG")
                newstring = base64.b64encode(buff.getvalue()).decode("utf-8")
                image1.src_base64 = newstring
                image1.fit = ft.ImageFit.FIT_WIDTH
                image1.update()
                props.reflowed = False

        except Exception as e:
            file_path.value = str(e)
            file_path.update()
        finally:
            myobjects.bar.visible = False
            myobjects.bar.update()


    first_row = ft.Row(alignment="center")
    txt_field = ft.Text(value="Reflow-App", expand=1)
    first_row.controls.append(txt_field)
    row_filepicker = ft.Row(alignment="center")
    file_path = ft.Text(value="Selected file path", expand=1)
    filepicker = ft.FilePicker(on_result=return_file)

    row_filepicker.controls.append(
        ft.ElevatedButton(text="Select file...", on_click=select_file)
    )
    row_filepicker.controls.append(file_path)
    prev_button = ft.OutlinedButton(text="Prev Page", on_click=prev_page)
    next_button = ft.OutlinedButton(text="Next Page", on_click=next_page)
    reflow_button = ft.OutlinedButton(text="Reflow/Unflow", on_click=reflow_image)
    images = ft.Row(expand=1, wrap=False, scroll="always")
    buttons = ft.Row(expand=1, wrap=False)
    buttons.controls.append(prev_button)
    buttons.controls.append(next_button)
    buttons.controls.append(reflow_button)
    images.controls.append(image1)
    st = ft.Stack([image1, pr])
    column = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            expand=1,
            controls=[
                first_row,
                row_filepicker,
                st,
                buttons,
            ],
        )
    page.add(
        column
    )


if __name__ == "__main__":
    ft.app(target=main, upload_dir="assets/uploads")
