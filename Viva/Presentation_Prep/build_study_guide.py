"""
Master script to assemble the complete Study and Presentation Preparation Guide,
save the docx, and convert it to a publication-quality PDF via Word COM.
"""
import os
import sys
import docx
import win32com.client

# Add builder package to path
BUILDER_DIR = os.path.abspath("Viva/Presentation_Prep/builder")
sys.path.append(BUILDER_DIR)

from doc_helpers import setup_page
from section_story_stack import build_cover_and_intro
from section_modules_retrieval import build_modules_and_retrieval
from section_verification_xai import build_verification_and_xai
from section_compare_demo import build_comparison_demo_scripts
from section_code_eval import build_code_and_evaluation
from section_viva_defense import build_viva_and_defense

def main():
    print("="*60)
    print("BUILDING RESEARCHNEXUS AI PRESENTATION & STUDY GUIDE")
    print("="*60)

    doc = docx.Document()
    setup_page(doc)

    print("Step 1: Building Cover, Project Story, Problem Formulation, Tech Stack, and Pipeline Flow...")
    build_cover_and_intro(doc)

    print("Step 2: Building Product Modules, Retrieval Engine, Cross-Encoder, RAG, and Gap Analysis...")
    build_modules_and_retrieval(doc)

    print("Step 3: Building Document-Only Mode, Dynamic Ingestion, PROVE Engine, Citation Integrity, and XAI...")
    build_verification_and_xai(doc)

    print("Step 4: Building Multi-Paper Comparison, Literature Review, Scenario Banks, Live Demo Steps & Scripts...")
    build_comparison_demo_scripts(doc)

    print("Step 5: Building Codebase Walkthrough, Verified Evaluation Metrics, and Figures...")
    build_code_and_evaluation(doc)

    print("Step 6: Building 40+ Categorized Viva Q&A, Examiner Challenges, Limitations, Scripts & Final Advice...")
    build_viva_and_defense(doc)

    # Output paths
    output_docx = os.path.abspath("Viva/Presentation_Prep/ResearchNexus_AI_Presentation_Study_Guide.docx")
    output_pdf = os.path.abspath("Viva/Presentation_Prep/ResearchNexus_AI_Presentation_Study_Guide.pdf")

    print(f"Saving DOCX to: {output_docx}")
    doc.save(output_docx)
    print("DOCX saved successfully!")

    print("Converting DOCX to PDF using Word COM automation...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc_obj = word.Documents.Open(output_docx)
        doc_obj.SaveAs(output_pdf, FileFormat=17) # 17 is wdFormatPDF
        doc_obj.Close()
        print(f"PDF generated successfully at: {output_pdf}")
    except Exception as e:
        print(f"Error converting to PDF: {e}")
    finally:
        word.Quit()

    if os.path.exists(output_pdf):
        size_kb = os.path.getsize(output_pdf) / 1024
        print(f"SUCCESS: Output PDF verified! Size: {size_kb:.2f} KB")
    else:
        print("WARNING: PDF file was not generated.")

if __name__ == "__main__":
    main()
