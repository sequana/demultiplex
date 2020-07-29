import sys, os
from sequana_pipelines.demultiplex import check_samplesheet
import easydev

sequana_path = easydev.get_package_location('sequana_demultiplex')
sharedir = os.sep.join([sequana_path , "sequana_pipelines", 'demultiplex', 'data'])



def test_noerror():
    sys.argv = ["test", "-s", sharedir + "/SampleSheet.csv"];
    check_samplesheet.main()


def test_error1():
    sys.argv = ["test", "-s", sharedir + "/SampleSheet-error1.csv"];
    try:
        check_samplesheet.main()
        assert False
    except:
        assert True


def test_error2():
    sys.argv = ["test", "-s", sharedir + "/SampleSheet-error2.csv"];
    try:
        check_samplesheet.main()
        assert False
    except:
        assert True


def test_error2():
    sys.argv = ["test", "-s", sharedir + "/SampleSheet-error3.csv"];
    try:
        check_samplesheet.main()
        assert False
    except:
        assert True
