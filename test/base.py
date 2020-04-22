import unittest
import sys
import os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))


class TestCase(unittest.TestCase):
    maxDiff = None

    def assert_nvector_equal(self, a, b, places=None, msg=None, delta=None):
        from lottie import NVector
        self.assertIsInstance(a, NVector)
        self.assertIsInstance(b, NVector)

        if msg is None:
            msg = "%s != %s" % (a, b)
            msg_len = "%s (length mismatch %s != %s)" % (msg, len(a), len(b))
        else:
            msg_len = msg

        self.assertEqual(len(a), len(b), msg_len)

        for ia, ib in zip(a, b):
            self.assertAlmostEqual(ia, ib, places, msg, delta)
