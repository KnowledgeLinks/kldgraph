__doc__ = """
License: GPL 2, W3C, BSD, or MIT
"""
import re
from rdflib.plugins.parsers.ntriples import (r_nodeid,
                                             r_literal,
                                             NTriplesParser,
                                             ParseError,
                                             unquote)
import kldgraph.rdfuri as rdfuri
from kldgraph.tracker import Tracker
from kldgraph import dataset
from kldgraph.batcher import BatchProcessor


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
    """
    The parser extends rdflib's NTriplesParser
    """
    count = 0

    def __init__(self, sink=None, use_tracker=False, tracker=None, use_batcher=False, batcher=None):
        if not sink:
            sink = dataset.Dataset()
        super().__init__(sink)
        self.tracker = None
        if use_tracker or tracker:
            if tracker:
                self.tracker = tracker
            else:
                self.tracker = Tracker()
        if use_batcher or batcher:
            if batcher:
                self.batcher = batcher
            else:
                self.batcher = BatchProcessor(sink)

    def parse(self, *args):
        if self.tracker:
            self.tracker.start()
        super().parse(*args)
        if self.batcher:
            self.batcher.batch_consumer.send()

    def readline(self):
        val = super().readline()
        self.count += 1
        if self.tracker:
            self.tracker.increment_count()
        if self.batcher:
            self.batcher.increment()
        return val

    def uriref(self):
        if self.peek('<'):
            uri = self.eat(r_uriref).group(1)
            uri = rdfuri.clear_signs(unquote(uri))
            return rdfuri.Node(uri, rdfuri.NodeType.XID)
        return False

    def nodeid(self):
        if self.peek('_'):
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
