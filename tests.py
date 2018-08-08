# ------------------------------------------------------------------------------
# Name:        tests
# Purpose:     Master script for sphobjinv testing suite
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     29 Oct 2017
# Copyright:   (c) Brian Skinn 2016-2018
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#           http://www.github.com/bskinn/sphobjinv
#
# ------------------------------------------------------------------------------


class AP(object):
    """ Container for arguments for selecting test suites.

    Also includes PFX, a helper string for substitution/formatting.

    """
    ALL = 'all'
    LOCAL = 'local'
    GOOD = 'good'
    GOOD_LOCAL = 'good_local'
    FAIL = 'fail'
    FAIL_LOCAL = 'fail_local'

    TESTALL = 'testall'

    CLI = 'cli'
    CLI_LOCAL = 'cli_local'
    CLI_GOOD = 'cli_good'
    CLI_GOOD_LOCAL = 'cli_good_local'
    CLI_FAIL = 'cli_fail'
    CLI_FAIL_LOCAL = 'cli_fail_local'

    API = 'api'
    API_LOCAL = 'api_local'
    API_GOOD = 'api_good'
    API_GOOD_LOCAL = 'api_good_local'
    API_FAIL = 'api_fail'

    README = 'readme'

    PFX = "--{0}"


def get_parser():
    import argparse

    # Create the parser
    prs = argparse.ArgumentParser(description="Run tests for sphobjinv")

    # Verbosity argument
    prs.add_argument('-v', action='store_true',
                     help="Show verbose output")

    # Warnings argument
    prs.add_argument('-w', action='store_true',
                     help="Display warnings emitted during tests")

    # Test subgroups
    gp_testall = prs.add_argument_group(title="Test All Inventories")
    gp_cli = prs.add_argument_group(title="CLI Tests")
    gp_api = prs.add_argument_group(title="API Tests")

    # Options without subgroups
    prs.add_argument(AP.PFX.format(AP.ALL), '-a',
                     action='store_true',
                     help="Run all tests (overrides any other selections)")
    prs.add_argument(AP.PFX.format(AP.LOCAL), '-l',
                     action='store_true',
                     help="Run all local tests (not requiring Internet "
                          "access)")
    prs.add_argument(AP.PFX.format(AP.GOOD), '-g',
                     action='store_true',
                     help="Run all expect-good tests")
    prs.add_argument(AP.PFX.format(AP.GOOD_LOCAL),
                     action='store_true',
                     help="Run all local expect-good tests")
    prs.add_argument(AP.PFX.format(AP.FAIL), '-f',
                     action='store_true',
                     help="Run all expect-fail tests")
    prs.add_argument(AP.PFX.format(AP.FAIL_LOCAL),
                     action='store_true',
                     help="Run all local expect-fail tests")
    prs.add_argument(AP.PFX.format(AP.README),
                     action='store_true',
                     help="Run README doctest")

    # TestAll group
    gp_testall.add_argument(AP.PFX.format(AP.TESTALL),
                            action='store_true',
                            help="Test all .inv files in selected tests")

    # CLI group
    gp_cli.add_argument(AP.PFX.format(AP.CLI),
                        action='store_true',
                        help="Run all CLI tests")
    gp_cli.add_argument(AP.PFX.format(AP.CLI_LOCAL),
                        action='store_true',
                        help="Run all local CLI tests")
    gp_cli.add_argument(AP.PFX.format(AP.CLI_GOOD),
                        action='store_true',
                        help="Run expect-good CLI tests")
    gp_cli.add_argument(AP.PFX.format(AP.CLI_GOOD_LOCAL),
                        action='store_true',
                        help="Run local expect-good CLI tests")
    gp_cli.add_argument(AP.PFX.format(AP.CLI_FAIL),
                        action='store_true',
                        help="Run expect-fail CLI tests")
    gp_cli.add_argument(AP.PFX.format(AP.CLI_FAIL_LOCAL),
                        action='store_true',
                        help="Run local expect-fail CLI tests")

    # API group
    gp_api.add_argument(AP.PFX.format(AP.API),
                        action='store_true',
                        help="Run all API tests")
    gp_api.add_argument(AP.PFX.format(AP.API_LOCAL),
                        action='store_true',
                        help="Run all local API tests")
    gp_api.add_argument(AP.PFX.format(AP.API_GOOD),
                        action='store_true',
                        help="Run expect-good API tests")
    gp_api.add_argument(AP.PFX.format(AP.API_GOOD_LOCAL),
                        action='store_true',
                        help="Run local expect-good API tests")
    gp_api.add_argument(AP.PFX.format(AP.API_FAIL),
                        action='store_true',
                        help="Run expect-fail API tests")

    # Return the parser
    return prs


def main():
    import os
    import os.path as osp
    import sys
    import unittest as ut

    import sphobjinv.test
    from sphobjinv.test.sphobjinv_base import TESTALL

    # Retrieve the parser
    prs = get_parser()

    # Pull the dict of stored flags, saving the un-consumed args, and
    # update sys.argv
    ns, args_left = prs.parse_known_args()
    params = vars(ns)
    sys.argv = sys.argv[:1] + args_left

    # Create the empty test suite
    ts = ut.TestSuite()

    # Helper function for adding test suites. Just uses ts and params from
    # the main() function scope
    def addsuiteif(suite, flags):
        if any(params[k] for k in flags):
            ts.addTest(suite)

    # Add commandline-indicated tests per-group
    # Expect-good tests
    addsuiteif(sphobjinv.test.sphobjinv_api.suite_api_expect_good(),
               [AP.ALL, AP.LOCAL, AP.GOOD, AP.GOOD_LOCAL,
                AP.API, AP.API_LOCAL, AP.API_GOOD, AP.API_GOOD_LOCAL])
    addsuiteif(sphobjinv.test.sphobjinv_api.suite_api_expect_good_nonlocal(),
               [AP.ALL, AP.GOOD, AP.API, AP.API_GOOD])
    addsuiteif(sphobjinv.test.sphobjinv_cli.suite_cli_expect_good(),
               [AP.ALL, AP.LOCAL, AP.GOOD, AP.GOOD_LOCAL,
                AP.CLI, AP.CLI_LOCAL, AP.CLI_GOOD, AP.CLI_GOOD_LOCAL])
    addsuiteif(sphobjinv.test.sphobjinv_cli.suite_cli_expect_good_nonlocal(),
               [AP.ALL, AP.GOOD, AP.CLI, AP.CLI_GOOD])

    # Expect-fail tests
    addsuiteif(sphobjinv.test.sphobjinv_api.suite_api_expect_fail(),
               [AP.ALL, AP.LOCAL, AP.FAIL, AP.API, AP.API_LOCAL, AP.API_FAIL])
    addsuiteif(sphobjinv.test.sphobjinv_cli.suite_cli_expect_fail(),
               [AP.ALL, AP.LOCAL, AP.FAIL, AP.FAIL_LOCAL,
                AP.CLI, AP.CLI_LOCAL, AP.CLI_FAIL, AP.CLI_FAIL_LOCAL])
    addsuiteif(sphobjinv.test.sphobjinv_cli.suite_cli_expect_fail_nonlocal(),
               [AP.ALL, AP.FAIL, AP.CLI, AP.CLI_FAIL])

    # README doctest
    addsuiteif(sphobjinv.test.sphobjinv_readme.suite_doctest_readme(),
               [AP.ALL, AP.README])

    # Enable testing all invs if indicated
    os.environ.update({TESTALL: '1' if params[AP.TESTALL] else ''})

    # Create the test runner and execute
    ttr = ut.TextTestRunner(buffer=True,
                            verbosity=(2 if params['v'] else 1),
                            warnings=('always' if params['w'] else None))
    success = ttr.run(ts).wasSuccessful()

    # Return based on success result (lets tox report success/fail)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
