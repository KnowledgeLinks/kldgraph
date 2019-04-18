import json
import pydgraph

DEFAULT_URL = 'localhost:9080'


class XidDoesNotExistError(Exception):
    pass


class Api:

    def __init__(self, url=DEFAULT_URL):
        self.url = url
        self.client_stub = pydgraph.DgraphClientStub(url)
        self.client = pydgraph.DgraphClient(self.client_stub)

    def get_uid_for_xid(self, xid):
        try:
            return self.find_uid_for_xid(xid)
        except XidDoesNotExistError:
            return self.create_uid_for_xid(xid)

    def find_uid_for_xid(self, xid):
        qry = """
            {{
                lookup(func: eq(xid, "{xid}"))
                    {{uid}}
            }}
            """.format(xid=xid)
        try:
            result = self.client.query(qry)
            data = json.loads(result.json)
            return data['lookup'][0]['uid']
        except (KeyError, IndexError):
            raise XidDoesNotExistError(xid)
        except Exception:
            self.add_xid_to_schema()
            raise XidDoesNotExistError(xid)

    def create_uid_for_xid(self, xid):
        data = {'xid': xid}
        txn = self.client.txn()
        uid = None
        try:
            result = txn.mutate(set_obj=data)
            txn.commit()
            uid = [result.uids[x] for x in result.uids][0]
        finally:
            txn.discard()
        return uid

    def add_xid_to_schema(self):
        """
        adds the xid schema to dgraph
        :return: True if added
        """
        schema = "xid: string @index(exact) ."
        op = pydgraph.Operation(schema=schema)
        self.client.alter(op)

    def mutate_add_dataset(self, dataset):
        """
        adds the triples in the dataset to dgraph
        :param dataset:
        :return:
        """
        dataset.lookup_nodes()
        txn = self.client.txn()
        try:
            result = txn.mutate(set_nquads=dataset.formatter.to_rdf())
            txn.commit()
        finally:
            txn.discard()
        return result

    def drop_all(self):
        """
        Drops all data from dgraph
        :return:
        """
        op = pydgraph.Operation(drop_all=True)
        self.client.alter(op)

# default instance of the API is generated on module load and the class methods of that instance are available at the
# module level.
default_api = Api()
drop_all = default_api.drop_all
mutate_add_dataset = default_api.mutate_add_dataset
add_xid_to_schema = default_api.add_xid_to_schema
create_uid_for_xid = default_api.create_uid_for_xid
find_uid_for_xid = default_api.find_uid_for_xid
get_uid_for_xid = default_api.get_uid_for_xid
