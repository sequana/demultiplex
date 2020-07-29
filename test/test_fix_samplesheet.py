import sys, os
from sequana_pipelines.demultiplex import fix_samplesheet
import easydev

sequana_path = easydev.get_package_location('sequana_demultiplex')
sharedir = os.sep.join([sequana_path , "sequana_pipelines", 'demultiplex', 'data'])




def test_error1():
    with easydev.TempFile() as fout:
        sys.argv = ["test", "-s",  sharedir + "/SampleSheet-error1.csv",
            "--fix-semicolons", "-o", fout.name]
        try:
            fix_samplesheet.main()
            assert False
        except:
            assert True

def test_error2():
    with easydev.TempFile() as fout:
        sys.argv = ["test", "-s",  sharedir + "/SampleSheet-error2.csv",
            "--fix-semicolons", "-o", fout.name]
        try:
            fix_samplesheet.main()
            assert False
        except:
            assert True

def test_error3():
    with easydev.TempFile() as fout:
        sys.argv = ["test", "-s",  sharedir + "/SampleSheet-error3.csv",
            "--fix-semicolons", "-o", fout.name]
        try:
            fix_samplesheet.main()
            assert False
        except:
            assert True

def test_in_out_same():
    with easydev.TempFile() as fout:
        sys.argv = ["test", "-s",  sharedir + "/SampleSheet-error3.csv",
            "--fix-semicolons", "-o", sharedir + "/SampleSheet-error3.csv"]
        try:
            fix_samplesheet.main()
            assert False
        except:
            assert True
