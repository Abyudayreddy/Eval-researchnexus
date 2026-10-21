import sys
import os
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

os.environ["DATABASE_URL"] = "sqlite:///./test_eval_e05.db"
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

def test_e05_01_same_benchmark():
    db = SessionLocal()
    try:
        ds = db.query(EvaluationDataset).filter(EvaluationDataset.dataset_id == "ds_nexus_v10").first()
        assert ds is not None
        assert ds.version == "v1.0"
        assert ds.item_count == 100
    finally:
        db.close()

def test_e05_02_same_test_items():
    db = SessionLocal()
    try:
        test_items = db.query(EvaluationItem).filter(EvaluationItem.dataset_id == "ds_nexus_v10", EvaluationItem.split == "TEST").all()
        assert len(test_items) == 15
        for it in test_items:
            assert it.gold_verified == "TRUE"
    finally:
        db.close()

def test_e05_03_same_canonical_b4_evidence():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        assert comp["hard_gate_audit"]["status"] == "PASSED"
    finally:
        db.close()

def test_e05_04_same_gemini_generation_config():
    db = SessionLocal()
    try:
        exp_b7a = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B7A_ENHANCED_RAG_VERIFIED_SINGLE_PASS").first()
        exp_b7r = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B7R_ENHANCED_RAG_ITERATIVE_REFINEMENT").first()

        cfg_b7a = json.loads(exp_b7a.configuration_json)
        cfg_b7r = json.loads(exp_b7r.configuration_json)

        assert cfg_b7a["generation_model"] == "gemini-2.5-flash"
        assert cfg_b7r["generation_model"] == "gemini-2.5-flash"
        assert cfg_b7a["temperature"] == cfg_b7r["temperature"] == 0.0
        assert cfg_b7a["max_output_tokens"] == cfg_b7r["max_output_tokens"] == 1024
    finally:
        db.close()

def test_e05_05_single_initial_b5e_generation_lock():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        assert comp["hard_gate_audit"]["status"] == "PASSED"
    finally:
        db.close()

def test_e05_06_b7a_baseline_definition():
    db = SessionLocal()
    try:
        exp_b7a = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B7A_ENHANCED_RAG_VERIFIED_SINGLE_PASS").first()
        assert exp_b7a is not None
        assert exp_b7a.baseline_id == "B7A_ENHANCED_RAG_VERIFIED_SINGLE_PASS"
    finally:
        db.close()

def test_e05_07_b7r_baseline_definition():
    db = SessionLocal()
    try:
        exp_b7r = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B7R_ENHANCED_RAG_ITERATIVE_REFINEMENT").first()
        assert exp_b7r is not None
        assert exp_b7r.baseline_id == "B7R_ENHANCED_RAG_ITERATIVE_REFINEMENT"
    finally:
        db.close()

def test_e05_08_phase_3_4_verification_lock():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        assert comp["hard_gate_audit"]["status"] == "PASSED"
    finally:
        db.close()

def test_e05_09_max_refinement_cycles_lock():
    db = SessionLocal()
    try:
        exp_b7r = db.query(EvaluationExperiment).filter(EvaluationExperiment.baseline_id == "B7R_ENHANCED_RAG_ITERATIVE_REFINEMENT").first()
        cfg_b7r = json.loads(exp_b7r.configuration_json)
        assert cfg_b7r["max_refinement_cycles"] == 2
    finally:
        db.close()

def test_e05_10_primary_generation_metrics():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        for key in ["citation_precision", "citation_coverage", "claim_support_rate", "unsupported_claim_rate", "evidence_coverage"]:
            assert key in comp["b7a_metrics"]["generation_metrics"]
            assert key in comp["b7r_metrics"]["generation_metrics"]
    finally:
        db.close()

def test_e05_11_initial_vs_final_b7r():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        init_final = comp["initial_vs_final_b7r"]
        assert "initial_citation_precision" in init_final
        assert "final_citation_precision" in init_final
        assert "citation_precision_gain" in init_final
        assert "unsupported_claim_reduction" in init_final
    finally:
        db.close()

def test_e05_12_cycle_level_metrics():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        cycle_m = comp["cycle_metrics"]
        assert len(cycle_m) == 3
        assert cycle_m[0]["version"] == "v1_initial"
        assert cycle_m[1]["version"] == "v2_cycle1"
        assert cycle_m[2]["version"] == "v3_cycle2"
    finally:
        db.close()

def test_e05_13_refinement_outcome_distribution():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        outcomes = comp["refinement_outcomes"]
        assert outcomes["total_items"] == 15
        assert outcomes["improved_count"] + outcomes["no_change_count"] + outcomes["degraded_count"] == 15
        assert outcomes["success_rate"] == 0.667
    finally:
        db.close()

def test_e05_14_self_feedback_category_distribution():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        fb_dist = comp["feedback_category_distribution"]
        assert "MISSING_EVIDENCE" in fb_dist
        assert "NO_REFINEMENT_NEEDED" in fb_dist
        assert sum(fb_dist.values()) == 15
    finally:
        db.close()

def test_e05_15_transition_matrix():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        trans = comp["transition_matrix"]
        assert "v1_to_v2" in trans
        assert "v2_to_v3" in trans
        assert trans["v1_to_v2"]["improved"] + trans["v1_to_v2"]["neutral"] + trans["v1_to_v2"]["degraded"] == 15
    finally:
        db.close()

def test_e05_16_latency_breakdown():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        lat = comp["latency_breakdown"]
        assert "feedback_generation_ms" in lat
        assert "refinement_generation_ms" in lat
        assert "b7r_overhead_p50_ms" in lat
        assert lat["b7r_overhead_p50_ms"] > 0
    finally:
        db.close()

def test_e05_17_model_calls_breakdown():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        calls = comp["model_calls_breakdown"]
        assert calls["b7a_calls"] == 3
        assert calls["b7r_calls"] == 5
        assert calls["refinement_calls"] == 2
    finally:
        db.close()

def test_e05_18_efficiency_indicators():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        eff = comp["efficiency_indicators"]
        assert "citation_precision_gain_per_call" in eff
        assert "claim_support_gain_per_call" in eff
        assert "unsupported_rate_reduction_per_call" in eff
    finally:
        db.close()

def test_e05_19_error_category_distribution():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        err_dist = comp["error_distribution"]
        assert isinstance(err_dist, list)
        types = [e["error_type"] for e in err_dist]
        assert "REFINEMENT_UNNECESSARY" in types
        assert "REFINEMENT_FAILED" in types
    finally:
        db.close()

def test_e05_20_wilcoxon_and_bootstrap_ci():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        stat = comp["statistical_analysis"]
        assert stat["paired_sample_size"] == 15
        assert "wilcoxon_p_value" in stat
        assert len(stat["bootstrap_95_ci"]) == 2
        assert "Sample size N=15" in stat["sample_size_warning"]
    finally:
        db.close()

def test_e05_21_representative_cases():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        rep = comp["representative_cases"]
        assert rep["improvement_case"] != "NOT AVAILABLE"
        assert rep["neutral_case"] != "NOT AVAILABLE"
        assert rep["degradation_case"] == "NOT AVAILABLE"
    finally:
        db.close()

def test_e05_22_human_evaluation_not_measured():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        assert comp["human_evaluation"] == "NOT MEASURED"
    finally:
        db.close()

def test_e05_23_publication_claim_audit():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        claims = comp["publication_claim_audit"]
        assert len(claims) == 5
        claim_ids = [c["claim_id"] for c in claims]
        assert "clm_e05_a" in claim_ids
        assert "clm_e05_d" in claim_ids
    finally:
        db.close()

def test_e05_24_scoped_conclusion_status():
    db = SessionLocal()
    try:
        comp = EvaluationService.compare_e05_iterative_refinement(db, "ds_nexus_v10", split="TEST")
        allowed = [
            "IMPROVEMENT OBSERVED",
            "NO MATERIAL DIFFERENCE",
            "PERFORMANCE DEGRADATION",
            "QUALITY IMPROVEMENT WITH LATENCY TRADEOFF",
            "INSUFFICIENT DATA"
        ]
        assert comp["conclusion_status"] in allowed
        assert comp["conclusion_status"] == "QUALITY IMPROVEMENT WITH LATENCY TRADEOFF"
    finally:
        db.close()
