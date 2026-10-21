import os
import docx

doc_name = 'SRS_V1_ (2).docx'
full_path = os.path.abspath(os.path.join('SDC Review 1', doc_name))

print("Opening:", full_path)
doc = docx.Document(full_path)
table = doc.tables[0]
print(f"Current rows: {len(table.rows)}")

new_entries = [
    ("1.0", "02-Aug-2026", "Project Team", "Initial IEEE SRS Draft"),
    ("2.0", "14-Aug-2026", "Project Team", "First review Draft - Hybrid Retrieval"),
    ("3.0", "25-Aug-2026", "Project Team", "Core - Enhanced RAG + XAI"),
    ("3.1", "01-Sep-2026", "Project Team", "Phase 3.4 Claim Verification & NLI Fact-Checking"),
    ("3.2", "15-Sep-2026", "Project Team", "Iterative Refinement Loop & Auto-Repair Subsystem"),
    ("4.0", "22-Sep-2026", "Project Team", "Multi-Paper Matrix Synthesizer & Personal Corpus Vault"),
    ("4.1", "29-Sep-2026", "Project Team", "LaTeX Manuscript Export, System Benchmarks & Final Review Release"),
]

while len(table.rows) > 1:
    tr = table.rows[-1]._tr
    tr.getparent().remove(tr)

for ver, dt, auth, desc in new_entries:
    row = table.add_row()
    row.cells[0].text = ver
    row.cells[1].text = dt
    row.cells[2].text = auth
    row.cells[3].text = desc

doc.save(full_path)
print("Updated Revision History successfully!")
