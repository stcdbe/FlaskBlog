from typing import Any

from src.utils import save_picture


def prepare_profile_data(form_data: dict[str, Any]) -> dict[str, Any]:
    for key in ['submit', 'csrf_token']:
        if key in form_data:
            form_data.pop(key)

    if form_data.get('picture'):
        pic_name = save_picture(picture=form_data['picture'],
                                img_catalog='profileimages',
                                img_size=(250, 250))
        form_data['picture'] = pic_name
    else:
        form_data.pop('picture')

    for key, val in form_data.items():
        if isinstance(val, str):
            form_data[key] = val.strip()

    return form_data
