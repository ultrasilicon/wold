from wold.utils import Utils

import sys
from ruamel.yaml import YAML


class Config():
    def __init__(self, path):
        raw = Utils.readall(path)
        yaml = YAML(typ="safe")
        parsed = yaml.load(raw)

        self.mode = parsed['mode']
        if parsed['mode'] == 'server':
            self.ws_port = parsed['ws_port']
            self.http_port = parsed['http_port']
        elif parsed['mode'] == 'client':
            self.host = parsed['host']
            self.port = parsed['port']
            self.inventory = dict(
                map(lambda inv: (inv['name'],inv['mac']), parsed['inventory']))
        else:
            Utils.log(f'Unknown operating mode {self.mode}',
                'To see help, use --help', 'fatal')

