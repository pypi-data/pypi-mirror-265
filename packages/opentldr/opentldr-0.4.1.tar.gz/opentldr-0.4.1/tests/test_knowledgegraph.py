import unittest

import sys
sys.path.insert(0, 'src')

from opentldr import KnowledgeGraph as kg
from opentldr.Domain import ReferenceNode

class TestKg(unittest.TestCase):
    def test_default_connection(self):
        self.assertTrue(kg.connect())

    def test_run_query(self):
        rn= kg.add_reference_node(ReferenceNode(text="this is a test",type="TEST"))
        list = kg.cypher_query_to_list("MATCH (n:ReferenceNode) return n","n")
        self.assertTrue(rn in list)

        kg.delete_reference_node(rn)
        list = kg.cypher_query_to_list("MATCH (n:ReferenceNode) return n","n")
        self.assertFalse(rn in list)


unittest.main()