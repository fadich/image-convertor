# Image convertor

Convert image(-s). See command manual for more details:
```shell
$ python convert.py --help

usage: convert.py [-h] [-p PATH] [-e EXT] [-r] [-y] [--override] [--clean-up] TARGET_TYPE

Convert image(s) type

positional arguments:
  TARGET_TYPE           target type

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  path to image or directory with images
  -e EXT, --ext EXT     source files extension; do nothing for a single file
  -r, --recursive       read directory recursively; do nothing for a single file
  -y, --confirm         skip confirmation
  --override            replace target file(s)
  --clean-up            remove converting file(s)
```

Example:
```shell
python image_convertor\cmd\convert.py png --path C:\home\Ванила\Screenshots --ext tga --recursive --override --clean-up --confirm
```
