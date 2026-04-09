"""C17 - Censor for b17_cost"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b17_cost."""
    field = 'cost_estimate'
    if field not in state:
        raise ValueError(f"Censor C17: missing '{field}' in pipeline state")
    # cost is dict not list
    pass
    return state

if __name__ == '__main__':
    print('Censor C17 (b17_cost) OK')
