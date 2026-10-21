import os
import sys
import unittest

# Load env variables manually to prevent pydantic validation errors
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().replace("\x00", "")
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.db.session import SessionLocal
from app.models.paper import Paper
from app.services.assistant.context_manager import ContextManager

class TestContextEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Insert mock papers for testing
        db = SessionLocal()
        db.query(Paper).filter(Paper.id.in_(["p1", "p2", "p3", "p4"])).delete(synchronize_session=False)
        for pid in ["p1", "p2", "p3", "p4"]:
            db.add(Paper(id=pid, title=f"Mock Paper {pid}", authors="Mock Author"))
        db.commit()
        db.close()

    @classmethod
    def tearDownClass(cls):
        # Clean up mock papers
        db = SessionLocal()
        db.query(Paper).filter(Paper.id.in_(["p1", "p2", "p3", "p4"])).delete(synchronize_session=False)
        db.commit()
        db.close()

    def test_reordered_hash(self):
        # Equivalent reordered papers must produce same hash
        ctx1 = ContextManager.validate_and_resolve(
            session_id="session-1",
            mode="compare",
            scope="selected_papers",
            paper_ids=["p1", "p2", "p3"]
        )
        ctx2 = ContextManager.validate_and_resolve(
            session_id="session-1",
            mode="compare",
            scope="selected_papers",
            paper_ids=["p3", "p1", "p2"]
        )
        self.assertEqual(ctx1.context_hash, ctx2.context_hash)

    def test_changed_paper_hash(self):
        # Different papers must produce different hash
        ctx1 = ContextManager.validate_and_resolve(
            session_id="session-1",
            mode="compare",
            scope="selected_papers",
            paper_ids=["p1", "p2", "p3"]
        )
        ctx2 = ContextManager.validate_and_resolve(
            session_id="session-1",
            mode="compare",
            scope="selected_papers",
            paper_ids=["p1", "p2", "p4"]
        )
        self.assertNotEqual(ctx1.context_hash, ctx2.context_hash)

    def test_compare_boundaries(self):
        # Reject comparison if paper list <2 or >5
        with self.assertRaises(ValueError) as context:
            ContextManager.validate_and_resolve(
                session_id="session-1", mode="compare", scope="selected_papers", paper_ids=["p1"]
            )
        self.assertEqual(str(context.exception), "COMPARE_TOO_FEW")

        with self.assertRaises(ValueError) as context:
            ContextManager.validate_and_resolve(
                session_id="session-1", mode="compare", scope="selected_papers", paper_ids=["p1","p2","p3","p4","p5","p6"]
            )
        self.assertEqual(str(context.exception), "COMPARE_TOO_MANY")

if __name__ == "__main__":
    unittest.main()
