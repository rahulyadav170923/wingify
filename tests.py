import unittest, os
import requests
from app import LocalData
from multiprocessing import Process
from app import run

headers={'Content-Type':'application/json','Authorization':'Basic cGFzc3dvcmQ=','username':'admin'}

class TestStringMethods(unittest.TestCase):

    def test_get(self):
        data = requests.get('http://0.0.0.0:8000/products',headers=headers)
        self.assertEqual(data.json(), LocalData.products)

    def test_post(self):
        requests.post('http://0.0.0.0:8000/products',headers=headers,json={'id':'product2'})
        data_get = requests.get('http://0.0.0.0:8000/products/product2',headers=headers)
        self.assertTrue(data_get.json(),{'id':'product2'})

    def test_put(self):
        requests.post('http://0.0.0.0:8000/products/product2',headers=headers,json={'id':'product2','cost':'20'})
        data_get = requests.get('http://0.0.0.0:8000/products/product2',headers=headers)
        self.assertTrue(data_get.json(),{'id':'product2','cost':'20'})

    def test_delete(self):
        requests.delete('http://0.0.0.0:8000/products/product2',headers=headers)
        data_get = requests.get('http://0.0.0.0:8000/products/product2',headers=headers)
        self.assertTrue(data_get.json(),{"status": "200","msg": "record_deleted"})

    # def test_search(self):
    #     pass

if __name__ == '__main__':
    p1 = Process(target = run)
    p1.start()
    p2 = Process(target = unittest.main)
    p2.start()
    p2.join(timeout=1)
    p1.terminate()