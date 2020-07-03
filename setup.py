import os
import sys
import setuptools
from ave.__main__ import make_json

if sys.version_info < (3, 5):
    print("Python 3.5 or higher required, please upgrade.")
    sys.exit(1)

with open("VERSION") as f:
    VERSION = f.read()

make_json()

requirements = []
if os.name == 'nt':
    requirements.append("windows-curses")

entry_points = {'console_scripts': ['ave = ave.__main__:run',
                                    'ave-make-json = ave.__main__:make_json']}

data_files = [
    ("_avegames", [os.path.join("games", i) for i in os.listdir("games")
                   if i.endswith(".ave")]),
    ("_avescreens", ["screens/credits", "screens/title", "screens/user"]),
    ("", ["VERSION", "gamelist.json"])]

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
        packages=["ave"],
        data_files=data_files,
        include_package_data=True,
        entry_points=entry_points,
        install_requires=requirements,)
