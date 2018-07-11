import unittest
from app import app

class TestRequest(unittest.TestCase):
    def test_hello(self):
        with app.test_client() as client:
            response = client.get("/")
            self.assertEqual(response.get_json()['msg'], "Hello World!")

    def test_info(self):
        with app.test_client() as client:
            response = client.get("/wargame/1")
            self.assertEqual(response.get_json()['title'], "Web Shell 탐지")
            response = client.get("/wargame/2")
            self.assertEqual(response.get_json()['title'], "Remote Buffer Overflow")
    
    def test_start(self):
        with app.test_client() as client:
            response = client.post("/wargame/start"
                ,json={'wargame_id':'1'})
            self.assertEqual(response.get_json()['msg'], "Requested to start : 1")
            response = client.post("/wargame/start"
                ,json={'wargame_id':'2'})
            self.assertEqual(response.get_json()['msg'], "Requested to start : 2")


if __name__ == '__main__':
    unittest.main()
    