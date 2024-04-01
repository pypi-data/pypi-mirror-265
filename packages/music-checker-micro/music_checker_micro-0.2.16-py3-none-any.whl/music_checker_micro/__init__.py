"""
MusicChecker is a class aimed at scanning a series of media files, 
extracting tag information from them for later reporting
"""

from .music_checker import MusicChecker

VERSION = (0, 2, 16)
"""Version tuple."""

VERSION_STRING = ".".join(map(str, VERSION))
"""Version string."""

MusicChecker
