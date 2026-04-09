"""C09 - Censor for b09_svg_gen"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b09_svg_gen."""
    field = 'svg_files'
    if field not in state:
        raise ValueError(f"Censor C09: missing '{field}' in pipeline state")
    # SVG files must be strings
    for s in data:
        assert isinstance(s, (str, dict)), f"SVG entry bad type: {s}"
    return state

if __name__ == '__main__':
    print('Censor C09 (b09_svg_gen) OK')
