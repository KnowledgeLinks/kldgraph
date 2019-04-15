class TriplePartSet(set):

    def __init__(self, spo_to_save=1):
        super().__init__()
        self.spo_to_save = None
        self.set_spo_to_save(spo_to_save)

    def triple(self, *args):
        """
        receives a triple arguments and only stores a unique value for the specified
        subject, predicate, object as represented in spo_to_save
        :param sub: subject of the triple
        :param pred: predicate of the triple
        :param obj: object of the triple
        :return: None
        """

        self.add(args[self.spo_to_save])

    def set_spo_to_save(self, spo_to_save):
        """
        assigns an int to spo_to_save. Since the args for triple
        are presented as subj, pred, obj. we can use an int value
        0, 1, 2 to select the appropriate item to save

        :param spo_to_save: subj, pred, or obj that should be saved
        :return:
        """
        if isinstance(spo_to_save, int):
            self.spo_to_save = spo_to_save
        elif spo_to_save.lower().startswith("s"):
            self.spo_to_save = 0
        elif spo_to_save.lower().startswith("p"):
            self.spo_to_save = 1
        elif spo_to_save.lower().startswith("o"):
            self.spo_to_save = 2
