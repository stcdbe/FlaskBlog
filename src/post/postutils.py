from typing import Any
from uuid import UUID

from src.database.enums import PostGroup
from src.utils import save_picture


def prepare_post_data(form_data: dict[str, Any],
                      post_group: PostGroup,
                      creator_id: UUID) -> dict[str, Any]:
    for key in ['submit', 'csrf_token']:
        if key in form_data:
            form_data.pop(key)

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

    form_data['group'] = post_group
    form_data['user_id'] = creator_id

    return form_data


def prepare_com_data(form_data: dict[str, Any],
                     post_id: UUID,
                     creator_id: UUID) -> dict[str, Any]:
    for key in ['submit', 'csrf_token']:
        if key in form_data:
            form_data.pop(key)

    for key, val in form_data.items():
        if isinstance(val, str):
            form_data[key] = val.strip()

    form_data['post_id'] = post_id
    form_data['user_id'] = creator_id

    return form_data
