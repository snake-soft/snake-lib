from unittest import TestCase
from snakelib.iterable import intersection


class ListTestCase(TestCase):
    
    def test_intersection(self):
        self.assertEqual(
            intersection(
                'abcd',
                'aefg',
                'aghi'
                ),
            'a',
            )
        self.assertEqual(
            intersection(
                ['a', 'b', 'c', 'd'],
                ['a', 'e', 'f', 'g'],
                ['a', 'g', 'h', 'i']
                ),
            ['a'],
            )
        self.assertEqual(
            intersection(
                {'a', 'b', 'c', 'd'},
                {'a', 'e', 'f', 'g'},
                {'a', 'g', 'h', 'i'}
                ),
            {'a'},
            )
