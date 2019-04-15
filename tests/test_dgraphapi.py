import unittest

from kldgraph import dgraphapi


class DgraphapiTestCase(unittest.TestCase):
    uri = "http://test.com/"

    @classmethod
    def setUpClass(cls):
        dgraphapi.drop_all()
        dgraphapi.add_xid_to_schema()

    def test_create_and_uid_for_xid(self):
        uid = dgraphapi.create_uid_for_xid(self.uri + '1')
        self.assertEqual(uid, dgraphapi.find_uid_for_xid(self.uri + '1'))

    def test_find_uid_for_xid(self):
        self.assertRaises(dgraphapi.XidDoesNotExistError,
                          dgraphapi.find_uid_for_xid,
                          "http://test.com/does_not_exist")

    def test_get_uid_for_xid(self):
        self.assertIsNotNone(dgraphapi.get_uid_for_xid(self.uri + '3'))

    def test_find_uid_for_xid_with_no_xid_schema(self):
        dgraphapi.drop_all()
        uid = dgraphapi.create_uid_for_xid("http://test.com")
        dgraphapi.drop_all()
        dgraphapi.add_xid_to_schema()

    @classmethod
    def tearDownClass(cls):
        dgraphapi.drop_all()

