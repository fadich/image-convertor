from setuptools import setup, find_packages


setup(
    name='image_convertor',
    description='Convert image types',
    version='0.1.0',
    packages=find_packages(),
    install_requires=(
        'Pillow==9.1.0',
    ),
    entry_points={
        'console_scripts': [
            'image-convertor = image-convertor.cmd.convert:main',
        ],
    }
)
