import unittest, tempfile, os
from app.services import schema_service
from tests.fake_db import FakeDB

class TestSchemaService(unittest.TestCase):
    def test_ensure_schema_executes(self):
        db = FakeDB()
        f = tempfile.NamedTemporaryFile("w+", delete=False, suffix=".sql")
        try:
            f.write("CREATE TABLE t(x int);"); f.close()
            schema_service.ensure_schema(db, f.name)
            self.assertTrue(db.executed)
            self.assertIn("CREATE TABLE t", db.executed[0][0])
        finally:
            os.unlink(f.name)

    def test_ensure_indexes_executes(self):
        db = FakeDB()
        f = tempfile.NamedTemporaryFile("w+", delete=False, suffix=".sql")
        try:
            f.write("CREATE INDEX i ON t(x);"); f.close()
            schema_service.ensure_indexes(db, f.name)
            self.assertTrue(db.executed)
            self.assertIn("CREATE INDEX i", db.executed[-1][0])
        finally:
            os.unlink(f.name)

if __name__ == "__main__":
    unittest.main()