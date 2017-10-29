# ------------------------------------------------------------------------------
# Name:        __init__
# Purpose:     Package submodule definition for the test suite
#
# Author:      Brian Skinn
#                bskinn@alum.mit.edu
#
# Created:     29 Oct 2017
# Copyright:   (c) Brian Skinn 2017
# License:     The MIT License; see "LICENSE.txt" for full license terms.
#
#              https://www.github.com/bskinn/sphobjinv
#
# ------------------------------------------------------------------------------

"""Base submodule for the sphobjinv test suite."""

from __future__ import absolute_import

__all__ = ['suite_expect_good', 'suite_expect_fail']

from .sphobjinv_base import suite_expect_good, suite_expect_fail
