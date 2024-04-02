import pathlib
import shutil

import pillow_avif  # noqa
from PIL import Image
from pillow_heif import register_heif_opener

from pix.utils import is_file_supported


def _validate_target_format(out, target_format):
    """
    Validates that a target format is provided when the output is a directory.
    """
    if not target_format:
        raise ValueError(
            "Format is required when 'out' is a directory. Use '--format' or '-f' option."
        )


def _get_filename_and_extension(file_path):
    """
    Extracts the file name without extension and the file extension.
    """
    path = pathlib.Path(file_path)
    return path.stem, path.suffix[1:]


def convert_file(
    input_file: pathlib.Path,
    output_file: pathlib.Path,
    prefix="",
    surfix="",
    quality=95,
    optimize=True,
    overwrite=False,
):
    """
    Converts an input file to a specified target format and saves it to the specified output location.
    """
    register_heif_opener()

    # Load and convert the image
    im = Image.open(input_file).convert("RGB")
    output_filename, output_ext = _get_filename_and_extension(output_file)
    if output_ext == "jpg":
        output_ext = "jpeg"
    output_path = pathlib.Path.joinpath(
        output_file.parent, prefix + f"{output_filename}" + surfix + f".{output_ext}"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if the output file already exists
    if output_path.exists() and not overwrite:
        print(f"`{output_path}` already exists. Use `--overwrite` to replace.")
        return

    im.save(output_path, format=output_ext, quality=quality, optimize=optimize)
    print(f"Image saved to {output_path}, quality: {quality}, optimize: {optimize}")


def convert_files(
    input_dir,
    out_dir,
    target_format,
    prefix="",
    surfix="",
    quality=95,
    optimize=True,
    overwrite=False,
):
    """
    Converts a list of input files to a specified target format and saves them to the specified output location.
    """
    register_heif_opener()

    _validate_target_format(out_dir, target_format)
    for file in input_dir.iterdir():
        if file.is_file() and is_file_supported(file):

            input_file_name, input_file_extension = _get_filename_and_extension(file)
            if input_file_extension == f".{target_format}":
                print(
                    f"[WARNING] Skipping {input_file_name} as it is already in the target format."
                )
                shutil.move(file, f"{out_dir}")
                return
            output_file = pathlib.Path(f"{out_dir}/{input_file_name}.{target_format}")
            convert_file(
                file, output_file, prefix, surfix, quality, optimize, overwrite
            )
