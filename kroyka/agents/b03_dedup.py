"""B03 - Deduplicator: сливает одинаковые детали суммированием qty"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState, RawPart
from typing import List, Dict, Tuple

def _key(p: RawPart) -> Tuple:
    return (p.name, p.w, p.h, p.material, p.grain,
            p.edge_top, p.edge_bottom, p.edge_left, p.edge_right)

def run(state: PipelineState) -> PipelineState:
    seen: Dict[Tuple, RawPart] = {}
    for p in state.raw_parts:
        k = _key(p)
        if k in seen:
            old = seen[k]
            seen[k] = old.model_copy(update={'qty': old.qty + p.qty})
        else:
            seen[k] = p
    merged = list(seen.values())
    warnings = list(state.warnings)
    n_merged = len(state.raw_parts) - len(merged)
    if n_merged > 0:
        warnings.append(f'B03: merged {n_merged} duplicate part rows')
    return state.model_copy(update={'raw_parts': merged, 'warnings': warnings})
