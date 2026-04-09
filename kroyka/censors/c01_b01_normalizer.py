"""C01 - Censor for b01_normalizer"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b01_normalizer."""
    field = 'normalized_parts'
    if field not in state:
        raise ValueError(f"Censor C01: missing '{field}' in pipeline state")
    # check all parts have length/width
    for p in data:
        assert p.get("length") and p.get("width"), f"Missing dims in {p}"
    return state

if __name__ == '__main__':
    print('Censor C01 (b01_normalizer) OK')
