import re
import json
import os
import sys
from typing import Optional
from pathlib import Path
from functools import cache
from jinja2 import FileSystemLoader, Environment
from stony.client import Client
from stony.config import Config


def urlize_title(title: str, config: Config):
    sep = re.sub("\W", "-", title).lower()
    sep = re.sub("(-)+", "-", sep)
    if sep.endswith("-"):
        sep = sep[:-1]
    return config.path + sep + ".html"


class Stony:
    def __init__(self, config: Config, client: Client):
        self.client = client
        self.config = config
        self.templates_searchpath = [
            self.config.templates_dir(),
            self.get_default_templates_dir(),
        ]
        self.template_loader = FileSystemLoader(searchpath=self.templates_searchpath)
        self.template_env = Environment(loader=self.template_loader)
        self.template_env.filters["url"] = lambda title: urlize_title(
            title, config=self.config
        )

    def get_default_templates_dir(self):
        module = sys.modules[__name__]
        module_path = os.path.dirname(module.__file__)
        return os.path.join(module_path, "templates")

    def get_template(self, name: str):
        return self.template_env.get_template(name)

    def render_template(self, name, **variables):
        template = self.get_template(name)
        return template.render(**variables, config=self.config)

    def write_json(self, data: dict, filepath: Path):
        outpath = self.config.out_dir / filepath
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, "w") as fh:
            json.dump(data, fh, indent=2)

    def write_page(self, url: str, data: str):
        outpath = self.config.out_dir / url
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, "w") as fh:
            fh.write(data)
        print("Wrote", url)

    def get_page(self, page_id: str) -> dict:
        page = self.client.get_page(page_id)
        self.write_json(page, f"pages/{page_id}.json")
        return page

    def get_block_children(self, block_id: str):
        result = self.client.get_block_children(block_id)
        self.write_json(result, f"block_children/{block_id}.json")
        return result

    def get_title_block(self, page: dict):
        return page["properties"]["title"]

    def build(self):
        root_page = self.get_page(self.config.root_page_id)
        root_page_content = self.get_block_children(self.config.root_page_id)
        title_block = self.get_title_block(root_page)
        index = self.render_template(
            "index.html", title=title_block, content=root_page_content["results"]
        )
        self.write_page("index.html", index)
        for block in root_page_content["results"]:
            if block["type"] == "child_page":
                article_content = self.get_block_children(block["id"])
                article = self.get_page(block["id"])
                article_title = article["properties"]["title"]["title"][0]["plain_text"]
                rendered_article = self.render_template(
                    "article.html", content=article_content["results"]
                )
                url = urlize_title(article_title, config=self.config)
                self.write_page(url, rendered_article)
