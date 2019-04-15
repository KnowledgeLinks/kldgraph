import unittest
import timeit

from kldgraph import rdfuri

RUN_TIMEIT = False


class TestUriFunctions(unittest.TestCase):
    valid_uris = ["http://wwww.schema.org/Person",
                  "http://wwww.schema.org/Person"]
    invalid_uris = [None, "xsdjkl", "h"]

    # @unittest.skip("performance")
    def test_is_uri(self):
        for uri in self.valid_uris:
            self.assertTrue(rdfuri.is_uri(uri))
        for uri in self.invalid_uris:
            self.assertFalse(rdfuri.is_uri(uri))
        if RUN_TIMEIT:
            print("is_uri time: ",
                  timeit.timeit('rdfuri.is_uri("http://wwww.schema.org/Person")', globals=globals()))

    # @unittest.skip("performance")
    def test_clear_signs(self):
        self.assertEqual(rdfuri.clear_signs("<x012>"), "x012")
        self.assertEqual(rdfuri.clear_signs("x012"), "x012")
        if RUN_TIMEIT:
            print("clear_signs time: ",
                  timeit.timeit('rdfuri.clear_signs("<x0123>")', globals=globals()))
            print("clear_signs time no sign: ",
                  timeit.timeit('rdfuri.clear_signs("x0123")', globals=globals()))
            print("clean_iri time: ",
                  timeit.timeit('rdfuri.clean_iri("<x0123>")', globals=globals()))

    # @unittest.skip("performance")
    def test_node_meta(self):
        x = rdfuri.Node("http://www.google.com/test", rdfuri.NodeType.XID)
        y = rdfuri.Node("http://www.google.com/test", rdfuri.NodeType.XID)
        b = rdfuri.Node("_:a1", rdfuri.NodeType.BLANK)
        if RUN_TIMEIT:
            print("make node time: ",
                  timeit.timeit('rdfuri.Node("http://www.google.com/test", rdfuri.NodeType.XID)', globals=globals()))
            print("make new blanknode time: ",
                  timeit.timeit('rdfuri.Node("_:a1", rdfuri.NodeType.BLANK)', globals=globals()))
        self.assertEqual(id(x), id(y))


class TestNodeRegistryMeta(unittest.TestCase):

    def test_clear_registry(self):
        node = rdfuri.Node()
        reg = rdfuri.NodeRegistryMeta
        self.assertTrue(reg._registry[node.node_type])
        reg.clear_registry(node.node_type)
        self.assertFalse(reg._registry[node.node_type])

    def test_registry(self):
        for i in range(10):
            node = rdfuri.Node()
        reg = rdfuri.NodeRegistryMeta
        self.assertTrue(len(reg._registry[node.node_type]) == 10)
        reg.clear_registry(node.node_type)


class TestLiteral(unittest.TestCase):

    def test_literal_assignments(self):
        self.assertEqual(rdfuri.Literal("""test "a" of 'b' in a string""", "xs:string").dgraph,
                         '''"test \\"a\\" of 'b' in a string"^^<xs:string>''')
        self.assertEqual(rdfuri.Literal(1, "xs:int").dgraph,
                         '''"1"^^<xs:int>''')


if __name__ == "__main__":
    unittest.main()
