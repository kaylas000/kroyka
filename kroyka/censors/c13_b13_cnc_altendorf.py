"""C13 - Censor for b13_cnc_altendorf"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b13_cnc_altendorf."""
    field = 'cnc_altendorf'
    if field not in state:
        raise ValueError(f"Censor C13: missing '{field}' in pipeline state")
    pass
    return state

if __name__ == '__main__':
    print('Censor C13 (b13_cnc_altendorf) OK')
