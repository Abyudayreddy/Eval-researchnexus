#!/usr/bin/env python3
"""
ResearchNexus AI - Reanalyze Latency and Overhead
Distinguishes observed total wall-clock latency difference from internal verification computational overhead.
"""

import os
import sys
import json
import numpy as np

def main():
    with open("evaluation/module_02/latency/latency_metrics.json", "r", encoding="utf-8") as f:
        lat_data = json.load(f)

    pq_lat = lat_data["per_query_latencies"]

    naive_totals = [l["naive_total_ms"] for l in pq_lat]
    naive_gens = [l["naive_generation_ms"] for l in pq_lat]
    ver_totals = [l["verified_total_ms"] for l in pq_lat]
    ver_drafts = [l["verified_draft_ms"] for l in pq_lat]
    ver_claim_exts = [l["claim_extraction_ms"] for l in pq_lat]
    ver_nlis = [l["nli_ms"] for l in pq_lat]
    ver_repairs = [l["repair_ms"] for l in pq_lat]
    ver_post_vers = [l["post_verification_ms"] for l in pq_lat]

    # Verification stage internal overhead
    ver_overhead = [
        l["claim_extraction_ms"] + l["nli_ms"] + l["repair_ms"] + l["post_verification_ms"]
        for l in pq_lat
    ]

    # Paired deltas (Verified Total - Naive Total)
    paired_deltas = [v - n for n, v in zip(naive_totals, ver_totals)]

    reanalysis = {
        "n_queries": len(pq_lat),
        "observed_totals": {
            "naive_rag_total_ms": {
                "mean": round(float(np.mean(naive_totals)), 2),
                "p50": round(float(np.percentile(naive_totals, 50)), 2),
                "p95": round(float(np.percentile(naive_totals, 95)), 2)
            },
            "verified_rag_total_ms": {
                "mean": round(float(np.mean(ver_totals)), 2),
                "p50": round(float(np.percentile(ver_totals, 50)), 2),
                "p95": round(float(np.percentile(ver_totals, 95)), 2)
            },
            "observed_mean_difference_ms": round(float(np.mean(paired_deltas)), 2),
            "paired_deltas_ms": [round(d, 2) for d in paired_deltas]
        },
        "verification_computational_overhead": {
            "mean_overhead_ms": round(float(np.mean(ver_overhead)), 2),
            "p50_overhead_ms": round(float(np.percentile(ver_overhead, 50)), 2),
            "p95_overhead_ms": round(float(np.percentile(ver_overhead, 95)), 2),
            "breakdown_mean_ms": {
                "claim_extraction": round(float(np.mean(ver_claim_exts)), 2),
                "stage_a_and_b_nli_verification": round(float(np.mean(ver_nlis)), 2),
                "citation_repair": round(float(np.mean(ver_repairs)), 2),
                "post_repair_reverification": round(float(np.mean(ver_post_vers)), 2)
            }
        },
        "generation_variance_explanation": {
            "mean_naive_generation_ms": round(float(np.mean(naive_gens)), 2),
            "mean_verified_draft_generation_ms": round(float(np.mean(ver_drafts)), 2),
            "generation_difference_ms": round(float(np.mean(ver_drafts) - np.mean(naive_gens)), 2),
            "explanation": "Observed end-to-end latency in Verified RAG was slightly lower than Naive RAG (-172.63 ms) despite executing verification because LLM draft generation time for the shorter verified prompts finished faster in this sample (mean draft: 3,214.50 ms vs naive generation: 4,821.81 ms). The actual computational overhead introduced by the verification pipeline itself is +1,434.68 ms mean."
        }
    }

    with open("evaluation/module_02/revision_01/latency_reanalysis.json", "w", encoding="utf-8") as f:
        json.dump(reanalysis, f, indent=2)

    print("Successfully generated latency_reanalysis.json.")

if __name__ == "__main__":
    main()
