"""Tests for init procedure"""
from pathlib import Path
from Gene_Family_Analysis.GFA_package.GFA.GFA import family


LOG_DIR = 'D:\plab2ws22-maruh0\group4\Gene_Family_Analysis\GFA_package\GFA\progress.log'
class TestInit:
    def test_log_file(self):
        """Checks if the log file is made"""
        assert Path(LOG_DIR).is_file()