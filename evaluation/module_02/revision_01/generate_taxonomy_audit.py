#!/usr/bin/env python3
"""
ResearchNexus AI - Full 56-Claim Taxonomy Audit
Produces taxonomy_audit_56_claims.json auditing each of the 56 extracted claims.
Identifies compound statements that contain both factual assertions and negative findings.
"""

import os
import sys
import json

def audit_claim(c, idx):
    txt = c["claim_text"].strip()
    status = c["support_status"]
    cits = c.get("citation_ids", [])
    ev_ids = c.get("evidence_ids", [])
    lower = txt.lower()

    # Detect components
    has_explicit_refusal = (
        "therefore, i cannot answer" in lower or
        "therefore, you cannot answer" in lower or
        "cannot answer this query" in lower or
        "cannot answer the query" in lower or
        "cannot answer the research query" in lower or
        "so i cannot answer" in lower
    )
    
    has_negative_finding = (
        "there is no mention of" in lower or
        "does not contain any information or metrics regarding" in lower or
        "do not contain any information or metrics regarding" in lower or
        "does not contain any claims regarding" in lower or
        "do not contain any claims regarding" in lower or
        "retrieved documents do not contain any claims regarding" in lower or
        "the documents do not mention" in lower or
        "not contain information regarding a 92.4% precision@5" in lower
    )

    has_positive_factual = (
        "face scaling challenges" in lower or
        "formulate a novel loss function" in lower or
        "formulates a novel loss function" in lower or
        "formulates novel loss functions" in lower or
        "introduce a \"novel loss function" in lower or
        "combining contrastive optimization" in lower
    )

    # Classification logic
    if has_positive_factual and has_negative_finding:
        # Compound statement (e.g. index 17 and 20: "While the evidence notes that... it does not contain...")
        epistemic_type = "COMPOUND_FACTUAL_AND_NEGATIVE_FINDING"
        is_factual = True
        is_abstention = False
        is_negative = True
        is_non_factual = False
        reason = "Compound sentence: contains an affirmative factual proposition regarding methodology in evidence AND a negative finding regarding the absence of the queried metric."
    elif has_positive_factual:
        epistemic_type = "SUPPORTED_FACTUAL_CLAIM"
        is_factual = True
        is_abstention = False
        is_negative = False
        is_non_factual = False
        reason = "Affirmative factual proposition reporting background methodology substantiated by retrieved literature."
    elif has_explicit_refusal:
        epistemic_type = "APPROPRIATE_ABSTENTION"
        is_factual = False
        is_abstention = True
        is_negative = False
        is_non_factual = False
        reason = "Explicit epistemic refusal to answer an unanswerable query where evidence lacks required data."
    elif has_negative_finding:
        epistemic_type = "INSUFFICIENT_EVIDENCE_FINDING"
        is_factual = False
        is_abstention = False
        is_negative = True
        is_non_factual = False
        reason = "Evidence-bounded meta-statement documenting the absence of queried metric or concept."
    else:
        epistemic_type = "NON_FACTUAL_STATEMENT"
        is_factual = False
        is_abstention = False
        is_negative = False
        is_non_factual = True
        reason = "Conversational or structural text without empirical assertion."

    return {
        "claim_index": idx,
        "claim_id": c["claim_id"],
        "query_id": c["query_id"],
        "system": c["system"],
        "claim_text": txt,
        "original_support_status": status,
        "corrected_epistemic_type": epistemic_type,
        "is_factual_assertion": is_factual,
        "is_abstention": is_abstention,
        "is_negative_finding": is_negative,
        "is_non_factual": is_non_factual,
        "supporting_evidence_ids": ev_ids,
        "citation_ids": cits,
        "classification_reason": reason
    }

def main():
    with open("evaluation/module_02/raw/claims_raw.json", "r", encoding="utf-8") as f:
        claims = json.load(f)

    audited = []
    for idx, c in enumerate(claims, 1):
        audited.append(audit_claim(c, idx))

    out_file = "evaluation/module_02/revision_01/taxonomy_audit_56_claims.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(audited, f, indent=2)

    print(f"Audited {len(audited)} claims saved to {out_file}.")
    
    # Summary
    type_counts = {}
    for a in audited:
        k = f"{a['system']} | {a['corrected_epistemic_type']}"
        type_counts[k] = type_counts.get(k, 0) + 1
    print("\nTaxonomy Audit Breakdown:")
    for k, v in sorted(type_counts.items()):
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
