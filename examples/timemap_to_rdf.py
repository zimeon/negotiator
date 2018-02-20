"""Example code importing TimeMap.triples() into rdflib."""
from negotiator2 import TimeMap
from rdflib import Graph, URIRef, Literal

tm = TimeMap("URI-R")
tm.add_memento("URI-M1", 'Thu, 08 Aug 2017 02:08:08 GMT')
tm.add_memento("URI-M2", 'Thu, 08 Aug 2017 05:08:08 GMT')

g = Graph()
for (s, p, o, o_is_data) in tm.triples():
    g.add((URIRef(s), URIRef(p),
           Literal(o) if o_is_data else URIRef(o)))

print(g.serialize(format='nt'))
