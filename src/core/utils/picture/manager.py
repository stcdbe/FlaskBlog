import logging
from pathlib import Path
from secrets import token_urlsafe
from typing import Literal

from PIL import Image
from werkzeug.datastructures import FileStorage

from src.config.enviroment import env


class PictureManager:
    def generate_rel_pic_path(self, img_catalog: Literal["postimg", "userimg"], filename: str) -> str:
        ext = Path(filename).suffix
        pic_name = token_urlsafe(32) + ext
        return str(Path("/static/img") / img_catalog / pic_name)

    def generate_abs_pic_path(self, rel_pic_path: str) -> str:
        return str(env.BASE_DIR / "src" / rel_pic_path[1:])

    def create_one(
        self,
        pic_file: FileStorage,
        rel_pic_path: str,
        pic_size: tuple[int, int],
    ) -> None:
        abs_pic_path = self.generate_abs_pic_path(rel_pic_path=rel_pic_path)

        with Image.open(pic_file) as img:
            img = img.convert(mode="RGB")
            img = img.resize(size=pic_size)
            img.save(fp=abs_pic_path)

    def delete_one(self, rel_pic_path: str) -> None:
        if rel_pic_path.endswith("default.jpg"):
            return

        abs_pic_path = self.generate_abs_pic_path(rel_pic_path=rel_pic_path)
        try:
            Path(abs_pic_path).unlink()
        except FileNotFoundError:
            logging.warning("Attempt to delete a non-existent file: %s", rel_pic_path)
