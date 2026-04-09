"""C03 - Censor for b03_dedup"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b03_dedup."""
    field = 'deduped_parts'
    if field not in state:
        raise ValueError(f"Censor C03: missing '{field}' in pipeline state")
    # dedup: qty must be >= 1
    for p in data:
        assert int(p.get("qty", 0)) >= 1, f"qty < 1 in {p}"
    return state

if __name__ == '__main__':
    print('Censor C03 (b03_dedup) OK')
