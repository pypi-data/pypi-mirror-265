import pathlib
import traceback

from pix import cli_parser, converter, croper, prune, resizer


def get_io_paths(args):
    file_input = pathlib.Path(args.input)
    file_output = pathlib.Path(args.output)
    return file_input, file_output


def convert_cmd(args):
    file_input, file_output = get_io_paths(args)
    if file_input.is_file():
        converter.convert_file(
            file_input,
            file_output,
            args.prefix,
            args.surfix,
            args.quality,
            not args.no_optimize,
            args.overwrite,
        )
    elif file_input.is_dir():
        converter.convert_files(
            file_input,
            file_output,
            args.format,
            args.prefix,
            args.surfix,
            args.quality,
            not args.no_optimize,
            args.overwrite,
        )
    else:
        raise FileNotFoundError(f"`{args.input}` not found.")


def resize_cmd(args):
    file_input, file_output = get_io_paths(args)
    if file_input.is_file():

        resizer.resize_image(
            file_input,
            file_output,
            args.size,
            args.scale,
            args.overwrite,
        )
    elif file_input.is_dir():
        resizer.resize_images(
            file_input, file_output, args.size, args.scale, args.overwrite
        )
    else:
        raise FileNotFoundError(f"`{args.input}` not found.")


def crop_cmd(args):
    file_input, file_output = get_io_paths(args)
    if file_input.is_file():
        file_output = pathlib.Path(args.output)
        croper.crop_image(
            file_input,
            file_output,
            args.overwrite,
            ratio=args.ratio,
            size=args.size,
            align=args.align,
        )
    elif file_input.is_dir():
        croper.crop_images(
            file_input,
            file_output,
            args.overwrite,
            ratio=args.ratio,
            size=args.size,
            align=args.align,
        )
    else:
        raise FileNotFoundError(f"`{args.input}` not found.")


def prune_cmd(args):
    file_input = pathlib.Path(args.input)
    if file_input.is_file():
        prune.prune_image(file_input, args.resolution, args.dry_run)
    elif file_input.is_dir():
        prune.prune_images(file_input, args.resolution, args.dry_run)
    else:
        raise FileNotFoundError(f"`{args.input}` not found.")


def main():
    try:
        parser = cli_parser.get_parser()
        args = parser.parse_args()
        if args.command is None:
            parser.print_help()
            return

        # Convert command
        if args.command == "convert":
            convert_cmd(args)

        # Resize command
        elif args.command == "resize":
            resize_cmd(args)

        # Crop command
        elif args.command == "crop":
            crop_cmd(args)

        # Prune command
        elif args.command == "prune":
            prune_cmd(args)
        print("Done!")
    except FileNotFoundError as e:
        print("File not found:", e)
        exit(1)
    except FileExistsError as e:
        print(e)
        exit(1)
    except ValueError as e:
        print(e)
        exit(1)
    except Exception as e:
        print(f"Unhandled exception: {e}")
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
