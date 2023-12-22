from typing import Any

from src.utils import save_picture


def serialize_profile_form(form_data: dict[str, Any]) -> dict[str, Any]:
    form_data.pop('submit')
    form_data.pop('csrf_token')

    if form_data['picture']:
        pic_name = save_picture(picture=form_data['picture'],
                                img_catalog='profileimages',
                                size=(250, 250))
        form_data['picture'] = pic_name
    else:
        form_data.pop('picture')

    for key, val in form_data.items():
        if isinstance(val, str):
            form_data[key] = val.strip()

    return form_data
