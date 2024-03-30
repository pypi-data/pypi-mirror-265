import os
from pathlib import Path

from pydantic_settings import BaseSettings

current_working_directory = Path.cwd()

filepath = os.path.join(os.path.dirname(__file__), "models")


class Settings(BaseSettings):
    API_KEY: str = "some_secret"
    MODELS_PATH: str = filepath
