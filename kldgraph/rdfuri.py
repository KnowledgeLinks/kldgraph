import json
import datetime
from enum import Enum
from uuid import uuid4, uuid1, uuid5
from kldgraph import dgraphapi


class NodeType(Enum):
    ALL = 0
    XID = 1
    UID = 2
    NS = 3
    BLANK = 4
    LITERAL = 5
    PRED = 6


class Geo(str):
    pass


DATA_TYPES = {
    "xs:string": str,
    "xs:dateTime": datetime.datetime,
    "xs:date": datetime.datetime,
    "xs:int": int,
    "xs:boolean": bool,
    "xs:double": float,
    "xs:float": float,
    "geo:geojson": Geo,
    "xs:password": str,
    "http://www.w3.org/2001/XMLSchema#string": str,
    "http://www.w3.org/2001/XMLSchema#dateTime": datetime.datetime,
    "http://www.w3.org/2001/XMLSchema#date": datetime.datetime,
    "http://www.w3.org/2001/XMLSchema#int": int,
    "http://www.w3.org/2001/XMLSchema#boolean": bool,
    "http://www.w3.org/2001/XMLSchema#double": float,
    "http://www.w3.org/2001/XMLSchema#float": float
}

STRING_DATATYPES = ["xs:string", "http://www.w3.org/2001/XMLSchema#string", "xs:password"]


class Literal:
    node_type = NodeType.LITERAL

    def __init__(self, value, data_type=None, lang=None):
        self.value = value
        self.data_type = data_type
        self.lang = lang

    @property
    def dgraph(self):
        if self.lang:
            return "%s@%s" % (self.quote_value(), self.lang)
        elif self.data_type in STRING_DATATYPES:
            return "%s^^<%s>" % (self.quote_value(), self.data_type)
        elif self.data_type:
            return '"%s"^^<%s>' % (self.value, self.data_type)
        else:
            return "%s^^<xs:string>" % self.quote_value()

    def quote_value(self):
        return json.dumps(self.value)


class NodeRegistryMeta(type):
    """

    """
    _registry = {NodeType.BLANK: {},
                 NodeType.XID: {},
                 NodeType.UID: {},
                 NodeType.PRED: {}}

    def __call__(cls, *args, **kwargs):
        # val = clear_signs(args[0])
        try:
            return cls._registry[args[1]][args[0]]
        except (KeyError, IndexError):
            node = super(NodeRegistryMeta, cls).__call__(*args, **kwargs)
            try:
                cls._registry[args[1]][args[0]] = node
            except IndexError:
                # no args were presented it is a new Blank node
                cls._registry[node.node_type][node.bid] = node
            return node

    @classmethod
    def clear_registry(mcs, node_type):
        if node_type == NodeType.ALL:
            for reg in mcs._registry.values():
                reg.clear()
        else:
            mcs._registry[node_type].clear()


class Node(metaclass=NodeRegistryMeta):
    # class Node:
    __slots__ = ['xid', 'uid', 'bid', 'hash_val', 'node_type', 'dgraph', 'not_looked_up']

    def __init__(self, value=None, node_type=None):
        """

        :param value:
        :param node_type:
        """
        self.node_type = node_type or NodeType.BLANK
        self.xid, self.uid, self.bid, self.dgraph, self.not_looked_up = None, None, None, None, None
        self._set_value(value)

    def _set_value(self, value):
        if not value and self.node_type == NodeType.BLANK:
            self.bid = "_:{}".format(new_id())
            self.not_looked_up = False
        else:
            if self.node_type == NodeType.BLANK:
                self.bid = value
                self.not_looked_up = False
                self.dgraph = value
            elif self.node_type == NodeType.PRED:
                self.uid = value
                self.xid = None
                self.not_looked_up = False
                self.dgraph = add_signs(value)
            elif self.node_type == NodeType.UID:
                self.uid = value
                self.not_looked_up = False
                self.dgraph = add_signs(value)
            elif self.node_type == NodeType.XID:
                self.xid = value
                self.not_looked_up = True
                # self.uid = dgraphapi.get_uid_for_xid(value)
        self.hash_val = hash(self.xid or self.uid or self.bid)

    def __repr__(self):
        return "Node({})".format(self.xid or self.uid or self.bid)

    def __hash__(self):
        return self.hash_val

    def __eq__(self, other):
        return hash(other) == self.hash_val

    def lookup_uid(self):
        if self.not_looked_up:
            self.uid = dgraphapi.get_uid_for_xid(self.xid)
            self.dgraph = add_signs(self.uid)
            self.not_looked_up = False

    @classmethod
    def clear_registry(cls, node_type):
        type(cls).clear_registry(node_type)

    @classmethod
    def clear_all_registries(cls):
        type(cls).clear_registry(NodeType.ALL)


def add_signs(value):
    return "<{}>".format(value)


def new_id(method="uuid"):
    """ Generates a unique identifier to be used with any dataset. The
        default method will use a random generated uuid based on computer
        and a random generated uuid.

        Args:
            method: "uuid" -> default random uuid generation
                    ???? -> other methods can be added later
    """
    if method == "uuid":
        return str(uuid5(uuid1(), str(uuid4())).hex)


def determine_node_type(value):
    """
    Determines if a value is a Blank Node, XID, UID or Literal

    :return NodeType:
    """
    if not value:
        return NodeType.BLANK
    if value[0] == "_":
        return NodeType.BLANK
    if value[0] == "<":
        if is_uri(value):
            return NodeType.XID
        return NodeType.UID
    return NodeType.LITERAL


def is_uri(value):
    """
    Weakly tests to see if the supplied string is a URI be seeing if it
    starts with '<htt' or 'http'. This is designed to be performant and
    not restrictive.

    :param value: the value to test
    :return: True if it appears to be a URI
    """
    try:
        # return value.lower().startswith("http")
        # if not (value[0] == 'h' or value[0] == 'H'):
        #     return False
        # if not (value[1] == 't' or value[1] == 'T'):
        #     return False
        # if not (value[2] == 't' or value[2] == 'T'):
        #     return False
        # if not (value[3] == 'p' or value[3] == 'P'):
        #     return False
        # return True
        # if not (value[0] == 'h'):
        #     return False
        # if not (value[1] == 't'):
        #     return False
        # if not (value[2] == 't'):
        #     return False
        # if not (value[3] == 'p'):
        #     return False
        # return True
        return value[:4] in ["<htt", "http"]
    except (TypeError, IndexError, AttributeError):
        return False


def clear_signs(value):
    """
    removes the <> from a uri string
    :param value: the string to clear
    :return:
    """
    if value[0] == "<":
        return value[1:-1]
    return value


def clean_iri(uri_string):
    """
    removes the <> signs from a string start and end
    :param uri_string:
    :return:
    """
    uri_string = str(uri_string).strip()
    if uri_string[:1] == "<" and uri_string[len(uri_string) - 1:] == ">":
        uri_string = uri_string[1:len(uri_string) - 1]
    return uri_string
