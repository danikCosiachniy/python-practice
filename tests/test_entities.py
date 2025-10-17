import unittest
from datetime import date
from app.domain.entities import student_from_json, room_from_json

class TestEntities(unittest.TestCase):
    def test_room_from_json_ok(self):
        r = room_from_json({"id": 5, "name": "Room #5"})
        self.assertEqual(5, r.id)
        self.assertEqual("Room #5", r.name)

    def test_student_from_json_ok(self):
        s = student_from_json({
            "id": 42, "name": "Alice", "sex": "F",
            "birthday": "2000-01-02", "room_id": 7
        })
        self.assertEqual(42, s.id)
        self.assertEqual("F", s.sex)
        self.assertEqual(date(2000, 1, 2), s.birthday)
        self.assertEqual(7, s.room_id)

    def test_student_invalid_sex(self):
        with self.assertRaises(ValueError):
            student_from_json({"id": 1, "name": "X", "sex": "Z",
                               "birthday": "2000-01-01", "room_id": 1})

    def test_student_missing_room_id(self):
        with self.assertRaises(ValueError):
            student_from_json({"id": 1, "name": "X", "sex": "M", "birthday": "2000-01-01"})

if __name__ == "__main__":
    unittest.main()