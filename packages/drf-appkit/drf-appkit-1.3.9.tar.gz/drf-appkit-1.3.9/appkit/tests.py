from django.test import TestCase

from .util import to_gsm7


VALID_GSM_STRING = 'This message contains only GSM-7 characters'
INVALID_GSM_STRING = "🥳 [It's] a $#!T 🥳 party 🥳"


class GSMTestCase(TestCase):
    def test_gsm7_to_gsm7(self):
        self.assertEqual(VALID_GSM_STRING, to_gsm7(VALID_GSM_STRING))

    def test_emoji_to_gsm7(self):
        # Note that leading and trailing whitespace are valid and therefore _NOT_ removed
        self.assertEqual(to_gsm7(INVALID_GSM_STRING), " [It's] a $#!T  party ")

    def test_to_gsm7_max_length(self):
        gsm_msg = to_gsm7(to_gsm7(INVALID_GSM_STRING), max_length=18)
        self.assertEqual(gsm_msg, " [It's] a $#!T  pa")
