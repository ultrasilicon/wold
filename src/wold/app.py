from wold.config import Config
from wold.server import Server
from wold.client import Client

import typer


def app(
    config_file: str = typer.Option(..., '--config','-c', help='Config file')
):
    """
    wold - YAML configed WoL daemon that wakes up boxes from Internet without DDNS

    For documents, see https://github.com/ultrasilicon/wold.
    """
    config = Config(config_file)
    if config.mode == 'server':
        server = Server(config)
        server.start()
    elif config.mode == 'client':
        client = Client(config)
        client.start()
        

def main():
    typer.run(app)