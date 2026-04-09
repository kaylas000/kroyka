"""B07 - Labeler: проставляет маркировку деталям если не задана"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    labeled = []
    counters = {}
    for p in state.raw_parts:
        if p.label:
            labeled.append(p)
            continue
        prefix = p.material[:3].upper()
        counters[prefix] = counters.get(prefix, 0) + 1
        label = f'{prefix}-{counters[prefix]:04d}'
        labeled.append(p.model_copy(update={'label': label}))
    return state.model_copy(update={'raw_parts': labeled})
