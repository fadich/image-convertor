#!/usr/bin/env python3

import os
import sys
import argparse

from PIL import Image


def write(line: str = "", std=None):
    if std is None:
        std = sys.stdout

    std.write(f"{line}")
    std.flush()


def writeln(line: str = "", std=None):
    if std is None:
        std = sys.stdout

    std.write(f"{line}\n")
    std.flush()


def main():
    parser = argparse.ArgumentParser(description="Convert image(s) type")
    parser.add_argument("TARGET_TYPE", type=str, help="target type")
    parser.add_argument("-p", "--path", dest="path", type=str, help="path to image or directory with images")
    parser.add_argument(
        "-e", "--ext", dest="ext", type=str, help="source files extension; do nothing for a single file"
    )
    parser.add_argument(
        "-r", "--recursive", dest="recursive", action="store_true",
        help="read directory recursively; do nothing for a single file"
    )
    parser.add_argument("-y", "--confirm", dest="confirm", action="store_true", help="skip confirmation")
    parser.add_argument("--override", dest="override", action="store_true", help="replace target file(s)")
    parser.add_argument("--clean-up", dest="clean_up", action="store_true", help="remove converting file(s)")

    args = parser.parse_args()

    target_type = args.TARGET_TYPE.lower()
    if not target_type.startswith("."):
        target_type = f".{target_type}"

    source_files = []
    if os.path.isdir(args.path):
        if args.ext is None:
            writeln(f"Please, specify a file extension to be converted", sys.stderr)

            return -1

        source_type = args.ext.lower()
        if not source_type.startswith("."):
            source_type = f".{source_type}"

        walked = os.walk(args.path)
        for dir_content in walked:
            converting = filter(lambda x: os.path.splitext(x)[1] == source_type, dir_content[2])
            source_files.extend(map(lambda x: os.path.join(dir_content[0], x), converting))
            if not args.recursive:
                break

        if len(source_files) == 0:
            writeln(f"No *{source_type} files found in <{args.path}>", sys.stderr)

            return -1

    elif os.path.isfile(args.path):
        source_files = [args.path, ]
    else:
        writeln(f"<{args.path}> not found", sys.stderr)

        return -1

    total_files = len(source_files)

    if args.confirm:
        writeln(f"Going to convert {total_files} file(s)...")
    else:
        writeln(f"Are you going to convert {total_files} file(s)?")
        writeln("Press [ENTER] to continue")
        sys.stdin.read(1)

    files = [(f, f"{os.path.splitext(f)[0]}{target_type}") for f in source_files]

    if not args.override:
        for _, target_file in files:
            if os.path.exists(target_file):
                writeln(f"File <{target_file}> already exists", sys.stderr)

                return -1

    errors = 0
    converted = 0
    for source_file, target_file in files:
        percent = (errors + converted) / total_files * 100
        write(f"{percent:.2f}% done...\r")

        try:
            Image.open(source_file).save(target_file)
            converted += 1

            if args.clean_up:
                os.remove(source_file)
        except Exception as e:
            errors += 1
            writeln(f"Error converting <{source_file}>: {str(e)}", sys.stderr)

    write("100.00% done...\n\r")

    writeln(f"{converted} files has been converted; {errors} errors")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
