"""Negotiator utility tests."""
import unittest
from negotiator2 import conneg_on_accept

class TestAll(unittest.TestCase):
    """Class to run tests."""

    def test01_conneg_on_accept(self):
        """Test conneg based on accept header only."""
        self.assertEqual(
            conneg_on_accept(['a/b'],  None),
            'a/b')
        self.assertEqual(
            conneg_on_accept(['a/b'], ''),
            'a/b')
        self.assertEqual(
            conneg_on_accept(['a/b'], 'garbage'),
            'a/b')
        self.assertEqual(
            conneg_on_accept(['a/b', 'c/d'], 'garbage'),
            'a/b')
        self.assertEqual(
            conneg_on_accept(
                ['text/plain', 'text/html'],
                 'application/atom+xml;q=0.6, application/rdf+xml;q=0.9, text/html'),
            'text/html')
        self.assertEqual(
            conneg_on_accept(
                ['text/plain', 'text/html'],
                 'application/atom+xml, text/html'),
            'text/html')

    def test02_conneg_on_accept_error_cases(self):
        """Error cases for conneg on accept."""
        # Bad types should exhibit default behavior
        self.assertEqual(
            conneg_on_accept(['a'], None),
            'a')
        # No server types is exception
        self.assertRaises(IndexError,
            conneg_on_accept, [], '')

