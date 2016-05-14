"""Tests for the kvstore API"""
import unittest
from app import kvstore
import Queue
import threading


ENDPOINT = 'http://10.112.0.101:8500/v1/kv'


class KVStoreTestCase(unittest.TestCase):

    def setUp(self):
        self.kv = kvstore.Client(ENDPOINT)

    def tearDown(self):
        self.kv.delete('__testing__', recursive=True)

    def test_set_new_key(self):
        key = '__testing__/testsetnew'
        value = '123456'
        self.kv.set(key, value)
        returned = self.kv.get(key)
        self.assertEqual(returned, value)

    def test_set_new_key_starting_with_slash(self):
        key = '/__testing__/testsetnew'
        value = '123456'
        self.kv.set(key, value)
        returned = self.kv.get(key)
        self.assertEqual(returned, value)

    def test_set_update_key(self):
        key = '__testing__/testsetupdate'
        value = 'orig'
        self.kv.set(key, value)
        value = 'new'
        self.kv.set(key, value)
        returned = self.kv.get(key)
        self.assertEqual(returned, value)

    def test_set_int_value(self):
        key = '__testing__/testsetnew'
        value = 1
        self.kv.set(key, value)
        returned = self.kv.get(key)
        self.assertEqual(int(returned), value)

    def test_get_existing_key(self):
        key = '__testing__/testget'
        value = '123456'
        self.kv.set(key, value)
        returned = self.kv.get(key)
        self.assertEqual(returned, value)

    def test_get_existing_key_starting_with_slash(self):
        key = '/__testing__/testget'
        value = '123456'
        self.kv.set(key, value)
        returned = self.kv.get(key)
        self.assertEqual(returned, value)

    def test_get_wait_returns_after_timeout_expired(self):
        key = '__testing__/testwaittimeout'
        expected = '000'
        self.kv.set(key, expected)
        index = self.kv.index(key)
        result = self.kv.get(key, wait=True, wait_index=index, timeout='1s')
        self.assertEqual(result, expected)

    def test_get_wait_with_index_and_timeout(self):
        key = '__testing__/testwait'
        initial = '000'
        expected = '123'
        self.kv.set(key, initial)
        index = self.kv.index(key)

        def wait_until_key_changes(key, index, timeout, q):
            q.put(self.kv.get(key, wait=True, wait_index=index, timeout=timeout))

        q = Queue.Queue()
        t = threading.Thread(target=wait_until_key_changes, args=(key, index, '5s', q))
        t.daemon = True
        t.start()
        self.kv.set(key, expected)
        t.join()
        result = q.get()
        self.assertEqual(result, expected)

    def test_recurse(self):
        expected = {'__testing__/r0': 'r0',
                    '__testing__/r0/r1': 'r1',
                    '__testing__/r0/r1/r2': 'r2'}
        for (k, v) in expected.items():
            self.kv.set(k, v)
        result = self.kv.recurse('__testing__')
        self.assertEqual(result, expected)

    def test_recurse_wait_with_index_and_timeout(self):
        key = '__testing__'
        initial = {'__testing__/r0': '',
                   '__testing__/r0/r1': '',
                   '__testing__/r0/r1/r2': ''}
        key_updated = '__testing__/r0/r1/r2'
        value_updated = 'FINAL'
        expected = {'__testing__/r0': '',
                    '__testing__/r0/r1': '',
                    key_updated: value_updated}
        for (k, v) in initial.items():
            self.kv.set(k, v)
        index = self.kv.index(key, recursive=True)

        def wait_until_key_changes(key, index, timeout, q):
            result = self.kv.recurse(key, wait=True, wait_index=index, timeout=timeout)
            q.put(result)

        q = Queue.Queue()
        t = threading.Thread(target=wait_until_key_changes, args=(key, index, '5s', q))
        t.daemon = True
        t.start()
        self.kv.set(key_updated, value_updated)
        t.join()
        result = q.get()
        self.assertEqual(result, expected)

    def test_index_increases(self):
        key = '__testing__/testindex'
        expected = '000'
        self.kv.set(key, expected)
        index1 = self.kv.index('__testing__/testwait')
        self.kv.set(key, expected)
        index2 = self.kv.index('__testing__/testwait')
        self.assertGreater(index2, index1)

    def test_delete_existing_key(self):
        key = '__testing__/testdelete'
        value = '123456'
        self.kv.set(key, value)

    def test_delete_non_existing_key(self):
        key = '__testing__/testdelete'
        self.kv.delete(key)
        self.assertRaises(kvstore.KeyDoesNotExist, self.kv.get, key)

    def test_delete_recursive(self):
        self.kv.set('__testing__/testdeleterecursive', 'XYZ')
        self.kv.set('__testing__/testdeleterecursive/level0', 'XYZ')
        self.kv.set('__testing__/testdeleterecursive/level0/level1', 'XYZ')
        self.kv.delete('__testing__/testdeleterecursive', recursive=True)
        self.assertRaises(kvstore.KeyDoesNotExist, self.kv.get, '__testing__/testdeleterecursive')

if __name__ == '__main__':
    unittest.main()
