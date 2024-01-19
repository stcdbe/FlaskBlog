from typing import Any
from uuid import UUID

from slugify import slugify

from src.utils import save_picture


def prepare_post_data(form_data: dict[str, Any], creator_id: UUID) -> dict[str, Any]:
    if form_data['picture']:
        pic_name = save_picture(picture=form_data['picture'],
                                img_catalog='postimages',
                                img_size=(900, 400))
        form_data['picture'] = pic_name
    else:
        form_data.pop('picture')

    for key, val in form_data.items():
        if isinstance(val, str):
            form_data[key] = val.strip()

    form_data['user_id'] = creator_id
    form_data['slug'] = slugify(text=form_data['title'])

    return form_data


def prepare_com_data(form_data: dict[str, Any],
                     post_id: UUID,
                     creator_id: UUID) -> dict[str, Any]:
    for key, val in form_data.items():
        if isinstance(val, str):
            form_data[key] = val.strip()

    form_data['post_id'] = post_id
    form_data['user_id'] = creator_id

    return form_data
