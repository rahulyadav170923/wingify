import unittest, os
from multiprocessing import

read_case = {

}


class TestStringMethods(unittest.TestCase):

    def test_create(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_delete(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_update(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    def test_read(self):
        pass

    def test_search(self):
        pass

if __name__ == '__main__':
    unittest.main()