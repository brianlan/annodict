import argparse
from pathlib import Path

from loguru import logger

from annodict.resource import AnnoScene
from submodules.lanutils.fs.fs import parent_ensured_path


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--scene-id", type=Path, required=True)
parser.add_argument("-o", "--output-path", type=parent_ensured_path, required=True)
parser.add_argument("--api-server", default="http://localhost:5100")


def main(args):
    logger.info(f"Start loading scene {args.scene_id} from {args.api_server}")
    scene = AnnoScene.from_objectid(args.scene_id, args.api_server, embedded=True)
    logger.info(f"Scene {args.scene_id} loaded")

    if args.output_path.suffix == ".csv":
        scene.export_csv(args.output_path)
    elif args.output_path.suffix == ".html":
        scene.export_html(args.output_path)
    else:
        raise ValueError(f"Unknown output format: {args.output_path.suffix}")

    logger.info(f"Exported scene {args.scene_id} to {args.output_path}")


if __name__ == "__main__":
    main(parser.parse_args())
