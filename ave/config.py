import os

debug = os.getenv("DEBUG")
screen_folder = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "../screens")
