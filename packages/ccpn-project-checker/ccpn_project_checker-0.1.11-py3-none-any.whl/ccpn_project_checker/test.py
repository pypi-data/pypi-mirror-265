import sys
from pathlib import Path

import pytest
def run_tests():
    # root_path = Path('__file__').parent.resolve()
    test_path = (Path('__file__').parent.resolve() / 'tests')
    retcode = pytest.main(['--rootdir', test_path,'-vvv'])
    sys.exit(retcode)

if __name__ == '__main__':
    run_tests()