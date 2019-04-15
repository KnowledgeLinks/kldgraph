from kldgraph import rdfuri


class BatchProcessor:

    def __init__(self, dataset, batch_consumer, batch_size=10000):
        self.dataset = dataset
        self.batch_size = batch_size
        self.count = 0
        self.batch_consumer = batch_consumer

    def increment(self):
        """
        increments the count and then test to see if the count has reached the batch size by calling test_size

        :return: None
        """
        self.count += 1
        self.test_szie()

    def test_size_send(self):
        """
        tests to see if the count has reached the batch size and if it has it tells the batch_consumer to send all data
        from the dataset.

        :return: None
        """
        if self.count >= self.batch_size:
            self.batch_consumer.send()
            self.dataset.clear_all()
            rdfuri.Node.clear_all_registries()
