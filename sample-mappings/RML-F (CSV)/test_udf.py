__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "arenas.guerrero.julian@outlook.com"


import os
import morph_kgc

from rdflib.graph import Graph
from rdflib import compare


def test_udf():
    g = Graph()
    g.parse(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output.nq'))

    mapping_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mapping.ttl')
    udf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'udf.py')
    config = f'[CONFIGURATION]\noutput_format=N-QUADS\nudfs={udf_path}\n[DataSource]\nmappings={mapping_path}'
    g_morph = morph_kgc.materialize(config)
    print(g_morph)

    assert compare.isomorphic(g, g_morph)


mapping_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mapping.ttl')
udf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'udf.py')
config = f'[CONFIGURATION]\noutput_format=N-QUADS\nudfs={udf_path}\n[DataSource]\nmappings={mapping_path}'
try:
    g_morph = morph_kgc.materialize(config)
    print(g_morph.serialize(format="ttl"))
except Exception as e:
    print("\n\n")
    print(e)

# test_udf()