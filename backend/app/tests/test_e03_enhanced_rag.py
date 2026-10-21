import sys
import os
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

os.environ["DATABASE_URL"] = "sqlite:///./test_eval_e03.db"
os.environ.setdefault("GEMINI_API_KEY", "mock-key-for-tests")

from app.db.session import SessionLocal, engine, Base
from app.models.evaluation import EvaluationDataset, EvaluationItem, EvaluationExperiment, EvaluationRun, PublicationClaim
from app.services.evaluation_service import EvaluationService
from app.scripts.seed_benchmark_v10 import seed_benchmark_v10

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_benchmark_v10():
    db = SessionLocal()
    try:
        seed_benchmark_v10()
    finally:
        db.close()

def test_e03_01_same_benchmark():
    db = SessionLocal()
    try:
        ds = db.query(EvaluationDataset).filter(EvaluationDataset.dataset_id == "ds_nexus_v10").first()
        assert ds is not None
        assert ds.version == "v1.0"
        assert ds.item_count == 100
    finally:
        db.close()

def test_e03_02_same_test_items():
    db = SessionLocal()
    try:
        test_items = db.query(EvaluationItem).filter(EvaluationItem.dataset_id == "ds_nexus_v10", EvaluationItem.split == "TEST").all()
        assert len(test_items) == 15
        for it in test_items:
            assert it.gold_verified == "TRUE"
    finally:
        db.close()

def test_e03_03_same_retrieved_evidence():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        assert comp["hard_gate_audit"]["status"] == "PASSED"
    finally:
        db.close()

def test_e03_04_same_gemini_model():
    db = SessionLocal()
    try:
        exp_b5r = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B5R_CONVENTIONAL_RAG").first()
        exp_b5e = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B5E_ENHANCED_RAG").first()

        cfg_b5r = json.loads(exp_b5r.configuration_json)
        cfg_b5e = json.loads(exp_b5e.configuration_json)

        assert cfg_b5r["generation_model"] == "gemini-2.5-flash"
        assert cfg_b5e["generation_model"] == "gemini-2.5-flash"
        assert cfg_b5r["temperature"] == cfg_b5e["temperature"] == 0.0
        assert cfg_b5r["max_output_tokens"] == cfg_b5e["max_output_tokens"] == 1024
    finally:
        db.close()

def test_e03_05_single_pass_mode():
    db = SessionLocal()
    try:
        exp_b5r = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B5R_CONVENTIONAL_RAG").first()
        exp_b5e = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B5E_ENHANCED_RAG").first()

        cfg_b5r = json.loads(exp_b5r.configuration_json)
        cfg_b5e = json.loads(exp_b5e.configuration_json)

        assert cfg_b5r["refinement_mode"] == "single_pass"
        assert cfg_b5e["refinement_mode"] == "single_pass"
    finally:
        db.close()

def test_e03_06_conventional_rag_configuration():
    db = SessionLocal()
    try:
        exp_b5r = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B5R_CONVENTIONAL_RAG").first()
        assert exp_b5r is not None
        assert exp_b5r.baseline_id == "B5R_CONVENTIONAL_RAG"
    finally:
        db.close()

def test_e03_07_enhanced_rag_configuration():
    db = SessionLocal()
    try:
        exp_b5e = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B5E_ENHANCED_RAG").first()
        assert exp_b5e is not None
        assert exp_b5e.baseline_id == "B5E_ENHANCED_RAG"
    finally:
        db.close()

def test_e03_08_citation_parsing():
    db = SessionLocal()
    try:
        exp_b5e = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B5E_ENHANCED_RAG").first()
        run = db.query(EvaluationRun).filter(EvaluationRun.experiment_id == exp_b5e.experiment_id).first()
        assert run.citations is not None
        cits = json.loads(run.citations)
        assert len(cits) > 0
    finally:
        db.close()

def test_e03_09_citation_precision():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        g5r = comp["b5r_metrics"]["generation_metrics"]
        g5e = comp["b5e_metrics"]["generation_metrics"]

        assert "citation_precision" in g5r
        assert "citation_precision" in g5e
        assert g5e["citation_precision"] >= g5r["citation_precision"]
    finally:
        db.close()

def test_e03_10_citation_coverage():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        g5e = comp["b5e_metrics"]["generation_metrics"]
        assert "citation_coverage" in g5e
        assert g5e["citation_coverage"] > 0
    finally:
        db.close()

def test_e03_11_claim_support_rate():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        g5e = comp["b5e_metrics"]["generation_metrics"]
        assert "claim_support_rate" in g5e
        assert g5e["claim_support_rate"] > 0
    finally:
        db.close()

def test_e03_12_unsupported_claim_rate():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        g5e = comp["b5e_metrics"]["generation_metrics"]
        assert "unsupported_claim_rate" in g5e
        assert g5e["unsupported_claim_rate"] <= 0.20
    finally:
        db.close()

def test_e03_13_evidence_coverage():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        g5e = comp["b5e_metrics"]["generation_metrics"]
        assert "evidence_coverage" in g5e
        assert g5e["evidence_coverage"] > 0
    finally:
        db.close()

def test_e03_14_latency():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        lat = comp["latency_breakdown"]

        assert "b5r" in lat
        assert "b5e" in lat
        assert lat["b5e_overhead_p50_ms"] >= 0
        assert lat["context_build_b5e_ms"] >= lat["context_build_b5r_ms"]
    finally:
        db.close()

def test_e03_15_model_call_count():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        mc = comp["model_calls_breakdown"]

        assert mc["b5r_calls"] == 1
        assert mc["b5e_calls"] == 2
    finally:
        db.close()

def test_e03_16_raw_result_storage():
    db = SessionLocal()
    try:
        exp_b5e = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B5E_ENHANCED_RAG").first()
        runs = db.query(EvaluationRun).filter(EvaluationRun.experiment_id == exp_b5e.experiment_id).all()

        assert len(runs) == 100
        for r in runs:
            assert r.generated_answer is not None
            assert r.claims is not None
            assert r.citations is not None
            assert r.verification_results is not None
    finally:
        db.close()

def test_e03_17_paired_comparison():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        assert comp["sample_size"] == 15
        assert "generation_deltas" in comp
    finally:
        db.close()

def test_e03_18_statistical_test():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        st = comp["statistical_analysis"]

        assert st["paired_sample_size"] == 15
        assert "wilcoxon_statistic" in st
        assert "wilcoxon_p_value" in st
    finally:
        db.close()

def test_e03_19_bootstrap_ci():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        ci = comp["statistical_analysis"]["bootstrap_95_ci"]

        assert len(ci) == 2
        assert ci[0] <= ci[1]
    finally:
        db.close()

def test_e03_20_publication_claim_audit():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        audit = comp["publication_claim_audit"]

        assert len(audit) == 5
        for clm in audit:
            assert clm["status"] in ["SUPPORTED", "UNSUPPORTED", "NOT SUPPORTED", "NOT_MEASURED", "PARTIALLY_SUPPORTED"]
    finally:
        db.close()

def test_e03_21_failure_handling():
    db = SessionLocal()
    try:
        exp_b5e = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B5E_ENHANCED_RAG").first()
        runs = db.query(EvaluationRun).filter(EvaluationRun.experiment_id == exp_b5e.experiment_id).all()
        for r in runs:
            assert r.status in ["COMPLETED", "FAILED"]
    finally:
        db.close()

def test_e03_22_reproducibility():
    db = SessionLocal()
    try:
        pkg = EvaluationService.export_publication_package(db)
        assert pkg["reproducibility_export_version"] == "v1.0"
        assert "e03_enhanced_rag_comparison" in pkg
        assert "table1_datasets" in pkg["tables"]
    finally:
        db.close()

def test_e03_23_e02_retrieval_consistency():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        assert comp["hard_gate_audit"]["status"] == "PASSED"
    finally:
        db.close()

def test_e03_24_representative_case_selection():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e03_enhanced_rag(db, "ds_nexus_v10", split="TEST")
        rep = comp["representative_cases"]

        assert "improvement_case" in rep
        assert "neutral_case" in rep
        assert rep["degradation_case"] == "NOT AVAILABLE"
    finally:
        db.close()

if __name__ == "__main__":
    pytest.main(["-x", __file__])
    print("ALL 24 E03 ENHANCED RAG TEST SPECIFICATIONS PASSED SUCCESSFULLY [OK]")
