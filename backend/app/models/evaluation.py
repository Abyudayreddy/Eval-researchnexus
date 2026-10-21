import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class EvaluationDataset(Base):
    __tablename__ = "evaluation_datasets"

    dataset_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False, default="v1.0")
    description = Column(Text, nullable=True)
    domain = Column(String, default="General Science")
    
    # Status: DRAFT | READY | RUNNING | ARCHIVED
    status = Column(String, default="DRAFT", index=True)
    item_count = Column(Integer, default=0)
    is_frozen = Column(String, default="FALSE") # "TRUE" | "FALSE"
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    created_by = Column(String, default="evaluator")

    items = relationship("EvaluationItem", back_populates="dataset", cascade="all, delete-orphan")
    experiments = relationship("EvaluationExperiment", back_populates="dataset", cascade="all, delete-orphan")

class EvaluationItem(Base):
    __tablename__ = "evaluation_items"

    item_id = Column(String, primary_key=True, index=True)
    dataset_id = Column(String, ForeignKey("evaluation_datasets.dataset_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Split: DEVELOPMENT | VALIDATION | TEST
    split = Column(String, default="DEVELOPMENT", index=True)
    
    question = Column(Text, nullable=False)
    # Type: SINGLE_PAPER | MULTI_PAPER | HYBRID | METHODOLOGY | RESULTS | COMPARISON | EVIDENCE | SYNTHESIS | UNANSWERABLE | ADVERSARIAL
    question_type = Column(String, nullable=False, index=True)
    domain = Column(String, default="AI")
    difficulty = Column(String, default="MEDIUM")
    
    # Gold Annotations (JSON string arrays)
    expected_paper_ids = Column(Text, nullable=True)
    expected_evidence_ids = Column(Text, nullable=True)
    reference_answer = Column(Text, nullable=True)
    gold_claims = Column(Text, nullable=True)
    
    gold_verified = Column(String, default="TRUE")  # "TRUE" | "FALSE"
    
    # Annotation origin: HUMAN_ANNOTATED | AI_ASSISTED | AUTOMATIC
    annotation_origin = Column(String, default="HUMAN_ANNOTATED")
    metadata_json = Column(Text, nullable=True)

    dataset = relationship("EvaluationDataset", back_populates="items")
    runs = relationship("EvaluationRun", back_populates="item", cascade="all, delete-orphan")

class EvaluationExperiment(Base):
    __tablename__ = "evaluation_experiments"

    experiment_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # Status: DRAFT | READY | RUNNING | COMPLETED | FAILED | ARCHIVED
    status = Column(String, default="DRAFT", index=True)
    dataset_id = Column(String, ForeignKey("evaluation_datasets.dataset_id"), nullable=False, index=True)
    
    # Baseline: B0_LLM_ONLY | B1_DENSE_RAG | B2_BM25_RAG | B3_HYBRID_RAG | B4_HYBRID_BGE | B5_ENHANCED_RAG | B6_ENHANCED_VERIFICATION | B7_ITERATIVE_RAG
    baseline_id = Column(String, nullable=False, index=True)
    
    # Immutable parameter configuration JSON
    configuration_json = Column(Text, nullable=False)
    
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    created_by = Column(String, default="researcher")

    dataset = relationship("EvaluationDataset", back_populates="experiments")
    runs = relationship("EvaluationRun", back_populates="experiment", cascade="all, delete-orphan")

class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    run_id = Column(String, primary_key=True, index=True)
    experiment_id = Column(String, ForeignKey("evaluation_experiments.experiment_id", ondelete="CASCADE"), nullable=False, index=True)
    item_id = Column(String, ForeignKey("evaluation_items.item_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Execution outputs (JSON strings)
    retrieved_papers = Column(Text, nullable=True)
    retrieved_evidence = Column(Text, nullable=True)
    generated_answer = Column(Text, nullable=True)
    claims = Column(Text, nullable=True)
    citations = Column(Text, nullable=True)
    verification_results = Column(Text, nullable=True)
    
    latencies_json = Column(Text, nullable=True)  # retrieval_ms, rrf_ms, bge_ms, generation_ms, total_ms
    model_calls_json = Column(Text, nullable=True)
    rerank_trace_json = Column(Text, nullable=True)  # pre_rerank_rank, post_rerank_rank, bge_score, rrf_score, candidate_counts
    
    # Status: COMPLETED | FAILED
    status = Column(String, default="COMPLETED", index=True)
    # Error Category: RETRIEVAL_MISS | RERANKING_ERROR | EVIDENCE_MISS | CITATION_ERROR | UNSUPPORTED_CLAIM | CONTEXT_LEAKAGE | GENERATION_ERROR | VERIFICATION_ERROR | ITERATION_ERROR | METADATA_ERROR
    error_category = Column(String, nullable=True, index=True)

    experiment = relationship("EvaluationExperiment", back_populates="runs")
    item = relationship("EvaluationItem", back_populates="runs")

class HumanEvaluationTask(Base):
    __tablename__ = "human_evaluation_tasks"

    task_id = Column(String, primary_key=True, index=True)
    experiment_id = Column(String, ForeignKey("evaluation_experiments.experiment_id", ondelete="CASCADE"), nullable=False, index=True)
    item_id = Column(String, ForeignKey("evaluation_items.item_id", ondelete="CASCADE"), nullable=False, index=True)
    evaluator_id = Column(String, nullable=False, index=True)
    
    # Blinded label: System A | System B | System C
    system_label = Column(String, default="System A")
    
    # Ratings 1-5 JSON dict: Correctness, Relevance, Groundedness, Citation Quality, Completeness, Usefulness, Clarity
    ratings_json = Column(Text, nullable=False)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PublicationClaim(Base):
    __tablename__ = "publication_claims"

    claim_id = Column(String, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    evidence_source = Column(Text, nullable=True)
    
    # Status: SUPPORTED | PARTIALLY_SUPPORTED | NOT_MEASURED | UNSUPPORTED
    status = Column(String, default="NOT_MEASURED", index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
