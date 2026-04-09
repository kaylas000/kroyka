"""C02 - Censor for b02_validator"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from kroyka.models import PipelineState

def run(state: PipelineState) -> PipelineState:
    """Validates output of b02_validator."""
    field = 'validated_parts'
    if field not in state:
        raise ValueError(f"Censor C02: missing '{field}' in pipeline state")
    # all parts must have name
    for p in data:
        assert p.get("name"), f"Part missing name: {p}"
    return state

if __name__ == '__main__':
    print('Censor C02 (b02_validator) OK')
