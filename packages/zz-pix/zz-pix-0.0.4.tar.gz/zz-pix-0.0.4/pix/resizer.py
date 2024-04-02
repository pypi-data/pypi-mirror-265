import pathlib

from PIL import Image

from pix.utils import is_file_supported


def _save_image(image, output_path, overwrite=False):
    """
    Saves the image to the specified path, with an option to overwrite existing files.
    """
    if not overwrite and pathlib.Path(output_path).exists():
        print(f"File '{output_path}' already exists. Use `--overwrite` to replace it.")
        return
    image.save(output_path)
    print(f"Image saved to '{output_path}'.")


def resize_image(input_path, output_path, size=None, scale=None, overwrite=False):
    """
    Resizes an image based on a specified size or scale factor.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as img:
        if size:
            new_size = tuple(map(int, size.split("x")))
        elif scale:
            new_size = tuple([int(dim * scale) for dim in img.size])
        else:
            raise ValueError("Either size or scale must be specified for resizing.")

        resized_img = img.resize(new_size, resample=Image.NEAREST)

        _save_image(resized_img, output_path, overwrite)


def resize_images(input_dir, output_dir, size=None, scale=None, overwrite=False):
    """
    Resizes a directory of images based on a specified size or scale factor.
    """
    for file in input_dir.iterdir():
        if file.is_file() and is_file_supported(file):
            output_file = pathlib.Path.joinpath(output_dir, file.name)
            resize_image(file, output_file, size, scale, overwrite)
