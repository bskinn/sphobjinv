# ------------------------------------------------------------------------------
# Name:        tests
# Purpose:     Master script for sphobjinv testing suite
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     29 Oct 2017
# Copyright:   (c) Brian Skinn 2016-2017
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
    GOOD = 'good'
    FAIL = 'fail'

    CLI = 'cli'
    CLI_GOOD = 'cli_good'
    CLI_FAIL = 'cli_fail'

    API = 'api'
    API_GOOD = 'api_good'
    API_FAIL = 'api_fail'

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
    gp_cli = prs.add_argument_group(title="CLI Tests")
    gp_api = prs.add_argument_group(title="API Tests")

    # Options without subgroups
    prs.add_argument(AP.PFX.format(AP.ALL), '-a',
                     action='store_true',
                     help="Run all tests (overrides any other selections)")
    prs.add_argument(AP.PFX.format(AP.GOOD), '-g',
                     action='store_true',
                     help="Run all expect-good tests")
    prs.add_argument(AP.PFX.format(AP.FAIL), '-f',
                     action='store_true',
                     help="Run all expect-fail tests")

    # CLI group
    gp_cli.add_argument(AP.PFX.format(AP.CLI),
                        action='store_true',
                        help="Run all CLI tests")
    gp_cli.add_argument(AP.PFX.format(AP.CLI_GOOD),
                        action='store_true',
                        help="Run expect-good CLI tests")
    gp_cli.add_argument(AP.PFX.format(AP.CLI_FAIL),
                        action='store_true',
                        help="Run expect-fail CLI tests")

    # API group
    gp_api.add_argument(AP.PFX.format(AP.API),
                        action='store_true',
                        help="Run all API tests")
    gp_api.add_argument(AP.PFX.format(AP.API_GOOD),
                        action='store_true',
                        help="Run expect-good API tests")
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

    # Commandline tests per-group
    # Expect-good tests
    addsuiteif(sphobjinv.test.sphobjinv_cli.suite_cli_expect_good(),
               [AP.ALL, AP.GOOD, AP.CLI, AP.CLI_GOOD])
    addsuiteif(sphobjinv.test.sphobjinv_api.suite_api_expect_good(),
               [AP.ALL, AP.GOOD, AP.API, AP.API_GOOD])

    # Expect-fail tests
    addsuiteif(sphobjinv.test.sphobjinv_cli.suite_cli_expect_fail(),
               [AP.ALL, AP.FAIL, AP.CLI, AP.CLI_FAIL])
    addsuiteif(sphobjinv.test.sphobjinv_api.suite_api_expect_fail(),
               [AP.ALL, AP.FAIL, AP.API, AP.API_FAIL])

    # Create the test runner and execute
    ttr = ut.TextTestRunner(buffer=True,
                            verbosity=(2 if params['v'] else 1),
                            warnings=('always' if params['w'] else None))
    success = ttr.run(ts).wasSuccessful()

    # Return based on success result (enables tox)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
