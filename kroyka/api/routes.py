from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid, datetime, sys, os

router = APIRouter(prefix="/api/v1", tags=["kroyka"])
_jobs: Dict[str, Dict] = {}

class PartIn(BaseModel):
    name: str
    length: float = Field(..., gt=0, le=10000)
    width: float = Field(..., gt=0, le=10000)
    qty: int = Field(1, ge=1, le=10000)
    material: str = "LDSP 16mm"
    grain: bool = False
    edge_top: float = 0
    edge_bottom: float = 0
    edge_left: float = 0
    edge_right: float = 0

class CutRequest(BaseModel):
    parts: List[PartIn]
    kerf: float = Field(3.2, ge=0, le=20)
    cnc_type: Optional[str] = "holzma"

class JobStatus(BaseModel):
    job_id: str
    status: str
    created_at: str
    result: Optional[Dict[str, Any]] = None
    errors: Optional[List[Dict]] = None

def _run_pipeline(job_id: str, request: CutRequest):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    try:
        from kroyka.orchestrator import run_pipeline
        from kroyka.models import PipelineState
        state = PipelineState(
            raw_parts=[p.dict() for p in request.parts],
            kerf=request.kerf,
            cnc_type=request.cnc_type or 'holzma',
        )
        result = run_pipeline(state)
        _jobs[job_id]['status'] = 'done'
        _jobs[job_id]['result'] = dict(result)
    except Exception as e:
        _jobs[job_id]['status'] = 'error'
        _jobs[job_id]['errors'] = [{'error': str(e)}]

@router.post("/cut", response_model=JobStatus, status_code=202)
async def create_cut_job(request: CutRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    _jobs[job_id] = {'job_id': job_id, 'status': 'pending',
        'created_at': datetime.datetime.utcnow().isoformat(), 'result': None, 'errors': None}
    background_tasks.add_task(_run_pipeline, job_id, request)
    return _jobs[job_id]

@router.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job(job_id: str):
    if job_id not in _jobs:
        raise HTTPException(404, detail=f"Job {job_id} not found")
    return _jobs[job_id]

@router.get("/jobs", response_model=List[JobStatus])
async def list_jobs():
    return list(_jobs.values())

@router.get("/health")
async def health():
    return {"status": "ok", "service": "kroyka"}
