"""
Music Checker is a class aimed at scanning a series of media files
extracting tag information from them for later reporting
"""

from ._generic_tag_map import TagMap
from .music_validator import MusicValidator

VERSION = (0, 1, 14)
"""Version tuple."""

VERSION_STRING = ".".join(map(str, VERSION))
"""Version string."""

TagMap

MusicValidator
