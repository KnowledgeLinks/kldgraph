import unittest

from kldgraph import dgraphapi, consumer, dataset, rdfuri, batcher


class BatchProcessorTestCase(unittest.TestCase):
    sub = rdfuri.Node("http://test.com/123", rdfuri.NodeType.XID)
    sub2 = rdfuri.Node("http://test.com/456", rdfuri.NodeType.XID)
    pred = rdfuri.Node("http://test.com/friend", rdfuri.NodeType.PRED)
    pred2 = rdfuri.Node("http://test.com/friend2", rdfuri.NodeType.PRED)
    obj = rdfuri.Literal("literal data", "xs:string")

    def test_init(self):
        data = dataset.Dataset()
        processor = batcher.BatchProcessor(data)
        # test default destination function
        self.assertEqual(processor.batch_consumer.destination, dgraphapi.mutate_add_dataset)

    def test_send(self):
        dgraphapi.drop_all()
        data = dataset.Dataset()
        batch_consumer = consumer.BatchConsumer(data)
        data.triple(self.sub, self.pred, self.obj)
        data.triple(self.sub, self.pred, rdfuri.Literal("literal data2", "xs:string"))
        result = batch_consumer.send()
        self.assertFalse(data)

    def test_batch(self):
        dgraphapi.drop_all()
        data = dataset.Dataset()
        processor = batcher.BatchProcessor(data, batch_size=10)
        batch_count = 0
        for i in range(1, 100):
            data.triple(self.sub, self.pred, rdfuri.Literal("literal data-%s" % i, "xs:string"))
            processor.increment()
            if processor.count == 0:
                batch_count += 1
        self.assertTrue(batch_count > 4)
