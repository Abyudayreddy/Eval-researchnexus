import sys
import os
import json

sys.path.insert(0, os.path.abspath('backend'))
from app.services.assistant.claim_verifier import ClaimVerifier, ClaimObject

verifier = ClaimVerifier()

# Test 1: Numerical mismatch test
c_num = ClaimObject(
    claim_id="c01",
    text="The model achieved an accuracy of 94.5% on ImageNet.",
    claim_type="numerical",
    evidence_ids=["ev01"]
)
ev_map_mismatch = {
    "ev01": {"evidence_text": "The model achieved an accuracy of 82.1% on ImageNet benchmark."}
}
status_num, reason_num = verifier._stage_a_deterministic_check(c_num, ev_map_mismatch)
print("Numerical Mismatch Test:", status_num, "| Reason:", reason_num)

# Test 2: Numerical match test
ev_map_match = {
    "ev01": {"evidence_text": "The model achieved an accuracy of 94.5% on ImageNet benchmark."}
}
status_match, reason_match = verifier._stage_a_deterministic_check(c_num, ev_map_match)
print("Numerical Match Test:", status_match, "| Reason:", reason_match)

# Test 3: Missing evidence
c_missing = ClaimObject(
    claim_id="c02",
    text="Transformers are self-attention architectures.",
    claim_type="conceptual",
    evidence_ids=["ev_nonexistent"]
)
status_miss, reason_miss = verifier._stage_a_deterministic_check(c_missing, {})
print("Missing Evidence Test:", status_miss, "| Reason:", reason_miss)
