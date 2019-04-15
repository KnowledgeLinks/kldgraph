from kldgraph.ntdgraphformatter import NtDgraphFormatter


class Dataset(dict):

    def __init__(self):
        super().__init__()
        self.formatter = NtDgraphFormatter(self)

    def triple(self, sub, pred, obj):
        """
        adds a triple to the dataset
        :param sub: subject of the triple
        :param pred: predicate of the triple
        :param obj: object of the triple
        :return: None
        """
        try:
            self[sub][pred].append(obj)
        except KeyError:
            try:
                self[sub][pred] = [obj]
            except KeyError:
                self[sub] = {pred: [obj]}
        except AttributeError:
            self[sub][pred] = [obj]

    def triples(self):
        rtn_list = []
        for subj, pred_ref in self.items():
            for pred, obj_ref in pred_ref.items():
                for obj in obj_ref:
                    rtn_list.append((subj, pred, obj,))
        return rtn_list

    def lookup_nodes(self):
        for subj, pred_ref in self.items():
            subj.lookup_uid()
            for obj_ref in pred_ref.values():
                for obj in obj_ref:
                    try:
                        obj.lookup_uid()
                    except AttributeError:
                        pass

    def are_nodes_set(self):
        for subj, pred_ref in self.items():
            if subj.not_looked_up:
                return False
            for obj_ref in pred_ref.values():
                for obj in obj_ref:
                    try:
                        if obj.not_looked_up:
                            return False
                    except AttributeError:
                        pass
        return True

    def clear(self):
        """
        cycles through the dictionary object to ensure all circular reference are removed
        :return: None
        """
        for subj, pred_ref in self.items():
            for pred in pred_ref.keys():
                self[subj][pred].clear()
            self[subj].clear()
        super().clear()

