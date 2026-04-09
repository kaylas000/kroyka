"""C07 - Censor for b07_labeler"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b07_labeler."""
    field = 'labeled_parts'
    if field not in state:
        raise ValueError(f"Censor C07: missing '{field}' in pipeline state")
    # labeled parts have label
    for p in data:
        assert "label" in p, f"Part missing label: {p}"
    return state

if __name__ == '__main__':
    print('Censor C07 (b07_labeler) OK')
