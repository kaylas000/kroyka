"""C15 - Censor for b15_cnc_gcode"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b15_cnc_gcode."""
    field = 'cnc_gcode'
    if field not in state:
        raise ValueError(f"Censor C15: missing '{field}' in pipeline state")
    pass
    return state

if __name__ == '__main__':
    print('Censor C15 (b15_cnc_gcode) OK')
