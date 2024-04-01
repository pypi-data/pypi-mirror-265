from dotenv import load_dotenv
import os
from pathlib import Path
import click
from click import option, group
from stony import Stony, Config, Client, load_config


@group()
def cli():
    "Static site generator powered by Notion"
    load_dotenv()


@cli.command
@option(
    "--out",
    "-o",
    default="dist",
    help="Directory to build the site. Default `dist`",
    type=click.Path(path_type=Path),
)
@option(
    "--project-dir",
    default=os.getcwd(),
    help="Directory containg the stony project",
    type=click.Path(path_type=Path),
    envvar="STONY_PROJECT_DIR",
)
@option(
    "--api-key",
    help="Notion API key",
    envvar="NOTION_API_KEY",
)
def build(out, project_dir, api_key):
    """
    Build the site
    """

    print(project_dir, out)
    config = load_config(project_dir, api_key=api_key)
    client = Client(config=config)
    stony = Stony(client=client, config=config)
    print(f"Building into {config.out_dir}")
    stony.build()
