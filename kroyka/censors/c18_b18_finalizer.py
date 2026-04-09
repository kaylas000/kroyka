"""C18 - Censor for b18_finalizer"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b18_finalizer."""
    field = 'pipeline_result'
    if field not in state:
        raise ValueError(f"Censor C18: missing '{field}' in pipeline state")
    # final result
    pass
    return state

if __name__ == '__main__':
    print('Censor C18 (b18_finalizer) OK')
