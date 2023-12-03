from typing import Any

from src.utils import save_picture


def serialize_post_form(form_data: dict[str, Any]) -> dict[str, Any]:
    form_data.pop('submit')
    form_data.pop('csrf_token')

    if form_data['picture']:
        pic_name = save_picture(picture=form_data['picture'], img_catalog='postimages', size=(900, 400))
        form_data['picture'] = pic_name
    else:
        form_data.pop('picture')

    for key, val in form_data.items():
        if isinstance(val, str):
            form_data[key] = val.strip()

    return form_data


def serialize_com_form(form_data: dict[str, Any]) -> dict[str, Any]:
    form_data.pop('submit')
    form_data.pop('csrf_token')

    for key, val in form_data.items():
        if isinstance(val, str):
            form_data[key] = val.strip()

    return form_data
