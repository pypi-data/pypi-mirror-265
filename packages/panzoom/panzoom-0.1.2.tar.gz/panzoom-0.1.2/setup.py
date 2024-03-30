from setuptools import setup, find_packages

setup(
    name="panzoom",
    version="0.1.2",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'panzoom=panzoom.cli:main',
        ],
    },
    install_requires=[
        'numpy',
        'opencv-python',
        'Pillow',
        'requests',
    ],
    author="Nazim Zeeshan",
    author_email="nazim.zeeshan@gmail.com",
    description="A CLI tool for creating pan and zoom videos from images.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nzee/panzoom",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
