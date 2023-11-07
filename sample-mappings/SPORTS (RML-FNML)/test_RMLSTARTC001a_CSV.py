__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "arenas.guerrero.julian@outlook.com"


import os
import morph_kgc
import rdflib
from pyoxigraph import Store


def test_RMLSTARTC001a():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output.nq')) as file:
        triples = file.readlines()
    g = [triple[:-2] for triple in triples]

    mapping_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mapping.ttl')
    config = f'[CONFIGURATION]\noutput_format=N-QUADS\n[DataSource]\nmappings={mapping_path}'

    g_morph = morph_kgc.materialize_set(config)

    assert set(g) == set(g_morph)


mapping_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mapping.ttl')
config = f'[CONFIGURATION]\noutput_format=N-QUADS\n[DataSource]\nmappings={mapping_path}'

g_morph = morph_kgc.materialize_set(config)
output = ""
for line in g_morph:
    output += line + "\n"

g = rdflib.Graph().parse(data=output, format="nquads")
print(g)
