from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class GrainDir(str, Enum):
    ALONG = "along"
    ACROSS = "across"
    ANY = "any"

class RawPart(BaseModel):
    name: str
    qty: int
    w: float  # mm
    h: float  # mm
    material: str
    grain: GrainDir = GrainDir.ANY
    edge_top: float = 0.0
    edge_bottom: float = 0.0
    edge_left: float = 0.0
    edge_right: float = 0.0
    label: str = ""

class Sheet(BaseModel):
    material: str
    w: float
    h: float
    qty: int
    cost_per_sheet: float = 0.0

class PlacedPart(BaseModel):
    part_name: str
    sheet_idx: int
    x: float
    y: float
    w: float
    h: float
    rotated: bool = False
    label: str = ""

class CutPlan(BaseModel):
    sheets_used: int
    efficiency: float  # 0..1
    placements: List[PlacedPart] = []
    unplaced: List[str] = []
    svg_paths: List[str] = []
    cnc_paths: List[str] = []
    warnings: List[str] = []

class PipelineState(BaseModel):
    order_csv: str = ""
    raw_parts: List[RawPart] = []
    sheets: List[Sheet] = []
    validated: bool = False
    plan: Optional[CutPlan] = None
    errors: List[str] = []
    warnings: List[str] = []
