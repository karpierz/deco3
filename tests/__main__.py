# Copyright (c) 2025 Adam Karpierz
# SPDX-License-Identifier: MIT

import unittest
import sys
import logging

from . import test_dir

log = logging.getLogger(__name__)


def test_suite(names=None, omit=()):
    from . import __name__ as pkg_name
    from . import __path__ as pkg_path
    import unittest
    import pkgutil
    if names is None:
        names = [name for _, name, _ in pkgutil.iter_modules(pkg_path)
                 if name.startswith("test_") and name not in omit]
    names = [".".join((pkg_name, name)) for name in names]
    tests = unittest.defaultTestLoader.loadTestsFromNames(names)
    return tests


def main(argv=sys.argv[1:]):
    import runpy
    print("Running tests\n", file=sys.stderr)
    tests = test_suite(argv or None)
    # result = unittest.TextTestRunner(verbosity=2).run(tests)
    # return 0 if result.wasSuccessful() else 1
    result1 = runpy.run_path(str(test_dir/"test_ast.py"),  run_name="__main__")
    result2 = runpy.run_path(str(test_dir/"test_conc.py"), run_name="__main__")
    result3 = runpy.run_path(str(test_dir/"tman_conc.py"), run_name="__main__")
    return 0 if result1 and result2 and result3 else 1


if __name__.rpartition(".")[-1] == "__main__":
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
