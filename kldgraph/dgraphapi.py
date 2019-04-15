import json
import pydgraph

client_stub = pydgraph.DgraphClientStub('localhost:9080')
client = pydgraph.DgraphClient(client_stub)


class XidDoesNotExistError(Exception):
    pass


def get_uid_for_xid(xid):
    try:
        return find_uid_for_xid(xid)
    except XidDoesNotExistError:
        return create_uid_for_xid(xid)


def find_uid_for_xid(xid):
    qry = """
        {{
            lookup(func: eq(xid, "{xid}"))
                {{uid}}
        }}
        """.format(xid=xid)
    try:
        result = client.query(qry)
        data = json.loads(result.json)
        return data['lookup'][0]['uid']
    except (KeyError, IndexError):
        raise XidDoesNotExistError(xid)
    except Exception:
        add_xid_to_schema()
        raise XidDoesNotExistError(xid)


def create_uid_for_xid(xid):
    data = {'xid': xid}
    txn = client.txn()
    uid = None
    try:
        result = txn.mutate(set_obj=data)
        txn.commit()
        uid = [result.uids[x] for x in result.uids][0]
    finally:
        txn.discard()
    return uid


def add_xid_to_schema():
    """
    adds the xid schema to dgraph
    :return: True if added
    """
    schema = "xid: string @index(exact) ."
    op = pydgraph.Operation(schema=schema)
    client.alter(op)


def mutate_add_dataset(dataset):
    """
    adds the triples in the dataset to dgraph
    :param dataset:
    :return:
    """
    dataset.lookup_nodes()
    txn = client.txn()
    try:
        result = txn.mutate(set_nquads=dataset.formatter.to_rdf())
        txn.commit()
    finally:
        txn.discard()


def drop_all():
    """
    Drops all data from dgraph
    :return:
    """
    op = pydgraph.Operation(drop_all=True)
    client.alter(op)
