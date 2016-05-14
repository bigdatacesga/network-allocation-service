import unittest
from .tests import TestAPI
from .test_disks import DisksTestCase
from .test_kvstore import KVStoreTestCase

suite = unittest.TestLoader().loadTestsFromTestCase(TestAPI)
suite = unittest.TestLoader().loadTestsFromTestCase(KVStoreTestCase)
suite = unittest.TestLoader().loadTestsFromTestCase(DisksTestCase)
