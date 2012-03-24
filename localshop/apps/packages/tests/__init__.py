import os


def load_tests(loader, standard_tests, pattern):
    """This function is automatically called by unittest2 to discover tests
    within this module.

    """
    package_tests = loader.discover(
        start_dir=os.path.dirname(__file__),
        pattern='test*.py',
        top_level_dir=os.path.join(os.path.dirname(__file__), '..', '..'))
    standard_tests.addTests(package_tests)
    return standard_tests

# Make sure that nose doesn't collect load_test as a testcase
load_tests.__test__ = False

