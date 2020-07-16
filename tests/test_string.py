from unittest import TestCase
from snakelib.string import remove_bad_chars


class StringTestCase(TestCase):
    
    def test_remove_bad_chars(self):
        bad_chars = '-+*~Ü'
        string = 'bli#bla-blubbütest*string'
        self.assertEqual(
            remove_bad_chars(string, bad_chars),
            'bli#blablubbüteststring',
            )
        self.assertEqual(
            remove_bad_chars(string, bad_chars, case_sensitive=False),
            'bli#blablubbteststring',
            )
