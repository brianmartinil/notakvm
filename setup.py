from notakvm import __version__
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

this_dir = abspath(dirname(__file__))
with open(join(this_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="notaKVM",
    version=__version__,
    python_requires=">=3.6",
    description="Fake a KVM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brianmartinil/notakvm",
    project_urls={
        "Source": "https://github.com/brianmartinil/notakvm",
    },
    author="Brian Martin",
    # TODO: classifiers
    keywords="cli",
    package_data={
        'notakvm': ['ControlMyMonitor.exe', 'ControlMyMonitor.chm', 'readme.txt'],
    },
    packages=find_packages(exclude=["docs"]),
    install_requires=[
        "wmi",
        "psutil",
    ],
    entry_points={
        "console_scripts": [
            "notakvm=notakvm.__main__:main",
        ],
    },
)