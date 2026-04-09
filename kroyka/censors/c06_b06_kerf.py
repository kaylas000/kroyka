"""C06 - Censor for b06_kerf"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b06_kerf."""
    field = 'kerf_adjusted_parts'
    if field not in state:
        raise ValueError(f"Censor C06: missing '{field}' in pipeline state")
    # kerf-adjusted parts
    for p in data:
        assert "kerf" in p or "length" in p, f"Bad kerf part: {p}"
    return state

if __name__ == '__main__':
    print('Censor C06 (b06_kerf) OK')
