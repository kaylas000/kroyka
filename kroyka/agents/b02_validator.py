from kroyka.models import PipelineState
from typing import List, Dict, Any

MIN_DIM = 1
MAX_DIM = 10000

def validate_part(part: Dict[str, Any]) -> List[str]:
    errs = []
    if not part.get('name'):
        errs.append('Missing or empty name')
    if not (MIN_DIM <= int(part.get('length', 0)) <= MAX_DIM):
        errs.append(f"length={part.get('length')} out of range")
    if not (MIN_DIM <= int(part.get('width', 0)) <= MAX_DIM):
        errs.append(f"width={part.get('width')} out of range")
    if not (1 <= int(part.get('qty', 0)) <= 10000):
        errs.append(f"qty={part.get('qty')} out of range")
    if not part.get('material'):
        errs.append('Missing material')
    return errs

def run(state: PipelineState) -> PipelineState:
    errors = list(state.errors or [])
    valid = True
    for part in (state.raw_parts or []):
        p = part.dict() if hasattr(part, 'dict') else dict(part)
        errs = validate_part(p)
        if errs:
            valid = False
            for e in errs:
                errors.append(f"{p.get('name', '?')}: {e}")
    state.validated = valid
    state.errors = errors
    return state

if __name__ == '__main__':
    s = PipelineState(raw_parts=[{
        'name': 'Door', 'length': 800, 'width': 400,
        'qty': 2, 'material': 'LDSP', 'w': 1220, 'h': 2440
    }])
    print('b02 ok:', run(s).validated)
