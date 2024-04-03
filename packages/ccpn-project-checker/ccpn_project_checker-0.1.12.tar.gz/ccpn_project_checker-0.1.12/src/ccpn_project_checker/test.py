import sys, os
from pathlib import Path
import pytest

def run_tests():
    root_path = Path(os.path.realpath(__file__)).parent.resolve() / 'tests'
    retcode = pytest.main(['--rootdir', root_path, '-vvv'])
    sys.exit(retcode)

if __name__ == '__main__':
    run_tests()