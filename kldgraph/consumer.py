from kldgraph import dgraphapi, rdfuri


class BatchConsumer:
    """
    consumes data and transfers tha data
    """

    def __init__(self, dataset, destination=None):
        self.dataset = dataset
        self.destination = destination if destination else dgraphapi.mutate_add_dataset

    def send(self):
        """
        sends the data to the destination
        :return:
        """
        result = self.destination(self.dataset)
        self.dataset.clear()
        rdfuri.Node.clear_all_registries()
        return result
