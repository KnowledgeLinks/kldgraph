
class NtDgraphFormatter:

    def __init__(self, dataset):
        self.dataset = dataset

    def to_rdf(self):
        rtn_list = []
        for subj, pred_ref in self.dataset.items():
            for pred, obj_ref in pred_ref.items():
                for obj in obj_ref:
                    rtn_list.append("%s %s %s .\n" % (subj.dgraph, pred.dgraph, obj.dgraph))
        return "".join(rtn_list)

    def to_json(self):
        pass