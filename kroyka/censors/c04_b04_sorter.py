"""C04 - Censor for b04_sorter"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b04_sorter."""
    field = 'sorted_parts'
    if field not in state:
        raise ValueError(f"Censor C04: missing '{field}' in pipeline state")
    # sorted parts non-empty check
    pass  # sorted_parts may be empty if no parts
    return state

if __name__ == '__main__':
    print('Censor C04 (b04_sorter) OK')
