import unittest

class T(unittest.TestCase):
    @unittest.expectedFailure
    def test_xfail_subtests(self):
        with self.subTest(i=1):
            self.assertTrue(False)

        with self.subTest(i=2):
            self.assertFalse(True)

    @unittest.expectedFailure
    def test_xpass_subtests(self):
        with self.subTest(i=1):
            self.assertTrue(True)

    def test_fail_subtests(self):
        with self.subTest("Pass"):
            self.assertTrue(True)

        with self.subTest("Fail"):
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()