# -*- coding: utf8 -*-

from sphobjinv._vendored.fuzzywuzzy.fuzz import *
from sphobjinv._vendored.fuzzywuzzy import process
from sphobjinv._vendored.fuzzywuzzy import utils

import itertools
import unittest

class UtilsTest(unittest.TestCase):
    def setUp(self):
        self.s1 = "new york mets"
        self.s1a = "new york mets"
        self.s2 = "new YORK mets"
        self.s3 = "the wonderful new york mets"
        self.s4 = "new york mets vs atlanta braves"
        self.s5 = "atlanta braves vs new york mets"
        self.s6 = "new york mets - atlanta braves"
        self.mixed_strings = [
            "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
            "C'est la vie",
            "Ça va?",
            "Cães danados",
            u"\xacCamarões assados",
            u"a\xac\u1234\u20ac\U00008000",
            u"\u00C1"
        ]


    def tearDown(self):
        pass

    def test_asciidammit(self):
        for s in self.mixed_strings:
            utils.asciidammit(s)

    def test_asciionly(self):
        for s in self.mixed_strings:
            # ascii only only runs on strings
            s = utils.asciidammit(s)
            utils.asciionly(s)

    def test_fullProcess(self):
        for s in self.mixed_strings:
            utils.full_process(s)

class RatioTest(unittest.TestCase):

    def setUp(self):
        self.s1 = "new york mets"
        self.s1a = "new york mets"
        self.s2 = "new YORK mets"
        self.s3 = "the wonderful new york mets"
        self.s4 = "new york mets vs atlanta braves"
        self.s5 = "atlanta braves vs new york mets"
        self.s6 = "new york mets - atlanta braves"

        self.cirque_strings = [
            "cirque du soleil - zarkana - las vegas",
            "cirque du soleil ",
            "cirque du soleil las vegas",
            "zarkana las vegas",
            "las vegas cirque du soleil at the bellagio",
            "zarakana - cirque du soleil - bellagio"
        ]

        self.baseball_strings = [
            "new york mets vs chicago cubs",
            "chicago cubs vs chicago white sox",
            "philladelphia phillies vs atlanta braves",
            "braves vs mets",
        ]

    def tearDown(self):
        pass

    def testEqual(self):
        self.assertEqual(ratio(self.s1, self.s1a),100)

    def testCaseInsensitive(self):
        self.assertNotEqual(ratio(self.s1, self.s2),100)
        self.assertEqual(ratio(utils.full_process(self.s1), utils.full_process(self.s2)),100)

    def testPartialRatio(self):
        self.assertEqual(partial_ratio(self.s1, self.s3),100)

    def testTokenSortRatio(self):
        self.assertEqual(token_sort_ratio(self.s1, self.s1a),100)

    def testPartialTokenSortRatio(self):
        self.assertEqual(partial_token_sort_ratio(self.s1, self.s1a),100)
        self.assertEqual(partial_token_sort_ratio(self.s4, self.s5),100)

    def testTokenSetRatio(self):
        self.assertEqual(token_set_ratio(self.s4, self.s5),100)

    def testPartialTokenSetRatio(self):
        self.assertEqual(partial_token_set_ratio(self.s4, self.s5),100)

    def testQuickRatioEqual(self):
        self.assertEqual(QRatio(self.s1, self.s1a), 100)

    def testQuickRatioCaseInsensitive(self):
        self.assertEqual(QRatio(self.s1, self.s2), 100)

    def testQuickRatioNotEqual(self):
        self.assertNotEqual(QRatio(self.s1, self.s3), 100)

    def testWRatioEqual(self):
        self.assertEqual(WRatio(self.s1, self.s1a), 100)

    def testWRatioCaseInsensitive(self):
        self.assertEqual(WRatio(self.s1, self.s2), 100)

    def testWRatioPartialMatch(self):
        # a partial match is scaled by .9
        self.assertEqual(WRatio(self.s1, self.s3), 90)

    def testWRatioMisorderedMatch(self):
        # misordered full matches are scaled by .95
        self.assertEqual(WRatio(self.s4, self.s5), 95)

    def testWRatioUnicode(self):
        self.assertEqual(WRatio(unicode(self.s1), unicode(self.s1a)), 100)

    def testQRatioUnicode(self):
        self.assertEqual(WRatio(unicode(self.s1), unicode(self.s1a)), 100)

    def testIssueSeven(self):
        s1 = "HSINCHUANG"
        s2 = "SINJHUAN"
        s3 = "LSINJHUANG DISTRIC"
        s4 = "SINJHUANG DISTRICT"

        self.assertGreater(partial_ratio(s1, s2), 75)
        self.assertGreater(partial_ratio(s1, s3), 75)
        self.assertGreater(partial_ratio(s1, s4), 75)

    def testWRatioUnicodeString(self):
        s1 = u"\u00C1"
        s2 = "ABCD"
        score = WRatio(s1, s2)
        self.assertEqual(0, score)

    def testQRatioUnicodeString(self):
        s1 = u"\u00C1"
        s2 = "ABCD"
        score = QRatio(s1, s2)
        self.assertEqual(0, score)

    # test processing methods
    def testGetBestChoice1(self):
        query = "new york mets at atlanta braves"
        best = process.extractOne(query, self.baseball_strings)
        self.assertEqual(best[0], "braves vs mets")

    def testGetBestChoice2(self):
        query = "philadelphia phillies at atlanta braves"
        best = process.extractOne(query, self.baseball_strings)
        self.assertEqual(best[0], self.baseball_strings[2])

    def testGetBestChoice3(self):
        query = "atlanta braves at philadelphia phillies"
        best = process.extractOne(query, self.baseball_strings)
        self.assertEqual(best[0], self.baseball_strings[2])

    def testGetBestChoice4(self):
        query = "chicago cubs vs new york mets"
        best = process.extractOne(query, self.baseball_strings)
        self.assertEqual(best[0], self.baseball_strings[0])

class ProcessTest(unittest.TestCase):

    def setUp(self):
        self.s1 = "new york mets"
        self.s1a = "new york mets"
        self.s2 = "new YORK mets"
        self.s3 = "the wonderful new york mets"
        self.s4 = "new york mets vs atlanta braves"
        self.s5 = "atlanta braves vs new york mets"
        self.s6 = "new york mets - atlanta braves"

        self.cirque_strings = [
            "cirque du soleil - zarkana - las vegas",
            "cirque du soleil ",
            "cirque du soleil las vegas",
            "zarkana las vegas",
            "las vegas cirque du soleil at the bellagio",
            "zarakana - cirque du soleil - bellagio"
        ]

        self.baseball_strings = [
            "new york mets vs chicago cubs",
            "chicago cubs vs chicago white sox",
            "philladelphia phillies vs atlanta braves",
            "braves vs mets",
        ]

    def testWithProcessor(self):
        events = [
            ["chicago cubs vs new york mets", "CitiField", "2011-05-11", "8pm"],
            ["new york yankees vs boston red sox", "Fenway Park", "2011-05-11", "8pm"],
            ["atlanta braves vs pittsburgh pirates", "PNC Park", "2011-05-11", "8pm"],
        ]
        query = "new york mets vs chicago cubs"
        processor = lambda event: event[0]

        best = process.extractOne(query, events, processor=processor)
        self.assertEqual(best[0], events[0])

    def testWithScorer(self):
        choices = [
            "new york mets vs chicago cubs",
            "chicago cubs at new york mets",
            "atlanta braves vs pittsbugh pirates",
            "new york yankees vs boston red sox"
        ]

        # in this hypothetical example we care about ordering, so we use quick ratio
        query = "new york mets at chicago cubs"
        scorer = QRatio

        # first, as an example, the normal way would select the "more 'complete' match of choices[1]"

        best = process.extractOne(query, choices)
        self.assertEqual(best[0], choices[1])

        # now, use the custom scorer

        best = process.extractOne(query, choices, scorer=scorer)
        self.assertEqual(best[0], choices[0])

    def testWithCutoff(self):
        choices = [
            "new york mets vs chicago cubs",
            "chicago cubs at new york mets",
            "atlanta braves vs pittsbugh pirates",
            "new york yankees vs boston red sox"
        ]

        query = "los angeles dodgers vs san francisco giants"

        # in this situation, this is an event that does not exist in the list
        # we don't want to randomly match to something, so we use a reasonable cutoff

        best = process.extractOne(query, choices, score_cutoff=50)
        self.assertTrue(best is None)
        #self.assertIsNone(best) # unittest.TestCase did not have assertIsNone until Python 2.7

        # however if we had no cutoff, something would get returned

        #best = process.extractOne(query, choices)
        #self.assertIsNotNone(best)

    def testEmptyStrings(self):
        choices = [
            "",
            "new york mets vs chicago cubs",
            "new york yankees vs boston red sox",
            "",
            ""
        ]

        query = "new york mets at chicago cubs"

        best = process.extractOne(query, choices)
        self.assertEqual(best[0], choices[1])

    def testNullStrings(self):
        choices = [
            None,
            "new york mets vs chicago cubs",
            "new york yankees vs boston red sox",
            None,
            None
        ]

        query = "new york mets at chicago cubs"

        best = process.extractOne(query, choices)
        self.assertEqual(best[0], choices[1])


if __name__ == '__main__':
    unittest.main()         # run all tests