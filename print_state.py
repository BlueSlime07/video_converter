#!/usr/bin/env python3
from pathlib import Path
import sys
import subprocess
import shutil
import hashlib
import pickle as pk

path = Path(sys.argv[1]).resolve()/".video_converter/state"
if not path.exists():exit(1)
file = path.open("rb")
print(pk.load(file))
