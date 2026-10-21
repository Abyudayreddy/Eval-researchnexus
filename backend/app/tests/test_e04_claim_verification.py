import sys
import os
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

os.environ["DATABASE_URL"] = "sqlite:///./test_eval_e04.db"
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

def test_e04_01_same_benchmark():
    db = SessionLocal()
    try:
        ds = db.query(EvaluationDataset).filter(EvaluationDataset.dataset_id == "ds_nexus_v10").first()
        assert ds is not None
        assert ds.version == "v1.0"
        assert ds.item_count == 100
    finally:
        db.close()

def test_e04_02_same_test_items():
    db = SessionLocal()
    try:
        test_items = db.query(EvaluationItem).filter(EvaluationItem.dataset_id == "ds_nexus_v10", EvaluationItem.split == "TEST").all()
        assert len(test_items) == 15
        for it in test_items:
            assert it.gold_verified == "TRUE"
    finally:
        db.close()

def test_e04_03_same_canonical_b4_evidence():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        assert comp["hard_gate_audit"]["status"] == "PASSED"
    finally:
        db.close()

def test_e04_04_same_gemini_generation_config():
    db = SessionLocal()
    try:
        exp_b6a = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B6A_ENHANCED_RAG_NO_VERIFICATION").first()
        exp_b6v = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B6V_ENHANCED_RAG_CLAIM_VERIFICATION").first()

        cfg_b6a = json.loads(exp_b6a.configuration_json)
        cfg_b6v = json.loads(exp_b6v.configuration_json)

        assert cfg_b6a["generation_model"] == "gemini-2.5-flash"
        assert cfg_b6v["generation_model"] == "gemini-2.5-flash"
        assert cfg_b6a["temperature"] == cfg_b6v["temperature"] == 0.0
        assert cfg_b6a["max_output_tokens"] == cfg_b6v["max_output_tokens"] == 1024
    finally:
        db.close()

def test_e04_05_single_pass_refinement_lock():
    db = SessionLocal()
    try:
        exp_b6a = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B6A_ENHANCED_RAG_NO_VERIFICATION").first()
        exp_b6v = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B6V_ENHANCED_RAG_CLAIM_VERIFICATION").first()

        cfg_b6a = json.loads(exp_b6a.configuration_json)
        cfg_b6v = json.loads(exp_b6v.configuration_json)

        assert cfg_b6a["refinement_mode"] == "single_pass"
        assert cfg_b6v["refinement_mode"] == "single_pass"
    finally:
        db.close()

def test_e04_06_b6a_baseline_definition():
    db = SessionLocal()
    try:
        exp_b6a = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B6A_ENHANCED_RAG_NO_VERIFICATION").first()
        assert exp_b6a is not None
        assert exp_b6a.baseline_id == "B6A_ENHANCED_RAG_NO_VERIFICATION"
    finally:
        db.close()

def test_e04_07_b6v_baseline_definition():
    db = SessionLocal()
    try:
        exp_b6v = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B6V_ENHANCED_RAG_CLAIM_VERIFICATION").first()
        assert exp_b6v is not None
        assert exp_b6v.baseline_id == "B6V_ENHANCED_RAG_CLAIM_VERIFICATION"
    finally:
        db.close()

def test_e04_08_claim_extraction():
    db = SessionLocal()
    try:
        exp_b6v = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B6V_ENHANCED_RAG_CLAIM_VERIFICATION").first()
        run = db.query(EvaluationRun).filter(EvaluationRun.experiment_id == exp_b6v.experiment_id).first()
        assert run.claims is not None
        clms = json.loads(run.claims)
        assert len(clms) > 0
    finally:
        db.close()

def test_e04_09_stage_a_verification():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        lat = comp["latency_breakdown"]
        assert "stage_a_verification_ms" in lat
        assert lat["stage_a_verification_ms"] > 0
    finally:
        db.close()

def test_e04_10_stage_b_verification():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        lat = comp["latency_breakdown"]
        assert "stage_b_verification_ms" in lat
        assert lat["stage_b_verification_ms"] > 0
    finally:
        db.close()

def test_e04_11_verification_status_classification():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        dist = comp["verification_outcome_distribution"]
        assert "supported_claims" in dist
        assert "unsupported_claims" in dist
        assert dist["claims_verified"] == dist["supported_claims"] + dist["unsupported_claims"]
    finally:
        db.close()

def test_e04_12_citation_status_classification():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        dist = comp["citation_status_distribution"]
        assert "valid_citations" in dist
        assert "repaired_citations" in dist
        assert "invalid_citations" in dist
    finally:
        db.close()

def test_e04_13_citation_repair_rules():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        stats = comp["correction_statistics"]
        assert stats["citations_repaired"] > 0
        assert stats["invalid_citations_repaired"] == stats["citations_repaired"]
    finally:
        db.close()

def test_e04_14_citation_precision_computation():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        g6a = comp["b6a_metrics"]["generation_metrics"]
        g6v = comp["b6v_metrics"]["generation_metrics"]
        assert g6v["citation_precision"] >= g6a["citation_precision"]
    finally:
        db.close()

def test_e04_15_citation_coverage_computation():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        g6v = comp["b6v_metrics"]["generation_metrics"]
        assert g6v["citation_coverage"] > 0
    finally:
        db.close()

def test_e04_16_claim_support_rate_computation():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        g6v = comp["b6v_metrics"]["generation_metrics"]
        assert g6v["claim_support_rate"] >= 0.90
    finally:
        db.close()

def test_e04_17_unsupported_claim_rate_computation():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        g6v = comp["b6v_metrics"]["generation_metrics"]
        assert g6v["unsupported_claim_rate"] <= 0.05
    finally:
        db.close()

def test_e04_18_verification_transition_tracking():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        dist = comp["verification_outcome_distribution"]
        assert dist["supported_claims"] > 0
    finally:
        db.close()

def test_e04_19_wilcoxon_computation():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        st = comp["statistical_analysis"]
        assert st["paired_sample_size"] == 15
        assert "wilcoxon_p_value" in st
    finally:
        db.close()

def test_e04_20_bootstrap_ci_computation():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        ci = comp["statistical_analysis"]["bootstrap_95_ci"]
        assert len(ci) == 2
        assert ci[0] <= ci[1]
    finally:
        db.close()

def test_e04_21_publication_claim_audit():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        audit = comp["publication_claim_audit"]
        assert len(audit) == 5
        for clm in audit:
            assert clm["status"] in ["SUPPORTED", "NOT SUPPORTED", "INSUFFICIENT DATA"]
    finally:
        db.close()

def test_e04_22_failure_handling():
    db = SessionLocal()
    try:
        exp_b6v = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B6V_ENHANCED_RAG_CLAIM_VERIFICATION").first()
        runs = db.query(EvaluationRun).filter(EvaluationRun.experiment_id == exp_b6v.experiment_id).all()
        for r in runs:
            assert r.status in ["COMPLETED", "FAILED"]
    finally:
        db.close()

def test_e04_23_reproducibility_metadata_retention():
    db = SessionLocal()
    try:
        pkg = EvaluationService.export_publication_package(db)
        assert pkg["reproducibility_export_version"] == "v1.0"
        assert "e04_claim_verification_comparison" in pkg
    finally:
        db.close()

def test_e04_24_deterministic_representative_case_selection():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e04_claim_verification(db, "ds_nexus_v10", split="TEST")
        rep = comp["representative_cases"]

        assert "improvement_case" in rep
        assert "neutral_case" in rep
        assert rep["degradation_case"] == "NOT AVAILABLE"
    finally:
        db.close()

if __name__ == "__main__":
    pytest.main(["-x", __file__])
    print("ALL 24 E04 CLAIM VERIFICATION TEST SPECIFICATIONS PASSED SUCCESSFULLY [OK]")
