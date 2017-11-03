"""Negotiator utility tests."""
import unittest

from negotiator2 import conneg_on_accept, negotiate_on_datetime, TimeMap, BadTimeMap


class TestAll(unittest.TestCase):
    """Class to run tests."""

    def test01_conneg_on_accept(self):
        """Test conneg based on accept header only."""
        self.assertEqual(
            conneg_on_accept(['a/b'], None),
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
        self.assertEqual(conneg_on_accept(['a'], None), 'a')
        # No server types is exception
        self.assertRaises(IndexError, conneg_on_accept, [], '')

    def test10_negotiate_on_datetime(self):
        """Test negotiation for Memento based on accept-datetime header only."""
        tm = TimeMap(original="URI-R")
        self.assertEqual(negotiate_on_datetime(tm, None), "URI-R")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 02 Nov 2017 16:29:00 GMT'), "URI-R")
        tm.set_original("URI-R2", 'Thu, 08 Aug 2017 08:08:08 GMT')
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 02 Nov 2017 16:29:00 GMT'), "URI-R2")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 31 Dec 1999 23:59:59 GMT'), "URI-R2")
        tm = TimeMap()
        tm.add_memento("URI-M1", 'Thu, 08 Aug 2017 02:08:08 GMT')
        tm.add_memento("URI-M2", 'Thu, 08 Aug 2017 05:08:08 GMT')
        tm.set_original("URI-R3", 'Thu, 08 Aug 2017 08:08:08 GMT')
        # default method=TimeMap.PREVIOUS
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 02 Nov 2017 16:29:00 GMT'), "URI-R3")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 08 Aug 2017 08:08:08 GMT'), "URI-R3")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 08 Aug 2017 08:08:07 GMT'), "URI-M2")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 08 Aug 2017 05:08:08 GMT'), "URI-M2")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 08 Aug 2017 04:08:08 GMT'), "URI-M1")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 08 Aug 2017 02:08:09 GMT'), "URI-M1")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 08 Aug 1991 01:01:01 GMT'), "URI-M1")
        # same times but method=TimeMap.CLOSEST
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 02 Nov 2017 16:29:00 GMT', method=TimeMap.CLOSEST), "URI-R3")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 08 Aug 2017 08:08:08 GMT', method=TimeMap.CLOSEST), "URI-R3")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 08 Aug 2017 08:08:07 GMT', method=TimeMap.CLOSEST), "URI-R3")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 08 Aug 2017 05:08:08 GMT', method=TimeMap.CLOSEST), "URI-M2")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 08 Aug 2017 04:08:08 GMT', method=TimeMap.CLOSEST), "URI-M2")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 08 Aug 2017 02:08:09 GMT', method=TimeMap.CLOSEST), "URI-M1")
        self.assertEqual(negotiate_on_datetime(tm, 'Thu, 08 Aug 1991 01:01:01 GMT', method=TimeMap.CLOSEST), "URI-M1")

    def test11_negotiate_on_datetime_error_cases(self):
        """Test negotiation for Memento based on accept-datetime header only."""
        self.assertRaises(BadTimeMap, negotiate_on_datetime, TimeMap(), None)
        self.assertRaises(BadTimeMap, negotiate_on_datetime, TimeMap(), 'Thu, 31 May 2007 20:35:00 GMT')
        # Bad accept-datetime header should always give last version
        tm = TimeMap(original="URI-R")
        self.assertEqual(negotiate_on_datetime(tm, 'junk'), "URI-R")
        tm = TimeMap()
        tm.add_memento("URI-M1", 'Thu, 11 May 2001 02:35:00 GMT')
        self.assertEqual(negotiate_on_datetime(tm, 'anything'), "URI-M1")
        tm = TimeMap()
        tm.set_original("URI-R", 'Thu, 08 Aug 2017 08:08:08 GMT')
        tm.add_memento("URI-M2", 'Thu, 03 Aug 2017 03:03:03 GMT')
        self.assertEqual(negotiate_on_datetime(tm, 'anything'), "URI-R")
        tm.add_memento("URI-M3", 'Thu, 09 Sep 2017 09:09:09 GMT')
        self.assertEqual(negotiate_on_datetime(tm, 'anything'), "URI-M3")
        self.assertEqual(negotiate_on_datetime(tm, 'anything', method=TimeMap.PREVIOUS), "URI-M3")
        self.assertEqual(negotiate_on_datetime(tm, 'anything', method=TimeMap.CLOSEST), "URI-M3")
