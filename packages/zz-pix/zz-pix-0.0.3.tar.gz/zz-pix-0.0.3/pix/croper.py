from pathlib import Path

from PIL import Image

from pix.utils import is_file_supported


def _calculate_crop_box_ratio(img_width, img_height, target_ratio, align):
    img_ratio = img_width / img_height
    if target_ratio > img_ratio:
        # Crop vertically
        new_height = int(img_width / target_ratio)
        vertical_start = _calculate_alignment_start(img_height, new_height, align)
        return (0, vertical_start, img_width, vertical_start + new_height)
    else:
        # Crop horizontally
        new_width = int(img_height * target_ratio)
        horizontal_start = _calculate_alignment_start(img_width, new_width, align)
        return (horizontal_start, 0, horizontal_start + new_width, img_height)


def _calculate_alignment_start(total_length, new_length, align):
    if align in ["top", "left"]:
        return 0
    elif align in ["bottom", "right"]:
        return total_length - new_length
    else:  # Center or unspecified
        return (total_length - new_length) // 2


def _crop_image_by_ratio(img, ratio, align):
    target_ratio = float(ratio.split(":")[0]) / float(ratio.split(":")[1])
    box = _calculate_crop_box_ratio(img.width, img.height, target_ratio, align)
    return img.crop(box)


def _crop_image_by_size(img, size_str):
    w, h, x, y = map(int, size_str.replace("x", "+").split("+"))
    box = (x, y, x + w, y + h)
    return img.crop(box)


def crop_image(input_path, output_path, overwrite, **crop_options):
    """crop an image based on the specified options

    Args:
        `input_path` (pathlib.Path): input image to crop
        `output_path` (pathlib.Path): output image path
        `overwrite` (bool): overwrite existing file

    Keyword Arguments:
        `ratio` (str): aspect ratio (W:H). Combine with `align`
        `size` (str): exact size and position as WxH+X+Y (e.g., 800x600+100+150)
        `align` (str): alignment (default: "center") (default: "center")

    Raises:
        ValueError: if neither `ratio` nor `size` is specified
    """

    # create directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    img = Image.open(input_path)
    if "ratio" in crop_options and crop_options["ratio"]:
        cropped_img = _crop_image_by_ratio(
            img, crop_options["ratio"], crop_options.get("align", "center")
        )
    elif "size" in crop_options and crop_options["size"]:
        cropped_img = _crop_image_by_size(img, crop_options["size"])
    else:
        raise ValueError("Either `--ratio` or `--size` must be specified")

    if overwrite or not Path(output_path).exists():
        cropped_img.save(output_path)
        print(
            f"Image saved to {output_path}, ratio: {crop_options.get('ratio', 'N/A')}, align: {crop_options.get('align', 'N/A')}, crop_box: {crop_options.get('size', 'N/A')}"
        )
    else:
        print(f"File {output_path} already exists. Use `--overwrite` to replace it.")


def crop_images(input_dir, output_dir, overwrite, **crop_options):
    """crop a list of images based on the specified options

    Args:
        `input_dir` (pathlib.Path): input directory containing images to crop
        `output_dir` (pathlib.Path): output directory to save cropped images
        `overwrite` (bool): overwrite existing files

    Keyword Arguments:
        `ratio` (str): aspect ratio (W:H). Combine with `align`
        `size` (str): exact size and position as WxH+X+Y (e.g., 800x600+100+150)
        `align` (str): alignment (default: "center") (default: "center")
    """
    for file in input_dir.iterdir():
        if file.is_file() and is_file_supported(file):
            output_file = Path(output_dir, file.name)
            crop_image(file, output_file, overwrite, **crop_options)
