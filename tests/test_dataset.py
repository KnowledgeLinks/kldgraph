import unittest
import timeit
import pprint
from kldgraph import dataset, rdfuri, dgraphapi


class TestDatasetLoading(unittest.TestCase):
    sub = rdfuri.Node("http://test.com/123", rdfuri.NodeType.XID)
    sub2 = rdfuri.Node("http://test.com/456", rdfuri.NodeType.XID)
    pred = rdfuri.Node("http://test.com/friend", rdfuri.NodeType.PRED)
    obj = rdfuri.Literal("literal data", "xs:string")

    def test_triple(self):
        data = dataset.Dataset()
        data.triple(self.sub, self.pred, self.obj)
        self.assertTrue(self.obj in data[self.sub][self.pred])
        self.assertTrue(self.sub in data.keys())
        self.assertTrue(self.pred in data[self.sub].keys())
        data.triple(self.sub, self.pred, self.obj)
        self.assertTrue(len(data[self.sub][self.pred]) == 2)
        pprint.pprint(data.triples())

    def test_are_nodes_set(self):
        data = dataset.Dataset()
        data.triple(self.sub, self.pred, self.obj)
        self.assertFalse(data.are_nodes_set())

    def test_lookup_nodes(self):
        rdfuri.NodeRegistryMeta.clear_registry(rdfuri.NodeType.XID)
        data = dataset.Dataset()
        data.triple(self.sub2, self.pred, self.obj)
        data.triple(self.sub2, self.pred, self.obj)
        data.triple(self.sub2, self.pred, self.obj)
        self.assertFalse(data.are_nodes_set())
        data.lookup_nodes()
        self.assertTrue(data.are_nodes_set())

    def test_formatter(self):
        data = dataset.Dataset()
        data.triple(self.sub, self.pred, self.obj)
        data.triple(self.sub, self.pred, rdfuri.Literal("literal data2", "xs:string"))
        data.triple(self.sub, self.pred, rdfuri.Literal("literal data3", "xs:string"))
        data.lookup_nodes()
        print(data.formatter.to_rdf())

    def test_mutate_dataset(self):
        data = dataset.Dataset()
        data.triple(self.sub, self.pred, self.obj)
        data.triple(self.sub, self.pred, rdfuri.Literal("literal data2", "xs:string"))
        data.triple(self.sub, self.pred, rdfuri.Literal("literal data3", "xs:string"))
        dgraphapi.mutate_add_dataset(data)
