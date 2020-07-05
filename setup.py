import os
import sys
import setuptools
from ave.__main__ import make_json

if sys.version_info < (3, 4):
    print("Python 3.4 or higher required, please upgrade.")
    sys.exit(1)

with open("VERSION") as f:
    VERSION = f.read()


make_json()

os.system("cp VERSION ave/")
os.system("cp -r games ave/_games")

entry_points = {'console_scripts': ['ave = ave.__main__:run',
                                    'ave-make-json = ave.__main__:make_json']}

data_files = [
    ("ave/_games", [os.path.join("ave/_games", i) for i in os.listdir("ave/_games")
                       if i.endswith(".ave")]),
    ("ave/screens", ["ave/screens/credits", "ave/screens/title", "ave/screens/user"]),
    ("ave", ["VERSION", "gamelist.json"])]


if __name__ == "__main__":
    setuptools.setup(
        name="avegame",
        description="Adventure! Villainy! Excitement!",
        version=VERSION,
        author="Matthew Scroggs and Giancarlo Grasso",
        license="MIT",
        author_email="ave@mscroggs.co.uk",
        maintainer_email="ave@mscroggs.co.uk",
        url="https://github.com/AVEgame/AVE",
        packages=["ave", "ave.components", "ave.parsing", "ave.display",
                  "ave.test", "ave.screens"],
        data_files=data_files,
        include_package_data=True,
        entry_points=entry_points,
        install_requires=['windows-curses>=2.1.0 ; platform_system=="Windows"']
    )
