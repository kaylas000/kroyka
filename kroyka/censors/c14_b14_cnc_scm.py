"""C14 - Censor for b14_cnc_scm"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b14_cnc_scm."""
    field = 'cnc_scm'
    if field not in state:
        raise ValueError(f"Censor C14: missing '{field}' in pipeline state")
    pass
    return state

if __name__ == '__main__':
    print('Censor C14 (b14_cnc_scm) OK')
