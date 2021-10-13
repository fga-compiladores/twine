import sys
import os

sys.path.append(os.getcwd())

from twine.cli import twine

twine()