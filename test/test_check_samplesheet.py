import sys, os
from sequana.iem import IEM
import easydev

sequana_path = easydev.get_package_location('sequana_demultiplex')
sharedir = os.sep.join([sequana_path , "sequana_pipelines", 'demultiplex', 'data'])



def test_noerror():
    IEM(sharedir + "/SampleSheet.csv").validate()


def test_error1():
    try:
        IEM(sharedir + "/SampleSheet-error1.csv").validate()
        assert False
    except:
        assert True


def test_error2():
    try:
        IEM(sharedir + "/SampleSheet-error2.csv").validate()
        assert False
    except:
        assert True


def test_error2():
    try:
        IEM(sharedir + "/SampleSheet-error3.csv").validate()
        assert False
    except:
        assert True
