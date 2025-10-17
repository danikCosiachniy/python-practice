import unittest
from tests.fake_db import FakeDB
from app.services import query_service as qs

class TestQueryService(unittest.TestCase):
    def test_rooms_counts_sql(self):
        db = FakeDB()
        db.set_query_result([{"id":1,"name":"R1","count":2}])
        rows = qs.rooms_counts(db)
        self.assertEqual(1, len(db.queries))
        self.assertIn("FROM rooms", db.queries[0][0])
        self.assertEqual([{"id":1,"name":"R1","count":2}], rows)

    def test_top5_young_avg_sql(self):
        db = FakeDB(); db.set_query_result([{"id":1}])
        qs.top5_young_avg(db)
        self.assertIn("LIMIT 5", db.queries[0][0])

    def test_top5_age_spread_sql(self):
        db = FakeDB(); db.set_query_result([{"id":1}])
        qs.top5_age_spread(db)
        sql = db.queries[0][0].lower()
        self.assertIn("max(age", sql)
        self.assertIn("min(age", sql)

    def test_mixed_gender_rooms_sql(self):
        db = FakeDB(); db.set_query_result([{"id":1}])
        qs.mixed_gender_rooms(db)
        self.assertIn("having count(distinct students.sex) >= 2",
                      db.queries[0][0].lower())

if __name__ == "__main__":
    unittest.main()