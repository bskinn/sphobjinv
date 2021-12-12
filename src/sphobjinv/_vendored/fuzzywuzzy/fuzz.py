#!/usr/bin/env python
# encoding: utf-8
"""
score.py

Copyright (c) 2011 Adam Cohen

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys
import os
import re
from difflib import SequenceMatcher
from sphobjinv._vendored.fuzzywuzzy import utils

REG_TOKEN = re.compile(r"[\w\d]+")  # B Skinn 2021-12-11

###########################
# Basic Scoring Functions #
###########################

def ratio(s1,  s2):

    if s1 is None: raise TypeError("s1 is None")
    if s2 is None: raise TypeError("s2 is None")

    m = SequenceMatcher(None, s1, s2)
    return int(100 * m.ratio())

# todo: skip duplicate indexes for a little more speed
def partial_ratio(s1,  s2):

    if s1 is None: raise TypeError("s1 is None")
    if s2 is None: raise TypeError("s2 is None")

    if len(s1) <= len(s2):
        shorter = s1; longer = s2;
    else:
        shorter = s2; longer = s1

    m = SequenceMatcher(None, shorter, longer)
    blocks = m.get_matching_blocks()

    # each block represents a sequence of matching characters in a string
    # of the form (idx_1, idx_2, len)
    # the best partial match will block align with at least one of those blocks
    #   e.g. shorter = "abcd", longer = XXXbcdeEEE
    #   block = (1,3,3)
    #   best score === ratio("abcd", "Xbcd")
    scores = []
    for block in blocks:
        long_start   = block[1] - block[0] if (block[1] - block[0]) > 0 else 0
        long_end     = long_start + len(shorter)
        long_substr  = longer[long_start:long_end]

        m2 = SequenceMatcher(None, shorter, long_substr)
        r = m2.ratio()
        if r > .995: return 100
        else: scores.append(r)

    return int(100 * max(scores))

##############################
# Advanced Scoring Functions #
##############################

# Sorted Token
#   find all alphanumeric tokens in the string
#   sort those tokens and take ratio of resulting joined strings
#   controls for unordered string elements
def _token_sort(s1,  s2, partial=True):

    if s1 is None: raise TypeError("s1 is None")
    if s2 is None: raise TypeError("s2 is None")

    # pull tokens
    tokens1 = REG_TOKEN.findall(s1)
    tokens2 = REG_TOKEN.findall(s2)

    # sort tokens and join
    sorted1 = u" ".join(sorted(tokens1))
    sorted2 = u" ".join(sorted(tokens2))

    sorted1 = sorted1.strip()
    sorted2 = sorted2.strip()

    if partial:
        return partial_ratio(sorted1, sorted2)
    else:
        return ratio(sorted1, sorted2)

def token_sort_ratio(s1,  s2):
    return _token_sort(s1, s2, False)

def partial_token_sort_ratio(s1,  s2):
    return _token_sort(s1, s2, True)

# Token Set
#   find all alphanumeric tokens in each string...treat them as a set
#   construct two strings of the form
#       <sorted_intersection><sorted_remainder>
#   take ratios of those two strings
#   controls for unordered partial matches
def _token_set(s1,  s2, partial=True):

    if s1 is None: raise TypeError("s1 is None")
    if s2 is None: raise TypeError("s2 is None")

    # pull tokens
    tokens1 = set(REG_TOKEN.findall(s1))
    tokens2 = set(REG_TOKEN.findall(s2))

    intersection = tokens1.intersection(tokens2)
    diff1to2 = tokens1.difference(tokens2)
    diff2to1 = tokens2.difference(tokens1)

    sorted_sect = u" ".join(sorted(intersection))
    sorted_1to2 = u" ".join(sorted(diff1to2))
    sorted_2to1 = u" ".join(sorted(diff2to1))

    combined_1to2 = sorted_sect + " " + sorted_1to2
    combined_2to1 = sorted_sect + " " + sorted_2to1

    # strip
    sorted_sect = sorted_sect.strip()
    combined_1to2 = combined_1to2.strip()
    combined_2to1 = combined_2to1.strip()

    pairwise = [
        ratio(sorted_sect, combined_1to2),
        ratio(sorted_sect, combined_2to1),
        ratio(combined_1to2, combined_2to1)
    ]
    return max(pairwise)

    # if partial:
    #     # partial_token_set_ratio
    #
    # else:
    #     # token_set_ratio
    #     tsr = ratio(combined_1to2, combined_2to1)
    #     return tsr

def token_set_ratio(s1,  s2):
    return _token_set(s1, s2, False)

def partial_token_set_ratio(s1,  s2):
    return _token_set(s1, s2, True)

# TODO: numerics

###################
# Combination API #
###################

# q is for quick
def QRatio(s1,  s2):
    if not utils.validate_string(s1): return 0
    if not utils.validate_string(s2): return 0

    p1 = utils.full_process(s1)
    p2 = utils.full_process(s2)

    return ratio(p1, p2)

# w is for weighted
def WRatio(s1,  s2):
    p1 = utils.full_process(s1)
    p2 = utils.full_process(s2)
    if not utils.validate_string(p1): return 0
    if not utils.validate_string(p2): return 0

    # should we look at partials?
    try_partial     = True
    unbase_scale    = .95
    partial_scale   = .90

    base = ratio(p1, p2)
    len_ratio = float(max(len(p1),len(p2)))/min(len(p1),len(p2))

    # if strings are similar length, don't use partials
    if len_ratio < 1.5: try_partial = False

    # if one string is much much shorter than the other
    if len_ratio > 8: partial_scale = .6

    if try_partial:
        partial      = partial_ratio(p1, p2)                 * partial_scale
        ptsor        = partial_token_sort_ratio(p1, p2)      * unbase_scale * partial_scale
        ptser        = partial_token_set_ratio(p1, p2)       * unbase_scale * partial_scale

        return int(max(base, partial, ptsor, ptser))
    else:
        tsor         = token_sort_ratio(p1, p2)              * unbase_scale
        tser         = token_set_ratio(p1, p2)               * unbase_scale

        return int(max(base, tsor, tser))

