import os
import sys

path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, path)

from simplestart.streamsync import *
from simplestart.common import *