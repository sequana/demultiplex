import easydev
import os
import tempfile
import subprocess
import sys

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
    import sequana_pipelines.demultiplex.main as m
    sys.argv = ["test", "--bcl-directory", bcldir, "--merging-strategy", "merge",
          "--working-directory", str(directory), "--force", "--sample-sheet", samplesheet]
    m.main()


def test_standalone_baddies(tmp_path):
    directory = tmp_path / "test"
    directory.mkdir()

    with tempfile.TemporaryDirectory() as directory:
        cmd = """sequana_demultiplex --bcl-directory {} """
        cmd += """--run-mode local --working-directory {} --force --sample-sheet {} --merging-strategy none"""
        cmd = cmd.format(bcldir, directory, "wrong")
        subprocess.call(cmd.split())

