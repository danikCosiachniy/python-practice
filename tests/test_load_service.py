import unittest, json, tempfile, os
from tests.fake_db import FakeDB
from app.services.load_service import _batched, load_rooms, load_students

class TestLoadService(unittest.TestCase):
    def test_batched(self):
        self.assertEqual(list(_batched([1,2,3,4,5], 2)), [[1,2],[3,4],[5]])

    def test_load_rooms(self):
        db = FakeDB()
        rooms = [{"id": 1, "name": "Room #1"}, {"id": 2, "name": "Room #2"}]
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json") as f:
            json.dump(rooms, f); path = f.name
        try:
            inserted = load_rooms(db, path, batch_size=1)
            self.assertEqual(2, inserted)
            self.assertEqual(2, len(db.executed_many))
            sql, batch1 = db.executed_many[0]
            self.assertIn("INSERT INTO rooms", sql)
            self.assertEqual((1, "Room #1"), batch1[0])
        finally:
            os.unlink(path)

    def test_load_students(self):
        db = FakeDB()
        students = [
            {"id": 10, "name": "Ann", "sex": "F", "birthday": "1999-05-01", "room_id": 1},
            {"id": 11, "name": "Bob", "sex": "M", "birthday": "1998-01-10", "room_id": 2},
        ]
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json") as f:
            json.dump(students, f); path = f.name
        try:
            inserted = load_students(db, path, batch_size=10)
            self.assertEqual(2, inserted)
            self.assertEqual(1, len(db.executed_many))
            sql, batch = db.executed_many[0]
            self.assertIn("INSERT INTO students", sql)
            self.assertEqual(10, batch[0][0])  # id первой записи
        finally:
            os.unlink(path)

if __name__ == "__main__":
    unittest.main()