import unittest
import pprint
import gzip
from kldgraph import ntparse, dataset, tripleset, tracker


class NtParseTestCase(unittest.TestCase):
    data_file = "./data/sample.nt"
    error_data_file = "./data/parse_error_data.nt"

    def test_parse_normal(self):
        parser = ntparse.NtParser(dataset.Dataset())
        fo = open(self.data_file, "rb")
        data = parser.parse(fo)
        fo.close()
        self.assertTrue(data.triples())

    def test_parse_tripleset(self):
        parser = ntparse.NtParser(tripleset.TriplePartSet())
        fo = open(self.data_file, "rb")
        data = parser.parse(fo)
        fo.close()
        pprint.pprint(data)

    def test_parse_tripleset_gz(self):
        data_file = "/home/stabiledev/data/library/viaf/viaf-20190402-clusters-rdf.nt.gz"
        data = tripleset.TriplePartSet()
        parser = ntparse.NtParser(data, tracker=tracker.Tracker(1000000, 10000))
        try:
            fo = gzip.open(data_file, "rb")
            data = parser.parse(fo)
        except Exception as ex:
            print(ex)
        fo.close()
        pprint.pprint(data)

    def test_parse_error_normal(self):
        parser = ntparse.NtParser(dataset.Dataset())
        fo = open(self.error_data_file, "rb")
        data = parser.parse(fo)
        fo.close()
        self.assertTrue(data.triples())