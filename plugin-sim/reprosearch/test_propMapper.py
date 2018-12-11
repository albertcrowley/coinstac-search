from unittest import TestCase
from .PropMapper import PropMapper


class TestPropMapper(TestCase):

    def test_map(self):
        p = PropMapper('local5.nidm.ttl')
        et = p.map('http://neurolex.org/wiki/Category:DICOM_term/EchoTime')
        self.assertEqual("EchoTime", et, "Didn't match a DICOM term");

        am = p.map('http://uri.interlex.org/base/ilx_0352279')
        self.assertEqual("ADOS_MODULE", am, "failed mapping for ADOS_MODULE")

        uri = 'http://purl.org/nidash/nidm#SliceTiming'
        st = p.map(uri)
        self.assertEqual('SliceTiming', st, "failed mapping nidm term " + uri)

        pass
