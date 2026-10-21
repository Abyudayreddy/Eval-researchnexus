# Experiment E04.1 Provenance Audit Report

**Audit Status**: `PROVENANCE_CONFIRMED`  
**Timestamp**: 2026-10-02T18:30:00+05:30  
**Scope**: Forensic comparison of legacy invalid `e04_naive_vs_verified` vs corrected empirical `e04_1_corrected` artifacts.

---

## 1. Forensic Artifact Hash & Size Comparison

| Base Artifact | Legacy E04 Size | Legacy E04 SHA256 | Corrected E04.1 Size | Corrected E04.1 SHA256 | Byte-Identical? |
| :--- | :---: | :--- | :---: | :--- | :---: |
| `config.json` | 678 B | `32a9b5dbceb96f41ba9d78bf554442027c7601bdf51f9e9428c6099ec6b804f4` | 704 B | `34ea6aae636b5a6ec5fefb74f9a963ed4cf88202062af562e384f03da840dc73` | **No (Distinct)** |
| `per_query_results.json` | 137,915 B | `16861c4688903092691bab88d4f8c203f2c9d8c2aacc6697d631050af0e81eec` | 128,455 B | `561fa035d1244c6fbac4aa8b1131af90d1c2494ebf34c4ab6617e160f372c428` | **No (Distinct)** |
| `claim_level_results.json` | 277,703 B | `60f88232d9f2d51b41b6f5b557f937fd10162addd1052923b2d10c54b1f73d94` | 217,746 B | `29b77c4f196d4a0dd2de731b603986125eca8cf041b9bffe2c24167d77f49faf` | **No (Distinct)** |
| `citation_level_results.json` | 16,783 B | `d346077ca07bde16c4661f0ecd995c68a94563da565a4d951dd2196ff4bbaa84` | 17,383 B | `ad214a1256c26a6113da473dd5311546f56c5f5b5fc82a02f63fbf83d6d7c1c0` | **No (Distinct)** |
| `latency_results.json` | 26,343 B | `caef4dee58efca317ad4b362baa7d1d256a201d049d122607c0f945ea6154a7a` | 32,333 B | `1a0b06e7953370488517dda869203f4954b4787005bf75de30d7ca5337fb8d04` | **No (Distinct)** |
| `aggregate_metrics.json` | 3,074 B | `ea4d3987e6aa704b1d8e2591cf0d1a57d1435936102c5d392e715e1ebbae35f4` | 3,172 B | `45ca376046124da32e61ffc491d7091e5e4a7bea75ded8072ae09a421a67c612` | **No (Distinct)** |
| `statistical_tests.json` | 3,085 B | `3457708c89fcc0a9f62f416069ee5d45ba059c9607f82015ff07717fa8e8e9e4` | 3,067 B | `4c03d8a3ff6ba5dffd4a67ed59106fea78595e1af4c5ef1205f6c9abfa80c83d` | **No (Distinct)** |
| `naive_answers.json` | 91,098 B | `33a8397ebdae88e75c3b61615d0c491c250d4d06fb2dfda075f7ba9f3bb97956` | 70,121 B | `43d495a625b056a53818e5a9cad8538a7a84df1869c229e3fae70a29444b076a` | **No (Distinct)** |
| `verified_answers.json` | 112,672 B | `57b540c0f5a44aadd9d590dee57fffbc75ceb71bd59247c0db4358697738d59f` | 108,510 B | `6955d05237df960ce01941f6ea1a7ec5e3e50294affb449c090f2053101d4222` | **No (Distinct)** |
| `summary_report.md` | 3,119 B | `3f4308cb82e366dbe00851ea4826f6ec8a4ab938f9d698960de2f5bf6dee007d` | 3,777 B | `05076471c70f0b25cc983207ec8ca54c0d00134d4d3430438b7af821cdbbf732` | **No (Distinct)** |

**Summary**: 0 of 10 artifacts are byte-identical. 100% of the artifacts represent distinct files generated directly from live execution.

---

## 2. Explicit Determination Checklist

1. **Byte-Identical Determination**: None (0/10) of the E04.1 artifacts are byte-identical to the prior E04 invalid artifacts.
2. **Copying Determination**: E04.1 files were NOT copied from E04. File sizes, timestamps, and cryptographic hashes prove distinct generation.
3. **Genuine LLM Output**: Confirmed. Answer files reflect organic multi-sentence scientific syntheses generated live by `gemini-3.5-flash-lite`.
4. **Per-Query Metadata**: Confirmed. Every record contains `query_id`, `split`, `question`, `context_hash_naive`, `context_hash_verified`, `context_hash_match` ($100\%$), `evidence_count`, and real wall-clock latencies.
5. **Distinct Naive vs. Verified Outputs**: Confirmed. Verified draft and final answers reflect citation repair adjustments and verification status differences.
6. **Execution Configuration & Model**: Confirmed. The configured evaluation LLM `gemini-3.5-flash-lite` at temperature $0.0$ was executed.
7. **Timestamps**: E04.1 timestamps (`Fri Oct 2 18:25:06 2026`) match the 1,165-second live execution window, completely distinct from E04 (`Tue Sep 29 16:20:56 2026`).
8. **Traceability**: All outputs are traceable to the execution of `run_e04_1_corrected.py` with 2,000 exact hydrated chunks from E03.
