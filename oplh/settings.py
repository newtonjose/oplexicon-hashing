from pathlib import PosixPath

from pydantic import BaseSettings


class Config(BaseSettings):
    opl_path: str
