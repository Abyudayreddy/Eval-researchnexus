import sys
import os
import uuid
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

os.environ["DATABASE_URL"] = "sqlite:///./test_eval_stage1.db"
os.environ.setdefault("GEMINI_API_KEY", "mock-key-for-tests")

from app.db.session import SessionLocal, engine, Base
from app.models.evaluation import EvaluationDataset, EvaluationItem, EvaluationExperiment, EvaluationRun, PublicationClaim
from app.services.evaluation_service import EvaluationService
from app.scripts.seed_benchmark_v10 import seed_benchmark_v10

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def test_stage1_benchmark_v10_seeding_and_gating():
    db = SessionLocal()
    try:
        # Seed benchmark v1.0
        seed_benchmark_v10()

        ds = db.query(EvaluationDataset).filter(EvaluationDataset.dataset_id == "ds_nexus_v10").first()
        assert ds is not None
        assert ds.version == "v1.0"
        assert ds.status == "READY"
        assert ds.is_frozen == "TRUE"
        assert ds.item_count == 100

        # Verify splits distribution (70 DEV, 15 VAL, 15 TEST)
        dev_items = db.query(EvaluationItem).filter(EvaluationItem.dataset_id == ds.dataset_id, EvaluationItem.split == "DEVELOPMENT").count()
        val_items = db.query(EvaluationItem).filter(EvaluationItem.dataset_id == ds.dataset_id, EvaluationItem.split == "VALIDATION").count()
        test_items = db.query(EvaluationItem).filter(EvaluationItem.dataset_id == ds.dataset_id, EvaluationItem.split == "TEST").count()

        assert dev_items == 70
        assert val_items == 15
        assert test_items == 15
    finally:
        db.close()

def test_stage1_freezing_immutability():
    db = SessionLocal()
    try:
        ds = db.query(EvaluationDataset).filter(EvaluationDataset.dataset_id == "ds_nexus_v10").first()
        assert ds.is_frozen == "TRUE"

        # Attempt to add item to frozen dataset -> Must raise ValueError
        with pytest.raises(ValueError, match="DATASET_FROZEN"):
            EvaluationService.add_evaluation_item(
                db=db,
                dataset_id=ds.dataset_id,
                question="Can frozen datasets be modified?",
                question_type="SINGLE_PAPER",
                split="DEVELOPMENT"
            )
    finally:
        db.close()

def test_stage1_e01_retrieval_only_experiment_execution():
    db = SessionLocal()
    try:
        ds = db.query(EvaluationDataset).filter(EvaluationDataset.dataset_id == "ds_nexus_v10").first()

        # 1. B1 Dense RAG
        exp_b1 = EvaluationService.create_experiment(
            db=db, name="E01 - B1 Dense RAG Baseline", dataset_id=ds.dataset_id, baseline_id="B1_DENSE_RAG"
        )
        res_b1 = EvaluationService.run_experiment(db, exp_b1.experiment_id)

        # 2. B2 BM25 RAG
        exp_b2 = EvaluationService.create_experiment(
            db=db, name="E01 - B2 BM25 RAG Baseline", dataset_id=ds.dataset_id, baseline_id="B2_BM25_RAG"
        )
        res_b2 = EvaluationService.run_experiment(db, exp_b2.experiment_id)

        # 3. B3 Hybrid RAG
        exp_b3 = EvaluationService.create_experiment(
            db=db, name="E01 - B3 Hybrid RAG Baseline", dataset_id=ds.dataset_id, baseline_id="B3_HYBRID_RAG"
        )
        res_b3 = EvaluationService.run_experiment(db, exp_b3.experiment_id)

        assert res_b1["status"] == "MEASURED"
        assert res_b2["status"] == "MEASURED"
        assert res_b3["status"] == "MEASURED"

        print("B1 Dense Paper Metrics:", res_b1["paper_metrics"])
        print("B2 BM25 Paper Metrics:", res_b2["paper_metrics"])
        print("B3 Hybrid Paper Metrics:", res_b3["paper_metrics"])

        # Paper-level metrics presence
        for r in [res_b1, res_b2, res_b3]:
            pm = r["paper_metrics"]
            assert "hit_at_1" in pm
            assert "hit_at_5" in pm
            assert "recall_at_5" in pm
            assert "precision_at_5" in pm
            assert "mrr" in pm
            assert "ndcg_at_5" in pm

            em = r["evidence_metrics"]
            assert "evidence_hit_at_5" in em
            assert "evidence_recall_at_5" in em
            assert "evidence_precision_at_5" in em

            lat = r["latency"]
            assert lat["p50_ms"] > 0
            assert lat["p95_ms"] >= lat["p50_ms"]

        # Hybrid RAG should outperform BM25 and Dense on MRR/Recall
        assert res_b3["paper_metrics"]["mrr"] >= res_b2["paper_metrics"]["mrr"]
        assert res_b3["paper_metrics"]["recall_at_5"] >= res_b1["paper_metrics"]["recall_at_5"]

    finally:
        db.close()

def test_stage1_paired_comparison_and_wilcoxon_test():
    db = SessionLocal()
    try:
        exp_b1 = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B1_DENSE_RAG").first()
        exp_b3 = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B3_HYBRID_RAG").first()

        comp = EvaluationService.compare_experiments(db, exp_b3.experiment_id, exp_b1.experiment_id)
        assert comp["status"] == "COMPARABLE"
        assert comp["paired_items_count"] > 0
        assert "bootstrap_95_ci" in comp
        assert comp["wilcoxon_test"]["statistically_significant"] is True
    finally:
        db.close()

def test_stage1_incompatible_run_protection():
    db = SessionLocal()
    try:
        ds_other = EvaluationService.create_dataset(db, name="Other Pilot Dataset", version="v0.1")
        # Add only 1 item to ds_other
        EvaluationService.add_evaluation_item(
            db, dataset_id=ds_other.dataset_id, question="Pilot question?", expected_paper_ids=["p1"]
        )
        exp_other = EvaluationService.create_experiment(db, name="Pilot Exp", dataset_id=ds_other.dataset_id, baseline_id="B1_DENSE_RAG")
        EvaluationService.run_experiment(db, exp_other.experiment_id)

        exp_b3 = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B3_HYBRID_RAG").first()

        comp = EvaluationService.compare_experiments(db, exp_b3.experiment_id, exp_other.experiment_id)
        assert comp["status"] == "NOT DIRECTLY COMPARABLE"
        assert "Item set mismatch" in comp["reason"]
    finally:
        db.close()

def test_stage1_publication_table_and_claim_audit():
    db = SessionLocal()
    try:
        package = EvaluationService.export_publication_package(db)
        assert package["reproducibility_export_version"] == "v1.0"
        assert "table1_datasets" in package["tables"]
        assert "table2_retrieval" in package["tables"]

        claims = package["publication_claim_audit"]
        claim1 = [c for c in claims if "Hybrid retrieval performs better" in c["text"]][0]
        assert claim1["status"] == "SUPPORTED"

        unmeasured = [c for c in claims if c["status"] == "NOT_MEASURED"]
        assert len(unmeasured) >= 1
    finally:
        db.close()

if __name__ == "__main__":
    test_stage1_benchmark_v10_seeding_and_gating()
    test_stage1_freezing_immutability()
    test_stage1_e01_retrieval_only_experiment_execution()
    test_stage1_paired_comparison_and_wilcoxon_test()
    test_stage1_incompatible_run_protection()
    test_stage1_publication_table_and_claim_audit()
    print("ALL EVALUATION STAGE 1 BENCHMARK & E01 TESTS PASSED SUCCESSFULLY [OK]")
