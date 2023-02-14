"""Tests for GFA package"""

from pathlib import Path
from click.testing import CliRunner
from Gene_Family_Analysis.GFA_package.GFA.cli import tree

class TestCli:
    """Class for testing the CLI command"""
    runner = runner = CliRunner()
    result = runner.invoke(tree, [str()])

    help_result = runner.invoke(tree, ['--help'])