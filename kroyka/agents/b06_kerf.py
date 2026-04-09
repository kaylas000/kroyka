"""B06 - Kerf Calculator: прибавляет припуск пилы к размерам деталей"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState, RawPart

DEFAULT_KERF = 4.0  # mm

def run(state: PipelineState, kerf: float = DEFAULT_KERF) -> PipelineState:
    expanded = []
    for p in state.raw_parts:
        expanded.append(p.model_copy(update={
            'w': p.w + kerf,
            'h': p.h + kerf,
        }))
    return state.model_copy(update={'raw_parts': expanded})
