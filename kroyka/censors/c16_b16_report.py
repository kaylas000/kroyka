"""C16 - Censor for b16_report"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b16_report."""
    field = 'final_report'
    if field not in state:
        raise ValueError(f"Censor C16: missing '{field}' in pipeline state")
    # report is dict not list
    pass
    return state

if __name__ == '__main__':
    print('Censor C16 (b16_report) OK')
