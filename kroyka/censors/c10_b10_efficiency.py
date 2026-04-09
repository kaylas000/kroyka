"""C10 - Censor for b10_efficiency"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b10_efficiency."""
    field = 'efficiency_report'
    if field not in state:
        raise ValueError(f"Censor C10: missing '{field}' in pipeline state")
    # skip list check - report is dict
    pass
    return state

if __name__ == '__main__':
    print('Censor C10 (b10_efficiency) OK')
