from PIL import Image


def prune_image(input_file, resolution, dry_run=False):
    size = (0, 0)
    with Image.open(input_file) as im:
        size = im.size

    res = tuple(map(int, resolution.split("x")))

    if size < res:
        if dry_run:
            print(f"Would have removed {input_file}")
        else:
            input_file.unlink()
            print(f"Removed {input_file}")


def prune_images(input_dir, resolution, dry_run=False):
    for file in input_dir.iterdir():
        if file.is_file():
            prune_image(file, resolution, dry_run)
