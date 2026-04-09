"""C05 - Censor for b05_stock_picker"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b05_stock_picker."""
    field = 'stock_sheets'
    if field not in state:
        raise ValueError(f"Censor C05: missing '{field}' in pipeline state")
    # sheets must have dimensions
    for s in data:
        assert s.get("length") and s.get("width"), f"Sheet missing dims: {s}"
    return state

if __name__ == '__main__':
    print('Censor C05 (b05_stock_picker) OK')
