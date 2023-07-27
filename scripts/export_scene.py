import argparse
from pathlib import Path

import pandas as pd
from loguru import logger

from annodict.resource import AnnoScene
from submodules.lanutils.fs.fs import parent_ensured_path


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--scene-id", type=Path, required=True)
parser.add_argument("-o", "--output-path", type=parent_ensured_path, required=True)
parser.add_argument("--api-server", default="http://localhost:5100")


def main(args):
    scene = AnnoScene.from_objectid(args.scene_id, args.api_server)
    with open(args.output_path, "w") as f:
        f.write(scene.export_html())


if __name__ == "__main__":
    main(parser.parse_args())
