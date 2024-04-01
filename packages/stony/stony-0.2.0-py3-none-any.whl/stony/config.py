from typing import Optional
from pathlib import Path
from pydantic import BaseModel
from yaml import load as load_yaml, Loader as YamlLoader


class Config(BaseModel):
    root_page_id: str
    api_key: Optional[str] = None
    project_dir: Path = Path(".")
    path: str = "/"
    api_url: str = "https://api.notion.com/v1"

    def templates_dir(self):
        return self.project_dir / "templates"

    @property
    def out_dir(self):
        return self.project_dir / f"dist"


def load_config(project_dir: Path, api_key: Optional[str] = None) -> Config:
    with open(project_dir / "stony.yml") as fh:
        conf = load_yaml(fh, Loader=YamlLoader)
    return Config(**conf, project_dir=project_dir, api_key=api_key)
