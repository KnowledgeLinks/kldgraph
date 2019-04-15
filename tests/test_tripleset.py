import unittest

from kldgraph import tripleset


class TriplePartSetTestCase(unittest.TestCase):

    def test_set_spo_to_save(self):
        tripset = tripleset.TriplePartSet()
        self.assertEqual(tripset.spo_to_save, 1)
        tripset.set_spo_to_save("Subject")
        self.assertEqual(tripset.spo_to_save, 0)
        tripset.set_spo_to_save("Pred")
        self.assertEqual(tripset.spo_to_save, 1)
        tripset.set_spo_to_save("Obj")
        self.assertEqual(tripset.spo_to_save, 2)
        tripset.set_spo_to_save(0)
        self.assertEqual(tripset.spo_to_save, 0)
        tripset.set_spo_to_save(1)
        self.assertEqual(tripset.spo_to_save, 1)
        tripset.set_spo_to_save(2)
        self.assertEqual(tripset.spo_to_save, 2)

    def test_triple(self):
        tripset = tripleset.TriplePartSet()
        tripset.triple("s", "p", "o")
        self.assertTrue("p" in tripset)
        tripset.triple("s", "p1", "o")
        tripset.triple("s", "p1", "o")
        tripset.triple("s", "p", "o")
        tripset.triple("s", "p", "o")
        self.assertTrue(len(tripset) == 2)
