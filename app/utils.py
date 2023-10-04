import os
from secrets import token_hex

from PIL import Image
from werkzeug.datastructures.file_storage import FileStorage

from app import app, mail
from app.database.dbmodels import User


def savepicture(picture: FileStorage, imgcatalog: str, size: tuple[int, int]) -> str:
    newname = token_hex(12)
    _, ext = os.path.splitext(picture.filename)
    picname = newname + ext
    piclink = os.path.join(app.root_path, 'static', 'images', imgcatalog, picname)
    print(piclink)
    with Image.open(picture) as img:
        rgbimg = img.convert('RGB')
        resizedimg = rgbimg.resize(size)
        resizedimg.save(piclink)
    return picname


def deletepicture(imgcatalog: str, picname: str) -> None:
    if picname == 'default.jpg':
        return
    try:
        os.remove(os.path.join(app.root_path, 'static', 'images', imgcatalog, picname))
    except FileNotFoundError:
        return


def sendemail(subject: str, template: str, user: User, url: str) -> None:
    mail.send(subject=subject,
              html_template=f'email/{template}',
              receivers=[user.email],
              body_params=dict(user=user, url=url))
