from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.evaluation_service import EvaluationService
from app.models.evaluation import EvaluationDataset, EvaluationItem, EvaluationExperiment, EvaluationRun, HumanEvaluationTask

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CreateDatasetRequest(BaseModel):
    name: str
    domain: str = "AI"
    version: str = "v1.0"
    description: Optional[str] = None

class AddItemRequest(BaseModel):
    question: str
    question_type: str = "SINGLE_PAPER"
    split: str = "DEVELOPMENT"
    domain: str = "AI"
    difficulty: str = "MEDIUM"
    expected_paper_ids: Optional[List[str]] = None
    expected_evidence_ids: Optional[List[str]] = None
    reference_answer: Optional[str] = None

class CreateExperimentRequest(BaseModel):
    name: str
    dataset_id: str
    baseline_id: str = "B5_ENHANCED_RAG"
    configuration: Optional[Dict[str, Any]] = None
    description: Optional[str] = None

class HumanEvalRequest(BaseModel):
    experiment_id: str
    item_id: str
    evaluator_id: str
    system_label: str = "System A"
    ratings: Dict[str, int]  # Correctness, Relevance, Groundedness, Citation Quality, Completeness, Usefulness, Clarity (1-5)
    comments: Optional[str] = None

@router.post("/datasets")
async def create_dataset(request: CreateDatasetRequest, db: Session = Depends(get_db)):
    ds = EvaluationService.create_dataset(
        db, name=request.name, domain=request.domain, version=request.version, description=request.description
    )
    return {"dataset_id": ds.dataset_id, "name": ds.name, "version": ds.version, "status": ds.status}

@router.get("/datasets")
async def list_datasets(db: Session = Depends(get_db)):
    datasets = db.query(EvaluationDataset).all()
    return [
        {
            "dataset_id": d.dataset_id,
            "name": d.name,
            "version": d.version,
            "domain": d.domain,
            "status": d.status,
            "item_count": d.item_count
        }
        for d in datasets
    ]

@router.post("/datasets/{dataset_id}/items")
async def add_item(dataset_id: str, request: AddItemRequest, db: Session = Depends(get_db)):
    try:
        item = EvaluationService.add_evaluation_item(
            db=db,
            dataset_id=dataset_id,
            question=request.question,
            question_type=request.question_type,
            split=request.split,
            domain=request.domain,
            difficulty=request.difficulty,
            expected_paper_ids=request.expected_paper_ids,
            expected_evidence_ids=request.expected_evidence_ids,
            reference_answer=request.reference_answer
        )
        return {"item_id": item.item_id, "dataset_id": item.dataset_id, "question": item.question}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/experiments")
async def create_experiment(request: CreateExperimentRequest, db: Session = Depends(get_db)):
    exp = EvaluationService.create_experiment(
        db=db,
        name=request.name,
        dataset_id=request.dataset_id,
        baseline_id=request.baseline_id,
        configuration=request.configuration,
        description=request.description
    )
    return {"experiment_id": exp.experiment_id, "name": exp.name, "status": exp.status, "baseline_id": exp.baseline_id}

@router.get("/experiments")
async def list_experiments(db: Session = Depends(get_db)):
    experiments = db.query(EvaluationExperiment).all()
    return [
        {
            "experiment_id": e.experiment_id,
            "name": e.name,
            "baseline_id": e.baseline_id,
            "status": e.status,
            "created_at": e.created_at.isoformat() if e.created_at else None
        }
        for e in experiments
    ]

@router.post("/experiments/{experiment_id}/run")
async def run_experiment(experiment_id: str, db: Session = Depends(get_db)):
    try:
        return EvaluationService.run_experiment(db, experiment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/experiments/{experiment_id}/results")
async def get_results(experiment_id: str, db: Session = Depends(get_db)):
    return EvaluationService.compute_experiment_metrics(db, experiment_id)

@router.get("/experiments/{dataset_id}/ablation")
async def get_ablation(dataset_id: str, db: Session = Depends(get_db)):
    return EvaluationService.run_ablation_study(db, dataset_id)

@router.get("/experiments/{dataset_id}/rrf-sensitivity")
async def get_rrf_sensitivity(dataset_id: str, db: Session = Depends(get_db)):
    return EvaluationService.run_rrf_sensitivity_study(db, dataset_id)

@router.post("/human-eval")
async def submit_human_eval(request: HumanEvalRequest, db: Session = Depends(get_db)):
    import json
    task_id = f"heval_{uuid.uuid4().hex[:12]}"
    task = HumanEvaluationTask(
        task_id=task_id,
        experiment_id=request.experiment_id,
        item_id=request.item_id,
        evaluator_id=request.evaluator_id,
        system_label=request.system_label,
        ratings_json=json.dumps(request.ratings),
        comments=request.comments
    )
    db.add(task)
    db.commit()
    return {"task_id": task_id, "status": "RECORDED"}

@router.get("/claims/audit")
async def audit_claims(db: Session = Depends(get_db)):
    return EvaluationService.audit_publication_claims(db)

@router.get("/export/tables")
async def export_tables(db: Session = Depends(get_db)):
    return EvaluationService.export_publication_package(db)

@router.get("/export/reproducibility")
async def export_reproducibility(db: Session = Depends(get_db)):
    return EvaluationService.export_publication_package(db)
