"""C12 - Censor for b12_cnc_biesse"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b12_cnc_biesse."""
    field = 'cnc_biesse'
    if field not in state:
        raise ValueError(f"Censor C12: missing '{field}' in pipeline state")
    pass
    return state

if __name__ == '__main__':
    print('Censor C12 (b12_cnc_biesse) OK')
