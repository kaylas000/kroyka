"""B04 - Sorter: сортирует детали по убывающей площади (First Fit Decreasing)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    sorted_parts = sorted(state.raw_parts,
                          key=lambda p: p.w * p.h * p.qty,
                          reverse=True)
    return state.model_copy(update={'raw_parts': sorted_parts})
