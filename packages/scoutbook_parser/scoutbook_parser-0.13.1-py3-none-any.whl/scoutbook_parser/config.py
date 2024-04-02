from pathlib import Path
import os
import toml

basedir = Path(os.path.dirname(__file__))

CONFIG = toml.load(basedir / "config.toml")
