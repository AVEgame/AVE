"""The configuration of AVE."""

import os

debug = os.getenv("DEBUG")
ave_folder = os.path.dirname(os.path.realpath(__file__))
folder_prefix = ""
if not os.path.isdir(os.path.join(ave_folder, "../games")):
    folder_prefix = "_ave"

screens_folder = os.path.join(ave_folder, "../" + folder_prefix + "screens")
games_folder = os.path.join(ave_folder, "../" + folder_prefix + "games")

with open(os.path.join(ave_folder, "../VERSION")) as f:
    version = f.read()
