"""The configuration of AVE."""

import os

debug = os.getenv("DEBUG")
ave_folder = os.path.dirname(os.path.realpath(__file__))

if os.path.isfile(os.path.join(ave_folder, "../VERSION")):
    # If running from folder
    root_folder = os.path.join(ave_folder, "..")
    games_folder = os.path.join(ave_folder, "games")
else:
    # If running from installation
    root_folder = ave_folder
    games_folder = os.path.join(root_folder, "_games")

screens_folder = os.path.join(ave_folder, "screens")


with open(os.path.join(root_folder, "VERSION")) as f:
    version = f.read().strip()

version_tuple = tuple(int(i) for i in version.split("."))
