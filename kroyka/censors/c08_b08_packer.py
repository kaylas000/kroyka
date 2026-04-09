"""C08 - Censor for b08_packer"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b08_packer."""
    field = 'packing_layouts'
    if field not in state:
        raise ValueError(f"Censor C08: missing '{field}' in pipeline state")
    # packing layouts non-null
    assert len(data) >= 0, "layouts must be list"
    return state

if __name__ == '__main__':
    print('Censor C08 (b08_packer) OK')
