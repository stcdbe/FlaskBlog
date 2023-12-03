import os
from uuid import uuid4

from PIL import Image
from werkzeug.datastructures.file_storage import FileStorage

from src import app, mail
from src.database.dbmodels import User


def save_picture(picture: FileStorage,
                 img_catalog: str,
                 size: tuple[int, int]) -> str:
    _, ext = os.path.splitext(picture.filename)
    pic_name = str(uuid4()) + ext
    pic_link = os.path.join(app.root_path, 'static', 'images', img_catalog, pic_name)
    with Image.open(picture) as img:
        rgb_img = img.convert('RGB')
        resized_img = rgb_img.resize(size)
        resized_img.save(pic_link)
    return pic_name


def delete_picture(pic_name: str, img_catalog: str) -> None:
    match pic_name:
        case 'default.jpg':
            return
        case _:
            pic_link = os.path.join(app.root_path, 'static', 'images', img_catalog, pic_name)
            try:
                os.remove(pic_link)
            except FileNotFoundError:
                return


def send_email(subject: str,
               template: str,
               user: User,
               url: str) -> None:
    mail.send(subject=subject,
              html_template='email/' + template,
              receivers=[user.email],
              body_params={'user': user, 'url': url})
