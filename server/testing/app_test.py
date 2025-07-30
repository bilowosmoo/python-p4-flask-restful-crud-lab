import unittest
from flask import Flask,request
from app import app, db
from models import Plant

class PlantTests(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            db.session.add(Plant(name="Rose", image="img", price=12.0))
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_plants(self):
        res = self.client.get("/plants")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Rose", str(res.data))

    def test_patch_plant(self):
        res = self.client.patch("/plants/1", json={"is_in_stock": False})
        self.assertEqual(res.status_code, 200)
        
        data = res.get_json()
        self.assertIn("is_in_stock", data)
        self.assertFalse(data["is_in_stock"])


    def test_get_one_plant(self):
        res = self.client.get("/plants/1")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Rose", res.data)

    def test_delete_plant(self):
        res = self.client.delete("/plants/1")
        self.assertEqual(res.status_code, 204)

if __name__ == "__main__":
    unittest.main()
