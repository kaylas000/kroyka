"""B02 - Dimension Validator: проверяет что w,h,qty > 0 и w,h <= max sheet"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

MAX_W = 3660.0
MAX_H = 2070.0
MIN_DIM = 1.0

def run(state: PipelineState) -> PipelineState:
    errors = list(state.errors)
    warnings = list(state.warnings)
    for p in state.raw_parts:
        if p.w < MIN_DIM or p.h < MIN_DIM:
            errors.append(f'B02: {p.name} dimension too small ({p.w}x{p.h})')
        if p.w > MAX_W or p.h > MAX_H:
            warnings.append(f'B02: {p.name} ({p.w}x{p.h}) exceeds max sheet - will try rotated')
        if p.qty <= 0:
            errors.append(f'B02: {p.name} qty={p.qty} must be > 0')
    return state.model_copy(update={'errors': errors, 'warnings': warnings})
