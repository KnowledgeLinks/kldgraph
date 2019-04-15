import re
from rdflib.plugins.parsers.ntriples import (r_nodeid,
                                             r_literal,
                                             NTriplesParser,
                                             ParseError,
                                             unquote)
import kldgraph.rdfuri as rdfuri
from kldgraph.tracker import Tracker


class Store:
    def __init__(self):
        self.data = []

    def triple(self, s, p, o):
        self.data.append((s, p, o,))


# the rdflib regex for URIs is too restrictive. here we remove the 'quote' and 'space'
# restrictions from the regex
uriref_loose = r'<([^:]+:[^<>]+)>'
r_uriref = re.compile(uriref_loose)


class NtParser(NTriplesParser):
    count = 0

    def __init__(self, sink=None, use_tracker=False, tracker=None):
        super().__init__(sink)
        self.tracker = None
        if use_tracker or tracker:
            if tracker:
                self.tracker = tracker
            else:
                self.tracker = Tracker()

    def parse(self, *args):
        if self.tracker:
            self.tracker.start()
        super().parse(*args)

    def readline(self):
        val = super().readline()
        self.count += 1
        if self.tracker:
            self.tracker.increment_count()
        return val

    def uriref(self):
        if self.peek('<'):
            uri = self.eat(r_uriref).group(1)
            uri = rdfuri.clear_signs(unquote(uri))
            return rdfuri.Node(uri, rdfuri.NodeType.XID)
        return False

    def nodeid(self):
        if self.peek('_'):
            # Fix for https://github.com/RDFLib/rdflib/issues/204
            bnode_id = self.eat(r_nodeid).group(1)
            return rdfuri.Node(bnode_id, rdfuri.NodeType.BLANK)
        return False

    def literal(self):
        if self.peek('"'):
            lit, lang, dtype = self.eat(r_literal).groups()
            if lang:
                lang = lang
            else:
                lang = None
            if dtype:
                dtype = dtype
            else:
                dtype = None
            if lang and dtype:
                raise ParseError("Can't have both a language and a datatype")
            lit = unquote(lit)
            return rdfuri.Literal(lit, dtype, lang)
        return False
