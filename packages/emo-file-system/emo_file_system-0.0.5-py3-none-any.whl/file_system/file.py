import os
import json
import shutil
from typing import Dict, List, Union


class File:

    @classmethod
    def create_file_directory(cls, file_path: str):
        directory = os.path.dirname(file_path)
        cls.create_directory(directory)

    @staticmethod
    def create_directory(path: str):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def exists(path: str) -> bool:
        return os.path.exists(path)

    @classmethod
    def remove(cls, path: str):
        if cls.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    @staticmethod
    def read_lines(
        filepath: str,
        mode: str = "r",
        encoding: str = "utf-8"
    ) -> Union[List, Dict]:
        with open(filepath, mode, encoding=encoding) as f:
            return f.readlines()

    @staticmethod
    def read(filepath: str, mode: str = "r", encoding: str = "utf-8"):
        with open(filepath, mode, encoding=encoding if mode == "r" else None) as f:
            return f.read()

    @staticmethod
    def read_json(filepath: str, mode: str = "r", encoding: str = "utf-8"):
        with open(filepath, mode, encoding=encoding if mode == "r" else None) as f:
            return json.load(f)

    @staticmethod
    def write_lines(
        filepath: str,
        lines: list,
        mode: str = "w",
        encoding: str = "utf-8"
    ):
        with open(filepath, mode, encoding=encoding) as f:
            f.writelines(lines)

    @staticmethod
    def write_json(
        filepath: str,
        lines: list,
        mode: str = "w",
        encoding: str = "utf-8"
    ):
        with open(filepath, mode, encoding=encoding) as f:
            json.dump(lines, f, ensure_ascii=False)

    @staticmethod
    def get_filename(path, without_extentsion: bool = False) -> str:
        filename = os.path.basename(path)

        if not without_extentsion:
            return filename

        return os.path.splitext(filename)[0]


file = "C:\\Users\\emozdal\\code\\python-packages\\file-system\\Pipfile.lock"
print(File.get_filename(file, without_extentsion=True))
