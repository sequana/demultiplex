import easydev
import os
import tempfile
import subprocess
import sys
from sequana_pipelines.demultiplex.main import  main
from click.testing import CliRunner


from . import test_dir

samplesheet = f"{test_dir}/data/SampleSheet.csv"
bcldir = f"{test_dir}/data/bcl"

def test_help():
    cmd = """sequana_demultiplex --help"""
    subprocess.call(cmd.split())


def test_standalone_subprocess(tmp_path):
    directory = tmp_path / "test"
    directory.mkdir()

    with tempfile.TemporaryDirectory() as directory:
        cmd = """sequana_demultiplex --bcl-directory {} """
        cmd += """--run-mode local --working-directory {} --force --sample-sheet {} --merging-strategy none"""
        cmd = cmd.format(bcldir, directory, samplesheet)
        subprocess.call(cmd.split())


def test_standalone_script(tmp_path):
    directory = tmp_path / "test"
    directory.mkdir()

    runner = CliRunner()
    results = runner.invoke(main, ["--bcl-directory", bcldir, "--merging-strategy", "merge", "--working-directory", str(directory), "--force", "--sample-sheet", samplesheet])
    assert results.exit_code == 0


def test_standalone_baddies(tmp_path):
    directory = tmp_path / "test"
    directory.mkdir()

    with tempfile.TemporaryDirectory() as directory:
        cmd = """sequana_demultiplex --bcl-directory {} """
        cmd += """--run-mode local --working-directory {} --force --sample-sheet {} --merging-strategy none"""
        cmd = cmd.format(bcldir, directory, "wrong")
        subprocess.call(cmd.split())


