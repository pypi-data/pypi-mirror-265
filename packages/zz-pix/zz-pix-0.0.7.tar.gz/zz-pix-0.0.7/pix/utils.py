import json
import pathlib


def get_supported_formats(str=False):

    supported_formats = ["png", "jpeg", "webp", "avif", "heif", "tiff", "bmp", "ico"]
    if str:
        return ", ".join(supported_formats)
    else:
        return supported_formats


def is_file_supported(file):
    supported_formats = get_supported_formats()
    ext = pathlib.Path(file).suffix
    ext = ext[1:]
    if ext == "jpg":
        ext = "jpeg"
    return ext in supported_formats


def get_manifest():
    root_dir = pathlib.Path(__file__).parent.absolute()
    manifest_path = pathlib.Path.joinpath(root_dir, "manifest.json")
    with open(manifest_path, "r") as f:
        return json.load(f)
