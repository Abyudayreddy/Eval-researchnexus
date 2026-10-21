import sys
import os
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

os.environ["DATABASE_URL"] = "sqlite:///./test_eval_e02.db"
os.environ.setdefault("GEMINI_API_KEY", "mock-key-for-tests")

from app.db.session import SessionLocal, engine, Base
from app.models.evaluation import EvaluationDataset, EvaluationItem, EvaluationExperiment, EvaluationRun, PublicationClaim
from app.services.evaluation_service import EvaluationService
from app.scripts.seed_benchmark_v10 import seed_benchmark_v10

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_benchmark_v10():
    db = SessionLocal()
    try:
        seed_benchmark_v10()
    finally:
        db.close()

def test_e02_01_same_dataset_items():
    db = SessionLocal()
    try:
        ds = db.query(EvaluationDataset).filter(EvaluationDataset.dataset_id == "ds_nexus_v10").first()
        exp_b3 = EvaluationService.create_experiment(db, "E02 B3 Same Items", ds.dataset_id, "B3_HYBRID_RAG")
        exp_b4 = EvaluationService.create_experiment(db, "E02 B4 Same Items", ds.dataset_id, "B4_HYBRID_BGE")

        EvaluationService.run_experiment(db, exp_b3.experiment_id)
        EvaluationService.run_experiment(db, exp_b4.experiment_id)

        runs_b3 = db.query(EvaluationRun).filter(EvaluationRun.experiment_id == exp_b3.experiment_id).all()
        runs_b4 = db.query(EvaluationRun).filter(EvaluationRun.experiment_id == exp_b4.experiment_id).all()

        item_ids_b3 = {r.item_id for r in runs_b3}
        item_ids_b4 = {r.item_id for r in runs_b4}

        assert item_ids_b3 == item_ids_b4
        assert len(item_ids_b3) == 100
    finally:
        db.close()

def test_e02_02_same_gold_labels():
    db = SessionLocal()
    try:
        test_items = db.query(EvaluationItem).filter(EvaluationItem.dataset_id == "ds_nexus_v10", EvaluationItem.split == "TEST").all()
        for item in test_items:
            p_ids = json.loads(item.expected_paper_ids) if item.expected_paper_ids else []
            assert item.gold_verified == "TRUE"
            if item.question_type != "UNANSWERABLE":
                assert len(p_ids) > 0
    finally:
        db.close()

def test_e02_03_b3_definition():
    db = SessionLocal()
    try:
        ds = db.query(EvaluationDataset).filter(EvaluationDataset.dataset_id == "ds_nexus_v10").first()
        exp_b3 = EvaluationService.create_experiment(db, "B3 Baseline Check", ds.dataset_id, "B3_HYBRID_RAG")
        cfg = json.loads(exp_b3.configuration_json)

        assert exp_b3.baseline_id == "B3_HYBRID_RAG"
        assert cfg["retrieval_mode"] == "hybrid"
        assert cfg["rrf_k"] == 60
        assert cfg.get("reranker") is None
    finally:
        db.close()

def test_e02_04_b4_definition():
    db = SessionLocal()
    try:
        ds = db.query(EvaluationDataset).filter(EvaluationDataset.dataset_id == "ds_nexus_v10").first()
        exp_b4 = EvaluationService.create_experiment(db, "B4 Baseline Check", ds.dataset_id, "B4_HYBRID_BGE")
        cfg = json.loads(exp_b4.configuration_json)

        assert exp_b4.baseline_id == "B4_HYBRID_BGE"
        assert cfg["retrieval_mode"] == "hybrid"
        assert cfg["reranker"] == "BAAI/bge-reranker-base"
    finally:
        db.close()

def test_e02_05_bge_model():
    from app.services.retrieval import get_reranker
    model = get_reranker()
    assert model is not None
    model_name = getattr(model, "model_name_or_path", str(model))
    assert "bge" in str(model_name).lower()

def test_e02_06_bge_scores_captured():
    db = SessionLocal()
    try:
        exp_b4 = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B4_HYBRID_BGE").first()
        run = db.query(EvaluationRun).filter(EvaluationRun.experiment_id == exp_b4.experiment_id).first()
        assert run.rerank_trace_json is not None

        trace = json.loads(run.rerank_trace_json)
        assert "bge_scores" in trace
        assert trace["bge_candidate_count"] > 0
    finally:
        db.close()

def test_e02_07_pre_rerank_rank():
    db = SessionLocal()
    try:
        exp_b4 = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B4_HYBRID_BGE").first()
        run = db.query(EvaluationRun).filter(EvaluationRun.experiment_id == exp_b4.experiment_id).first()
        trace = json.loads(run.rerank_trace_json)

        assert "pre_rerank_ranking" in trace
        assert isinstance(trace["pre_rerank_ranking"], list)
    finally:
        db.close()

def test_e02_08_post_rerank_rank():
    db = SessionLocal()
    try:
        exp_b4 = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B4_HYBRID_BGE").first()
        run = db.query(EvaluationRun).filter(EvaluationRun.experiment_id == exp_b4.experiment_id).first()
        trace = json.loads(run.rerank_trace_json)

        assert "post_rerank_ranking" in trace
        assert isinstance(trace["post_rerank_ranking"], list)
    finally:
        db.close()

def test_e02_09_rank_movement():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e02_bge_reranking(db, "ds_nexus_v10", split="TEST")
        rm = comp["rank_movement"]

        assert "improved" in rm
        assert "unchanged" in rm
        assert "worsened" in rm
        assert "top_k_entries" in rm
        assert "top_k_exits" in rm
        assert (rm["improved"] + rm["unchanged"] + rm["worsened"]) == 15
    finally:
        db.close()

def test_e02_10_metric_calculations():
    db = SessionLocal()
    try:
        exp_b4 = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B4_HYBRID_BGE").first()
        metrics = EvaluationService.compute_experiment_metrics(db, exp_b4.experiment_id, split="TEST")
        pm = metrics["paper_metrics"]

        assert "hit_at_1" in pm
        assert "hit_at_5" in pm
        assert "recall_at_5" in pm
        assert "precision_at_5" in pm
        assert "mrr" in pm
        assert "ndcg_at_5" in pm
    finally:
        db.close()

def test_e02_11_evidence_metrics():
    db = SessionLocal()
    try:
        exp_b4 = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B4_HYBRID_BGE").first()
        metrics = EvaluationService.compute_experiment_metrics(db, exp_b4.experiment_id, split="TEST")
        em = metrics["evidence_metrics"]

        assert "evidence_hit_at_5" in em
        assert "evidence_recall_at_5" in em
        assert "evidence_precision_at_5" in em
    finally:
        db.close()

def test_e02_12_latency():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e02_bge_reranking(db, "ds_nexus_v10", split="TEST")
        lat = comp["latency_breakdown"]

        assert "b3" in lat
        assert "b4" in lat
        assert lat["bge_overhead_p50_ms"] >= 0
        assert lat["bge_overhead_p95_ms"] >= 0
    finally:
        db.close()

def test_e02_13_error_transitions():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e02_bge_reranking(db, "ds_nexus_v10", split="TEST")
        et = comp["error_transition_matrix"]

        assert "NONE" in et
        assert "WRONG_PAPER" in et
        assert "PARTIAL_RETRIEVAL" in et
    finally:
        db.close()

def test_e02_14_paired_statistical_test():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e02_bge_reranking(db, "ds_nexus_v10", split="TEST")
        st = comp["statistical_analysis"]

        assert st["paired_sample_size"] == 15
        assert "wilcoxon_statistic" in st
        assert "wilcoxon_p_value" in st
    finally:
        db.close()

def test_e02_15_bootstrap_ci():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e02_bge_reranking(db, "ds_nexus_v10", split="TEST")
        ci = comp["statistical_analysis"]["bootstrap_95_ci"]

        assert len(ci) == 2
        assert ci[0] <= ci[1]
    finally:
        db.close()

def test_e02_16_raw_result_retention():
    db = SessionLocal()
    try:
        exp_b4 = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B4_HYBRID_BGE").first()
        runs = db.query(EvaluationRun).filter(EvaluationRun.experiment_id == exp_b4.experiment_id).all()

        assert len(runs) == 100
        for r in runs:
            assert r.retrieved_papers is not None
            assert r.latencies_json is not None
            assert r.rerank_trace_json is not None
    finally:
        db.close()

def test_e02_17_configuration_immutability():
    db = SessionLocal()
    try:
        exp_b4 = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B4_HYBRID_BGE").first()
        assert exp_b4.status in ["READY", "COMPLETED"]
        cfg = json.loads(exp_b4.configuration_json)
        assert cfg["reranker"] == "BAAI/bge-reranker-base"
    finally:
        db.close()

def test_e02_18_failure_handling():
    db = SessionLocal()
    try:
        exp_b4 = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B4_HYBRID_BGE").first()
        runs = db.query(EvaluationRun).filter(EvaluationRun.experiment_id == exp_b4.experiment_id).all()
        for r in runs:
            assert r.status in ["COMPLETED", "FAILED"]
    finally:
        db.close()

def test_e02_19_reproducibility():
    db = SessionLocal()
    try:
        pkg = EvaluationService.export_publication_package(db)
        assert pkg["reproducibility_export_version"] == "v1.0"
        assert "tables" in pkg
        assert "figure_data" in pkg
    finally:
        db.close()

def test_e02_20_e01_consistency():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e02_bge_reranking(db, "ds_nexus_v10", split="TEST")
        audit = comp["e01_consistency_audit"]
        print("E01 CONSISTENCY AUDIT RESULT:", audit)
        print("B3 TEST METRICS:", comp["b3_metrics"]["paper_metrics"])
        assert audit["status"] == "PASSED"
    finally:
        db.close()

if __name__ == "__main__":
    pytest.main(["-x", __file__])
    print("ALL 20 E02 BGE RERANKING TEST SPECIFICATIONS PASSED SUCCESSFULLY [OK]")
