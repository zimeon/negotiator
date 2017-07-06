"""Negotiator tests."""
import unittest
from negotiator2 import AcceptParameters, ContentType, Language, ContentNegotiator


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_content_type(self):
        """CONTENT TYPE."""
        accept = "text/plain"
        server = [AcceptParameters(ContentType("text/plain"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept=accept)
        self.assertEqual(str(ap), 'AcceptParameters:: Content Type: text/plain;')
        self.assertEqual(str(ap.content_type), 'text/plain')

        # application/atom+xml vs application/rdf+xml without q values
        accept = "application/atom+xml, application/rdf+xml"
        server = [AcceptParameters(ContentType("application/rdf+xml")),
                  AcceptParameters(ContentType("application/atom+xml"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept=accept)
        self.assertEqual(str(ap.content_type), 'application/atom+xml')

        # application/atom+xml vs application/rdf+xml with q values
        accept = "application/atom+xml;q=0.6, application/rdf+xml;q=0.9"
        server = [AcceptParameters(ContentType("application/rdf+xml")),
                  AcceptParameters(ContentType("application/atom+xml"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept=accept)
        self.assertEqual(str(ap.content_type), 'application/rdf+xml')

        # application/atom+xml vs application/rdf+xml vs text/html
        # with mixed q values
        accept = "application/atom+xml;q=0.6, application/rdf+xml;q=0.9, text/html"
        server = [AcceptParameters(ContentType("application/rdf+xml")),
                  AcceptParameters(ContentType("application/atom+xml")),
                  AcceptParameters(ContentType("text/html"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept=accept)
        self.assertEqual(str(ap.content_type), 'text/html')

        # text/plain only, unsupported by server
        accept = "text/plain"
        server = [AcceptParameters(ContentType("text/html"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept=accept)
        self.assertEqual(str(ap), 'None')

        # application/atom+xml vs application/rdf+xml vs text/html
        # with mixed q values, most preferred unavailable
        accept = "application/atom+xml;q=0.6, application/rdf+xml;q=0.9, text/html"
        server = [AcceptParameters(ContentType("application/rdf+xml")),
                  AcceptParameters(ContentType("application/atom+xml"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept=accept)
        self.assertEqual(str(ap.content_type), 'application/rdf+xml')

        # application/atom+xml vs application/rdf+xml vs text/html
        # with mixed q values, most preferred available
        accept = "application/atom+xml;q=0.6, application/rdf+xml;q=0.9, text/html"
        server = [AcceptParameters(ContentType("application/rdf+xml")),
                  AcceptParameters(ContentType("text/html"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept=accept)
        self.assertEqual(str(ap.content_type), 'text/html')

        # application/atom+xml;type=feed supported by server
        accept = "application/atom+xml;type=feed"
        server = [AcceptParameters(ContentType("application/atom+xml;type=feed"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept=accept)
        self.assertEqual(str(ap.content_type), 'application/atom+xml;type=feed')

        # image/* supported by server
        accept = "image/*"
        server = [AcceptParameters(ContentType("text/plain")),
                  AcceptParameters(ContentType("image/png")),
                  AcceptParameters(ContentType("image/jpeg"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept=accept)
        self.assertEqual(str(ap.content_type), 'image/png')

        # */* supported by server
        accept = "*/*"
        server = [AcceptParameters(ContentType("text/plain")),
                  AcceptParameters(ContentType("image/png")),
                  AcceptParameters(ContentType("image/jpeg"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept=accept)
        self.assertEqual(str(ap.content_type), 'text/plain')

    def test02_language(self):
        """LANGUAGE."""
        # en only
        accept_language = "en"
        server = [AcceptParameters(language=Language("en"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept_language=accept_language)
        self.assertEqual(str(ap), "AcceptParameters:: Language: en;")
        self.assertEqual(str(ap.language), 'en')

        # en vs de without q values
        accept = "en, de"
        server = [AcceptParameters(language=Language("en")),
                  AcceptParameters(language=Language("de"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept_language=accept)
        self.assertEqual(str(ap.language), 'en')

        # fr vs no with q values
        accept = "fr;q=0.7, no;q=0.8"
        server = [AcceptParameters(language=Language("fr")),
                  AcceptParameters(language=Language("no"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept_language=accept)
        self.assertEqual(str(ap.language), 'no')

        # en vs de vs fr with mixed q values
        accept = "en;q=0.6, de;q=0.9, fr"
        server = [AcceptParameters(language=Language("en")),
                  AcceptParameters(language=Language("de")),
                  AcceptParameters(language=Language("fr"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept_language=accept)
        self.assertEqual(str(ap.language), 'fr')

        # en only, unsupported by server
        accept = "en"
        server = [AcceptParameters(language=Language("de"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept_language=accept)
        self.assertEqual(ap, None)

        # en vs no vs de with mixed q values, most preferred unavailable
        accept = "en;q=0.6, no;q=0.9, de"
        server = [AcceptParameters(language=Language("en")),
                  AcceptParameters(language=Language("no"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept_language=accept)
        self.assertEqual(str(ap.language), 'no')

        # en vs no vs de with mixed q values, most preferred available
        accept = "en;q=0.6, no;q=0.9, de"
        server = [AcceptParameters(language=Language("no")),
                  AcceptParameters(language=Language("de"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept_language=accept)
        self.assertEqual(str(ap.language), 'de')

        # en-gb supported by server
        accept = "en-gb"
        server = [AcceptParameters(language=Language("en-gb"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept_language=accept)
        self.assertEqual(str(ap.language), 'en-gb')

        # en-gb, unsupported by server
        accept = "en-gb"
        server = [AcceptParameters(language=Language("en"))]
        cn = ContentNegotiator(acceptable=server,
                               ignore_language_variants=False)
        ap = cn.negotiate(accept_language=accept)
        self.assertEqual(ap, None)

        # en-gb, supported by server through language variants
        accept = "en-gb"
        server = [AcceptParameters(language=Language("en"))]
        cn = ContentNegotiator(acceptable=server,
                               ignore_language_variants=True)
        ap = cn.negotiate(accept_language=accept)
        self.assertEqual(str(ap.language), 'en')

        # en, partially supported by server
        accept = "en"
        server = [AcceptParameters(language=Language("en-gb"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept_language=accept)
        self.assertEqual(str(ap.language), 'en-gb')

        # * by itself
        accept = "*"
        server = [AcceptParameters(language=Language("no")),
                  AcceptParameters(language=Language("de"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept_language=accept)
        self.assertEqual(str(ap.language), 'no')

        # * with other options, primary option unsupported
        accept = "en, *"
        server = [AcceptParameters(language=Language("no")),
                  AcceptParameters(language=Language("de"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept_language=accept)
        self.assertEqual(str(ap.language), 'no')

        # * with other options, primary option supported
        accept = "en, *"
        server = [AcceptParameters(language=Language("en")),
                  AcceptParameters(language=Language("de"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept_language=accept)
        self.assertEqual(str(ap.language), 'en')

    def test03_language_and_content_type(self):
        """LANGUAGE+CONTENT TYPE."""
        # content type and language specified
        accept = "text/html"
        accept_lang = "en"
        server = [AcceptParameters(ContentType("text/html"),
                  Language("en"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept=accept, accept_language=accept_lang)
        self.assertEqual(str(ap.content_type), 'text/html')
        self.assertEqual(str(ap.language), 'en')

        # 2 content types and one language specified
        accept = "text/html, text/plain"
        accept_lang = "en"
        server = [AcceptParameters(ContentType("text/html"),
                                   Language("de")),
                  AcceptParameters(ContentType("text/plain"),
                                   Language("en"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept=accept, accept_language=accept_lang)
        self.assertEqual(str(ap.content_type), 'text/plain')
        self.assertEqual(str(ap.language), 'en')

        # 2 content types and 2 languages specified
        accept = "text/html, text/plain"
        accept_lang = "en, de"
        server = [AcceptParameters(ContentType("text/html"), Language("de")),
                  AcceptParameters(ContentType("text/plain"), Language("en"))]
        cn = ContentNegotiator(acceptable=server)
        ap = cn.negotiate(accept=accept, accept_language=accept_lang)
        self.assertEqual(str(ap.content_type), 'text/html')
        self.assertEqual(str(ap.language), 'de')

        # 2 content types and one language specified, with weights
        weights = {'content_type': 2.0, 'language': 1.0, 'charset': 1.0,
                   'encoding': 1.0}
        accept = "text/html, text/plain"
        accept_lang = "en"
        server = [AcceptParameters(ContentType("text/html"), Language("de")),
                  AcceptParameters(ContentType("text/plain"), Language("en"))]
        cn = ContentNegotiator(acceptable=server, weights=weights)
        ap = cn.negotiate(accept=accept, accept_language=accept_lang)
        self.assertEqual(str(ap.content_type), 'text/plain')
        self.assertEqual(str(ap.language), 'en')
