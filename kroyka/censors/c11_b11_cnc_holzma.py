"""C11 - Censor for b11_cnc_holzma"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b11_cnc_holzma."""
    field = 'cnc_holzma'
    if field not in state:
        raise ValueError(f"Censor C11: missing '{field}' in pipeline state")
    # CNC programs are strings
    for c in data:
        assert isinstance(c, (str, dict)), f"Bad holzma prog: {c}"
    return state

if __name__ == '__main__':
    print('Censor C11 (b11_cnc_holzma) OK')
