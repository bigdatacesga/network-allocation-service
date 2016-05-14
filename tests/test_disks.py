"""Tests for the generic service discovery API"""
import unittest
from app import disks


class DisksTestCase(unittest.TestCase):

    def setUp(self):
        self.prefix = '__testingdisks__/resources'
        #self.prefix = ''
        # Set the prefix for the testing entries generated
        disks.PREFIX = self.prefix
        for node in ('c13-1', 'c13-2'):
            for disk in range(12):
                disks._kv.set('{}/{}/disks/disk{}/status'
                              .format(self.prefix, node, disk), 'free')
        # Show all output when test fails
        self.maxDiff = None

    def tearDown(self):
        disks._kv.delete(self.prefix, recursive=True)

    def test_get_status_of_all_disks(self):
        expected = {'disk{}'.format(n): 'free' for n in range(12)}
        returned = disks.get('c13-1')
        self.assertEqual(returned, expected)

    def test_get_free_disks(self):
        expected = {'number': 12,
                    'disks': sorted(['disk{}'.format(n) for n in range(12)])}
        returned = disks.get_free('c13-1')
        self.assertEqual(returned, expected)

    def test_get_used_disks(self):
        expected = {'number': 0,
                    'disks': []}
        returned = disks.get_used('c13-1')
        self.assertEqual(returned, expected)

    def test_set_status(self):
        expected = 'username/mpi/cluster0'
        disks.set_status('c13-1', 'disk1', expected)
        returned = disks.get('c13-1')['disk1']
        self.assertEqual(returned, expected)

if __name__ == '__main__':
    unittest.main()
