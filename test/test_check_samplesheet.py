import sys, os
from sequana.iem import IEM
import easydev
from . import test_dir


sharedir = f"{test_dir}/data/"


def test_noerror():
    IEM(sharedir + "SampleSheet.csv").validate()


def test_error1():
    try:
        IEM(sharedir + "SampleSheet-error1.csv").validate()
        assert False
    except:
        assert True


def test_error2():
    try:
        IEM(sharedir + "SampleSheet-error2.csv").validate()
        assert False
    except:
        assert True


def test_error2():
    try:
        IEM(sharedir + "SampleSheet-error3.csv").validate()
        assert False
    except:
        assert True
