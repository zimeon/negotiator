"""Memento tests."""
from datetime import datetime
try:  # Python 3
    from datetime.timezone import utc
except:  # Python 2
    from dateutil.tz import tzutc as utc
import re
import unittest

from negotiator2 import BadTimeMap, TimeMap, memento_parse_datetime, memento_datetime_string


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_memento_parse_datetime(self):
        """Test datetime parsing."""
        # a few datetimes from the Memento spec
        self.assertEqual(memento_parse_datetime("Thu, 31 May 2007 20:35:00 GMT").isoformat(),
                         "2007-05-31T20:35:00+00:00")
        self.assertEqual(memento_parse_datetime("Wed, 30 May 2007 18:47:52 GMT").isoformat(),
                         "2007-05-30T18:47:52+00:00")
        self.assertEqual(memento_parse_datetime("Tue, 20 Mar 2001 20:35:00 GMT").isoformat(),
                         "2001-03-20T20:35:00+00:00")
        self.assertEqual(memento_parse_datetime("Tue, 20 Mar 2001 13:36:10 GMT").isoformat(),
                         "2001-03-20T13:36:10+00:00")
        self.assertEqual(memento_parse_datetime("Tue, 15 Sep 2000 11:28:26 GMT").isoformat(),
                         "2000-09-15T11:28:26+00:00")
        # bad cases....
        self.assertRaises(ValueError, memento_parse_datetime, "")
        self.assertRaises(ValueError, memento_parse_datetime, "X")
        self.assertRaises(ValueError, memento_parse_datetime, "Thu, 31 May 2007 20:35:00 +0000")
        self.assertRaises(ValueError, memento_parse_datetime, "Thu, 31 May 2007 20:35:00")
        self.assertRaises(ValueError, memento_parse_datetime, "Thu, 31 May 2007 20:35:00.1 GMT")
        self.assertRaises(ValueError, memento_parse_datetime, "XYZ, 31 May 2007 20:35:00 GMT")
        # FIXME - these should be errors but aren't
        self.assertTrue(memento_parse_datetime("THu, 31 May 2007 20:35:00 GMT"))  # Bad case
        self.assertTrue(memento_parse_datetime("Thu, 30 JUN 2007 20:35:00 GMT"))  # Bad case
        self.assertTrue(memento_parse_datetime("Sat, 31 May 2007 20:35:00 GMT"))  # Wrong day

    def test02_memento_datetime_string(self):
        """Test memento_datetime_string."""
        self.assertEqual(memento_datetime_string(datetime(2009, 9, 23, 22, 15, 29)),
                         "Wed, 23 Sep 2009 22:15:29 GMT")
        self.assertEqual(memento_datetime_string(datetime(2001, 2, 3, 4, 5, 6)),
                         "Sat, 03 Feb 2001 04:05:06 GMT")

    def test10_timemap_init(self):
        """Test TimeMap initialiation and instance vars."""
        tm = TimeMap()
        self.assertEqual(tm.original, None)
        self.assertEqual(tm.mementos, {})
        self.assertEqual(tm.timegate, None)
        self.assertEqual(tm.timemap, None)
        self.assertEqual(tm.original_datetime, None)

    def test11_set_original(self):
        """Test setting of original and original_datetime."""
        tm = TimeMap()
        tm.set_original("URI-arrrgh!")
        self.assertEqual(tm.original, "URI-arrrgh!")
        self.assertEqual(tm.original_datetime, None)
        tm.set_original("URI-R", "Sat, 03 Feb 2001 04:05:06 GMT")
        self.assertEqual(tm.original, "URI-R")
        self.assertEqual(tm.original_datetime,
                         datetime(2001, 2, 3, 4, 5, 6, tzinfo=utc()))
        tm.set_original("URI-R2")
        self.assertEqual(tm.original, "URI-R2")
        self.assertEqual(tm.original_datetime, None)

    def test12_add_memento(self):
        """Test addition of memento."""
        tm = TimeMap()
        tm.add_memento("URI-M1", "Sat, 03 Feb 2001 04:05:06 GMT")
        self.assertEqual(len(tm.mementos), 1)
        self.assertEqual(tm.mementos[datetime(2001, 2, 3, 4, 5, 6, tzinfo=utc())], "URI-M1")

    def test13_timemap_serialize_link_format(self):
        """Test link format serialization."""
        tm = TimeMap()
        self.assertRaises(BadTimeMap, tm.serialize_link_format)
        tm.original = 'URI-R'
        self.assertEqual(tm.serialize_link_format(), '<URI-R>\n  ;rel="original"')
        tm.timegate = tm.original
        self.assertEqual(tm.serialize_link_format(), '<URI-R>\n  ;rel="original timegate"')
        tm.timegate = "URI-TG"
        self.assertTrue(re.search(r'''<URI-TG>\n  ;rel="timegate"''',
                                  tm.serialize_link_format()))
        tm.timegate = None
        tm.mementos[datetime(2001, 2, 3, 4, 5, 6)] = 'URI-M1'
        self.assertTrue(re.search(r'''<URI-M1>\n  ;rel="memento"\n  ;datetime="Sat, 03 Feb 2001 04:05:06 GMT"''',
                                  tm.serialize_link_format()))
        tm.timemap = "URI-TM"
        self.assertTrue(re.search(r'''<URI-TM>\n  ;rel="self"''',
                                  tm.serialize_link_format()))

    def test13_timemap_triples(self):
        """Test triples output."""
        tm = TimeMap()
        self.assertRaises(BadTimeMap, tm.triples)
        tm.original = 'URI-R'
        self.assertEqual(tm.triples(), [('URI-R', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://mementoweb.org/ns#Memento')])
        tm.timegate = tm.original
        self.assertTrue(('URI-R', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://mementoweb.org/ns#TimeGate') in tm.triples())
        tm.timegate = "URI-TG"
        self.assertTrue(('URI-TG', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://mementoweb.org/ns#TimeGate') in tm.triples())
        tm.timegate = None
        tm.mementos[datetime(2001, 2, 3, 4, 5, 6)] = 'URI-M1'
        self.assertTrue(('URI-M1', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://mementoweb.org/ns#Memento') in tm.triples())
        self.assertTrue(('URI-M1', 'http://mementoweb.org/ns#memento-datetime', '"Sat, 03 Feb 2001 04:05:06 GMT') in tm.triples())
        tm.timemap = "URI-TM"
        self.assertTrue(('URI-TM', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://mementoweb.org/ns#TimeMap') in tm.triples())
        n = len(tm.triples())
        tm.timegate = 'URI-TG2'
        self.assertEqual(len(tm.triples()), n + 3)  # TimeGate should add 3 triples
        self.assertTrue(('URI-M1', 'http://mementoweb.org/ns#timegate', 'URI-TG2') in tm.triples())
