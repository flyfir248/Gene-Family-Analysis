"""GFA module tests."""

import pytest
from Gene_Family_Analysis.GFA_package.GFA.cli import tree
from pathlib import Path
import os

IMAGE_PATH = str(os.path.join(Path.home(), "Downloads"))
class TestFamily:
    """Unit tests for the family class."""
    def test_image(self):
        """Checks if the result is downloaded or not"""
        if IMAGE_PATH.is_file():
            IMAGE_PATH.unlink()
        assert not IMAGE_PATH.is_file()

