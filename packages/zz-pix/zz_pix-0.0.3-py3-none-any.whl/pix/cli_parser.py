import argparse

from pix import utils


# fmt: off
def get_parser():
    manifest = utils.get_manifest()

    parser = argparse.ArgumentParser(description=f"{manifest['description']} ({manifest['version']})")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {manifest['version']}")
    subparser = parser.add_subparsers(dest="command", help="Command to execute")

    # convert command
    convert_parser = subparser.add_parser("convert", help="Convert images to a different format")
    convert_parser.add_argument("input", type=str, help="Input image or directory")
    convert_parser.add_argument("-o", "--output", type=str, help="Output image or directory (default: .)", default=".")
    convert_parser.add_argument("-f","--format",type=str,choices=utils.get_supported_formats(),help=f"Output format [{utils.get_supported_formats(True)}]",)
    convert_parser.add_argument("-q", "--quality", type=int, help="Output quality (0-100)", default=95)
    convert_parser.add_argument("--no-optimize", action="store_true", help="Disable optimization")
    convert_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    convert_parser.add_argument("--prefix", type=str, help="Prefix for the output file name", default="")
    convert_parser.add_argument("--surfix", type=str, help="Surfix for the output file name", default="")

    # resize command
    resize_parser = subparser.add_parser("resize", help="Resize images")
    resize_parser.add_argument("input", type=str, help="Input image or directory")
    resize_parser.add_argument("-o", "--output", type=str, help="Output image or directory", default=".")
    resize_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    resize_group = resize_parser.add_mutually_exclusive_group()
    resize_group.add_argument("--size", type=str, help="Output size (WxH)")
    resize_group.add_argument("--scale", type=float, help="Output scale (0.0-1.0)")

    # crop command
    crop_parser = subparser.add_parser("crop", help="Crop images")
    crop_parser.add_argument("input", type=str, help="Input image or directory")
    crop_parser.add_argument("-o", "--output", type=str, help="Output image or directory", default=".")
    crop_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    crop_group = crop_parser.add_mutually_exclusive_group()
    crop_group.add_argument("--ratio", type=str, help="Aspect ratio (W:H). Combine with --align")
    crop_group.add_argument("--size", type=str, help="Exact size and position as WxH+X+Y (e.g., 800x600+100+150)",)
    crop_parser.add_argument("--align", type=str, choices=["top", "bottom", "left", "right", "center"], help="Alignment (top, bottom, left, right, center)")

    # prune command
    prune_parser = subparser.add_parser("prune", help="Remove images smaller than specified resolution")
    prune_parser.add_argument("input", type=str, help="Input image or directory")
    prune_parser.add_argument("-r", "--resolution", type=str, help="Minimum resolution as WxH. Images smaller than this will be removed.")
    prune_parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without deleting files.")
    return parser
# fmt: on
