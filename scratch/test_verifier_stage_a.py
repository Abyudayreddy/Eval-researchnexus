import sys
import os
import json

sys.path.insert(0, os.path.abspath('backend'))
from app.services.assistant.claim_verifier import ClaimVerifier

verifier = ClaimVerifier()

# Test 1: Stage A deterministic check with high overlap
claim_high = "Deep neural networks require large labeled datasets for supervised training."
evidence_high = "Deep neural networks require large labeled datasets for supervised training and optimization."
res_high = verifier._stage_a_deterministic_check(claim_high, evidence_high)

# Test 2: Stage A deterministic check with low overlap
claim_low = "Quantum computing uses qubits and entanglement."
evidence_low = "Decision trees partition tabular records using information gain."
res_low = verifier._stage_a_deterministic_check(claim_low, evidence_low)

print("Stage A High Overlap Result:", res_high)
print("Stage A Low Overlap Result:", res_low)
