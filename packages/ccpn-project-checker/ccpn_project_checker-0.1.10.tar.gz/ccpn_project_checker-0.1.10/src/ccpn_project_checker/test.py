import sys
from pathlib import Path

import pytest
from ccpn_project_checker.util import different_cwd
def run_tests():
    test_path = (Path('__file__').parent.resolve() / 'tests')
    retcode = pytest.main(['-x', test_path,'-vvv'])
    sys.exit(retcode)

if __name__ == '__main__':
    run_tests()